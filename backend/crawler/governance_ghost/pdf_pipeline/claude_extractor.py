import json
import logging
import os

import anthropic

from app.config import settings

logger = logging.getLogger(__name__)


def _mock_nlp_enabled() -> bool:
    """Check if MOCK_NLP is enabled via environment variable."""
    return os.environ.get("MOCK_NLP", "").lower() == "true"

EXTRACTION_PROMPTS = {
    "bid_notice": """Extract structured data from this Philippine government bid notice document.
Return a JSON object with these fields:
- reference_number: PhilGEPS reference number
- title: Project title
- procuring_entity: The government agency/LGU
- approved_budget: Approved budget in PHP (number only)
- bid_submission_deadline: Date string (YYYY-MM-DD)
- project_category: Infrastructure/Health/Education/etc.
- location: City/Municipality name
- description: Brief project description
- key_requirements: List of notable requirements

For each field, also include a confidence score (0.0-1.0).
Return ONLY valid JSON, no markdown formatting.""",

    "award_notice": """Extract structured data from this Philippine government award notice.
Return a JSON object with:
- reference_number: PhilGEPS reference number
- title: Project title
- procuring_entity: Government agency/LGU
- winning_bidder: Name of awarded contractor
- contract_amount: Contract amount in PHP (number only)
- award_date: Date (YYYY-MM-DD)
- project_category: Infrastructure/Health/Education/etc.
- location: City/Municipality name

Include confidence scores (0.0-1.0) for each field.
Return ONLY valid JSON.""",

    "budget_document": """Extract budget allocation data from this Philippine government budget document.
Return a JSON object with:
- lgu_name: The LGU or agency name
- fiscal_year: The fiscal year
- allocations: Array of objects, each with:
  - category: Budget category (e.g., Infrastructure, Health, Education, Social Services)
  - subcategory: Specific line item
  - amount: Allocated amount in PHP (number only)
- total_budget: Total budget amount
- source_document_type: GAA/NEP/Annual Investment Program/etc.

Include confidence scores. Return ONLY valid JSON.""",

    "audit_report": """Extract key findings from this COA (Commission on Audit) report.
Return a JSON object with:
- lgu_name: Audited LGU/agency
- audit_year: Year covered
- findings: Array of objects, each with:
  - finding_type: observation/disallowance/suspension/charge
  - description: Brief description
  - amount: Amount involved in PHP (number only, if applicable)
  - recommendation: Auditor's recommendation
- total_disallowances: Total disallowed amount
- overall_assessment: Brief overall assessment

Include confidence scores. Return ONLY valid JSON.""",

    "promise_extraction": """Extract all specific commitments, pledges, and promises made by \
government officials from this document (speech transcript, news article, executive order, \
development plan, or public hearing record).

Return a JSON object with:
- promises: Array of objects, each with:
  - official_name: Full name of the government official who made the promise
  - position: Their title/position (e.g., City Mayor, Governor, Congressman)
  - promise_text: The exact or closely paraphrased promise/commitment text
  - target_date: Promised completion date if mentioned (YYYY-MM-DD), or null
  - budget_mentioned: Budget amount in PHP (number only) if mentioned, or null
  - category: One of Infrastructure/Health/Education/Social Services/Environment/\
Public Safety/Economic Development/Housing/Technology/Governance
  - confidence: Confidence score (0.0-1.0) that this is a genuine verifiable commitment

Only include specific, verifiable commitments — not vague aspirational statements. \
A promise must have a clear deliverable or measurable outcome.

Include an overall confidence score. Return ONLY valid JSON.""",
}


class ClaudeExtractor:
    """Extract structured data from government document text using Claude API."""

    def __init__(self):
        if _mock_nlp_enabled():
            logger.info("MOCK_NLP is enabled; skipping Anthropic client initialisation")
            self.client = None
        else:
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def extract_structured_data(
        self, raw_text: str, document_type: str
    ) -> dict:
        """Extract structured data from raw document text.

        Args:
            raw_text: OCR-extracted text from the document
            document_type: One of 'bid_notice', 'award_notice', 'budget_document', 'audit_report'

        Returns:
            Structured data dictionary with confidence scores
        """
        if _mock_nlp_enabled():
            from governance_ghost.pdf_pipeline.mock_data import (
                MOCK_STRUCTURED_AUDIT,
                MOCK_STRUCTURED_AWARD_NOTICE,
                MOCK_STRUCTURED_BID_NOTICE,
                MOCK_STRUCTURED_BUDGET,
                MOCK_STRUCTURED_PROMISES,
            )

            logger.info(
                "MOCK_NLP: returning canned structured data instead of calling Claude API"
            )
            mock_dispatch = {
                "award_notice": MOCK_STRUCTURED_AWARD_NOTICE,
                "bid_notice": MOCK_STRUCTURED_BID_NOTICE,
                "budget_document": MOCK_STRUCTURED_BUDGET,
                "audit_report": MOCK_STRUCTURED_AUDIT,
                "promise_extraction": MOCK_STRUCTURED_PROMISES,
            }
            return mock_dispatch.get(document_type, MOCK_STRUCTURED_BID_NOTICE)

        prompt = EXTRACTION_PROMPTS.get(document_type)
        if not prompt:
            logger.warning(f"No extraction prompt for document type: {document_type}")
            prompt = f"Extract all structured data from this government document. Return valid JSON with field names and confidence scores.\nDocument type: {document_type}"

        # Truncate very long documents to stay within token limits
        max_chars = 50000
        if len(raw_text) > max_chars:
            logger.warning(
                f"Document text truncated from {len(raw_text)} to {max_chars} chars"
            )
            raw_text = raw_text[:max_chars]

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n---\nDOCUMENT TEXT:\n{raw_text}",
                    }
                ],
            )
            response_text = message.content[0].text.strip()

            # Parse JSON from response (handle potential markdown wrapping)
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0]

            structured_data = json.loads(response_text)
            logger.info(f"Successfully extracted {len(structured_data)} fields")
            return structured_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            return {"error": "JSON parse error", "raw_response": response_text}
        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            return {"error": str(e)}
