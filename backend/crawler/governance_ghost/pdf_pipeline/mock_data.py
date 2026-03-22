"""Canned OCR text and structured extraction results for local testing.

Used when MOCK_OCR=true or MOCK_NLP=true to avoid calling AWS Textract
and the Claude API during development.
"""

# ---------------------------------------------------------------------------
# Mock OCR output  (simulates Textract raw text from a PhilGEPS bid notice)
# ---------------------------------------------------------------------------
MOCK_OCR_BID_NOTICE_TEXT = """\
Republic of the Philippines
PHILIPPINE GOVERNMENT ELECTRONIC PROCUREMENT SYSTEM (PhilGEPS)

INVITATION TO BID

Reference No.: 2024-BID-00312
Project Title: Construction of Two-Storey Municipal Health Center
Procuring Entity: Municipality of San Miguel, Bulacan
Approved Budget for the Contract (ABC): PHP 45,000,000.00

Deadline for Submission of Bids: March 15, 2025, 10:00 AM

Project Description:
The Municipality of San Miguel, Bulacan intends to undertake the construction
of a two-storey municipal health center with the following scope of work:
- Structural works including foundation, columns, beams, and slabs
- Architectural finishing including tiling, painting, and ceiling works
- Electrical works including power distribution and lighting
- Plumbing and sanitary works
- Installation of medical gas system

Project Location: Brgy. Poblacion, San Miguel, Bulacan

Key Requirements:
1. Contractor must have PCAB License Category A or higher
2. Must have completed at least one similar project within the last 5 years
3. Minimum 3 years of experience in health facility construction
4. PhilGEPS Platinum Membership
5. Valid Mayor's Permit and Business Registration

Funding Source: Local Government Fund (General Fund FY 2024)

Contact Person: Engr. Maria Santos, BAC Chairperson
Email: bac@sanmiguel.gov.ph
Phone: (044) 764-1234
"""

# ---------------------------------------------------------------------------
# Mock structured extraction  (simulates Claude NLP output)
# ---------------------------------------------------------------------------
MOCK_STRUCTURED_BID_NOTICE = {
    "reference_number": {
        "value": "2024-BID-00312",
        "confidence": 0.98,
    },
    "title": {
        "value": "Construction of Two-Storey Municipal Health Center",
        "confidence": 0.97,
    },
    "procuring_entity": {
        "value": "Municipality of San Miguel, Bulacan",
        "confidence": 0.96,
    },
    "approved_budget": {
        "value": 45000000.00,
        "confidence": 0.95,
    },
    "bid_submission_deadline": {
        "value": "2025-03-15",
        "confidence": 0.94,
    },
    "project_category": {
        "value": "Infrastructure",
        "confidence": 0.92,
    },
    "location": {
        "value": "San Miguel, Bulacan",
        "confidence": 0.93,
    },
    "description": {
        "value": (
            "Construction of a two-storey municipal health center including "
            "structural, architectural, electrical, plumbing, and medical gas works."
        ),
        "confidence": 0.91,
    },
    "key_requirements": {
        "value": [
            "PCAB License Category A or higher",
            "At least one similar project completed in last 5 years",
            "Minimum 3 years health facility construction experience",
            "PhilGEPS Platinum Membership",
            "Valid Mayor's Permit and Business Registration",
        ],
        "confidence": 0.90,
    },
}

MOCK_STRUCTURED_AWARD_NOTICE = {
    "reference_number": {
        "value": "2024-AWD-00198",
        "confidence": 0.97,
    },
    "title": {
        "value": "Construction of Two-Storey Municipal Health Center",
        "confidence": 0.96,
    },
    "procuring_entity": {
        "value": "Municipality of San Miguel, Bulacan",
        "confidence": 0.95,
    },
    "winning_bidder": {
        "value": "JDC Construction Corp.",
        "confidence": 0.94,
    },
    "contract_amount": {
        "value": 43500000.00,
        "confidence": 0.93,
    },
    "award_date": {
        "value": "2025-04-01",
        "confidence": 0.92,
    },
    "project_category": {
        "value": "Infrastructure",
        "confidence": 0.91,
    },
    "location": {
        "value": "San Miguel, Bulacan",
        "confidence": 0.90,
    },
}
