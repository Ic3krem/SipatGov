"""ML-powered (lightweight) validation for scraped Philippine government data.

Design principles:
- Rule-based checks handle ~90% of cases (no heavy ML deps).
- Claude API is called only for ambiguous edge cases via ``_claude_verify``.
- Returns a ``ValidationResult`` with a 0-1 quality score per item.
"""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone

import anthropic

from governance_ghost.validation.models import ValidationResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

# Known PhilGEPS reference number pattern: varies, but commonly numeric or
# alphanumeric with hyphens.  We accept a relaxed pattern.
_PHILGEPS_REF_RE = re.compile(r"^[\w\-]{4,30}$", re.IGNORECASE)

# Valid budget categories used by DBM / Philippine LGU budgets
KNOWN_BUDGET_CATEGORIES = {
    "general public services",
    "education",
    "health",
    "social services",
    "social welfare",
    "economic services",
    "infrastructure",
    "public works",
    "public order and safety",
    "housing",
    "environment",
    "debt service",
    "other purposes",
    "personnel services",
    "maintenance and other operating expenses",
    "capital outlay",
    "mooe",
    "ps",
    "co",
    "agriculture",
    "tourism",
    "transportation",
    "water supply",
    "energy",
    "science and technology",
    "labor and employment",
    "trade and industry",
}

VALID_FOI_STATUSES = {
    "pending",
    "processing",
    "successful",
    "denied",
    "partially_successful",
    "closed",
    "awaiting_clarification",
    "proactively_disclosed",
    "referred",
    "accepted",
    "awaiting",
    "info_under_exceptions",
}

VALID_AUDIT_FINDING_TYPES = {
    "observation",
    "disallowance",
    "suspension",
    "charge",
}

# Budget reasonability ranges per broad category (in PHP)
_BUDGET_RANGES: dict[str, tuple[float, float]] = {
    "general public services": (100_000, 50_000_000_000),
    "education": (100_000, 80_000_000_000),
    "health": (50_000, 50_000_000_000),
    "infrastructure": (100_000, 100_000_000_000),
    "social services": (50_000, 30_000_000_000),
    "social welfare": (50_000, 30_000_000_000),
    "public works": (100_000, 100_000_000_000),
    "_default": (1_000, 100_000_000_000),
}


def _mock_nlp_enabled() -> bool:
    return os.environ.get("MOCK_NLP", "").lower() == "true"


class DataValidator:
    """Validates scraped government data for quality and completeness.

    All validation is rule-based except ``_claude_verify`` which calls the
    Claude API for ambiguous items (score between 0.4 and 0.7 with specific
    heuristic triggers).
    """

    def __init__(self) -> None:
        self._claude_client: anthropic.Anthropic | None = None
        if not _mock_nlp_enabled():
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if api_key:
                self._claude_client = anthropic.Anthropic(api_key=api_key)

        # In-memory cache of recent item title tokens for duplicate detection.
        # Kept per spider run (reset when the pipeline opens a new spider).
        self._recent_titles: list[set[str]] = []
        self._max_recent = 500

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_item(self, item, item_type: str) -> ValidationResult:
        """Score an item 0.0-1.0 for quality.

        ``item_type`` is the Scrapy item class name, e.g. ``BidNoticeItem``.
        """
        dispatch = {
            "BidNoticeItem": self._validate_bid_notice,
            "AwardNoticeItem": self._validate_award_notice,
            "BudgetItem": self._validate_budget,
            "AuditReportItem": self._validate_audit,
            "FOIRequestItem": self._validate_foi,
            "GovernmentDocumentItem": self._validate_generic,
        }
        validator_fn = dispatch.get(item_type, self._validate_generic)

        try:
            result = validator_fn(dict(item))
        except Exception as exc:
            logger.exception("Validation failed for %s", item_type)
            return ValidationResult(
                score=0.5,
                issues=[f"Validation error: {exc}"],
            )

        # Duplicate similarity check
        title = dict(item).get("title", "")
        if title:
            dup_score = self._check_duplicate_similarity(dict(item), self._recent_titles)
            if dup_score > 0.85:
                result.issues.append(
                    f"Possible near-duplicate (similarity={dup_score:.2f})"
                )
                result.score = max(0.0, result.score - 0.2)

            # Cache title tokens
            tokens = self._tokenize(title)
            if tokens:
                self._recent_titles.append(tokens)
                if len(self._recent_titles) > self._max_recent:
                    self._recent_titles.pop(0)

        # Claude verification for ambiguous items
        if 0.4 <= result.score <= 0.7 and result.issues and self._claude_client:
            result = self._claude_verify(dict(item), item_type, result)

        # Recompute flags after potential score changes
        result.auto_approve = result.score > 0.8
        result.needs_review = 0.3 <= result.score <= 0.8

        return result

    # ------------------------------------------------------------------
    # Per-type validators
    # ------------------------------------------------------------------

    def _validate_bid_notice(self, item: dict) -> ValidationResult:
        """Validate a PhilGEPS bid notice item."""
        issues: list[str] = []
        checks_passed = 0
        total_checks = 5

        # 1. Reference number format
        ref = str(item.get("reference_number", "") or "").strip()
        if not ref:
            issues.append("Missing reference_number")
        elif not _PHILGEPS_REF_RE.match(ref):
            issues.append(f"Suspicious reference_number format: '{ref}'")
        else:
            checks_passed += 1

        # 2. Approved budget is numeric and > 0
        budget = item.get("approved_budget")
        if budget is None or budget == "":
            issues.append("Missing approved_budget")
        else:
            try:
                budget_val = float(str(budget).replace(",", "").replace("PHP", "").strip())
                if budget_val <= 0:
                    issues.append(f"approved_budget must be > 0, got {budget_val}")
                elif budget_val > 100_000_000_000:
                    issues.append(f"approved_budget suspiciously large: {budget_val}")
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(f"approved_budget not numeric: '{budget}'")

        # 3. Procuring entity not empty
        entity = str(item.get("procuring_entity", "") or "").strip()
        if not entity:
            issues.append("Missing procuring_entity")
        elif len(entity) < 3:
            issues.append(f"procuring_entity too short: '{entity}'")
        else:
            checks_passed += 1

        # 4. Bid submission deadline is a parseable future date
        deadline = str(item.get("bid_submission_deadline", "") or "").strip()
        if not deadline:
            issues.append("Missing bid_submission_deadline")
        else:
            parsed = self._parse_date(deadline)
            if parsed is None:
                issues.append(f"Cannot parse bid_submission_deadline: '{deadline}'")
            else:
                checks_passed += 1

        # 5. Title not empty
        title = str(item.get("title", "") or "").strip()
        if not title:
            issues.append("Missing title")
        elif len(title) < 5:
            issues.append(f"Title suspiciously short: '{title}'")
        else:
            checks_passed += 1

        score = checks_passed / total_checks
        return ValidationResult(score=score, issues=issues)

    def _validate_award_notice(self, item: dict) -> ValidationResult:
        """Validate a PhilGEPS award notice item."""
        issues: list[str] = []
        checks_passed = 0
        total_checks = 5

        # 1. Reference number
        ref = str(item.get("reference_number", "") or "").strip()
        if not ref:
            issues.append("Missing reference_number")
        elif not _PHILGEPS_REF_RE.match(ref):
            issues.append(f"Suspicious reference_number format: '{ref}'")
        else:
            checks_passed += 1

        # 2. Title
        title = str(item.get("title", "") or "").strip()
        if not title:
            issues.append("Missing title")
        else:
            checks_passed += 1

        # 3. Procuring entity
        entity = str(item.get("procuring_entity", "") or "").strip()
        if not entity:
            issues.append("Missing procuring_entity")
        else:
            checks_passed += 1

        # 4. Winning bidder
        bidder = str(item.get("winning_bidder", "") or "").strip()
        if not bidder:
            issues.append("Missing winning_bidder")
        else:
            checks_passed += 1

        # 5. Contract amount
        amount = item.get("contract_amount")
        if amount is None or amount == "":
            issues.append("Missing contract_amount")
        else:
            try:
                val = float(str(amount).replace(",", "").replace("PHP", "").strip())
                if val <= 0:
                    issues.append(f"contract_amount must be > 0, got {val}")
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(f"contract_amount not numeric: '{amount}'")

        score = checks_passed / total_checks
        return ValidationResult(score=score, issues=issues)

    def _validate_budget(self, item: dict) -> ValidationResult:
        """Validate a DBM budget allocation item."""
        issues: list[str] = []
        checks_passed = 0
        total_checks = 4

        # 1. Fiscal year in valid range
        fy = item.get("fiscal_year")
        if fy is None:
            issues.append("Missing fiscal_year")
        else:
            try:
                fy_int = int(fy)
                if not (2020 <= fy_int <= 2030):
                    issues.append(f"fiscal_year out of range (2020-2030): {fy_int}")
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(f"fiscal_year not a valid integer: '{fy}'")

        # 2. Amount is reasonable
        amount = item.get("allocated_amount")
        if amount is None or amount == "":
            issues.append("Missing allocated_amount")
        else:
            try:
                amount_val = float(
                    str(amount).replace(",", "").replace("PHP", "").strip()
                )
                category = str(item.get("category", "") or "").strip().lower()
                if not self._validate_budget_reasonability(amount_val, category):
                    issues.append(
                        f"Budget amount {amount_val} outside reasonable range for '{category}'"
                    )
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(f"allocated_amount not numeric: '{amount}'")

        # 3. Category matches known budget categories
        category = str(item.get("category", "") or "").strip().lower()
        if not category:
            issues.append("Missing category")
        elif category not in KNOWN_BUDGET_CATEGORIES:
            # Partial match — allow if a known category is a substring
            matched = any(known in category or category in known for known in KNOWN_BUDGET_CATEGORIES)
            if matched:
                checks_passed += 1
            else:
                issues.append(f"Unknown budget category: '{category}'")
        else:
            checks_passed += 1

        # 4. LGU name resolves (non-empty is good enough here)
        lgu = str(item.get("lgu_name", "") or "").strip()
        if not lgu:
            issues.append("Missing lgu_name")
        elif len(lgu) < 2:
            issues.append(f"lgu_name too short: '{lgu}'")
        else:
            checks_passed += 1

        score = checks_passed / total_checks
        return ValidationResult(score=score, issues=issues)

    def _validate_audit(self, item: dict) -> ValidationResult:
        """Validate a COA audit report item."""
        issues: list[str] = []
        checks_passed = 0
        total_checks = 4

        # 1. Audit year is valid
        year = item.get("audit_year")
        if year is None:
            issues.append("Missing audit_year")
        else:
            try:
                year_int = int(year)
                current_year = datetime.now(timezone.utc).year
                if not (2010 <= year_int <= current_year):
                    issues.append(
                        f"audit_year out of range (2010-{current_year}): {year_int}"
                    )
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(f"audit_year not a valid integer: '{year}'")

        # 2. Findings summary is not empty
        findings = str(item.get("findings_summary", "") or "").strip()
        if not findings:
            issues.append("Missing findings_summary")
        elif len(findings) < 10:
            issues.append("findings_summary too brief")
        else:
            checks_passed += 1

        # 3. Total disallowances is numeric
        disallowances = item.get("total_disallowances")
        if disallowances is not None and disallowances != "":
            try:
                val = float(
                    str(disallowances).replace(",", "").replace("PHP", "").strip()
                )
                if val < 0:
                    issues.append(f"total_disallowances negative: {val}")
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(
                    f"total_disallowances not numeric: '{disallowances}'"
                )
        else:
            # Disallowances can legitimately be absent (clean audit)
            checks_passed += 1

        # 4. LGU name resolves
        lgu = str(item.get("lgu_name", "") or "").strip()
        if not lgu:
            issues.append("Missing lgu_name")
        elif len(lgu) < 2:
            issues.append(f"lgu_name too short: '{lgu}'")
        else:
            checks_passed += 1

        score = checks_passed / total_checks
        return ValidationResult(score=score, issues=issues)

    def _validate_foi(self, item: dict) -> ValidationResult:
        """Validate an e-FOI request item."""
        issues: list[str] = []
        checks_passed = 0
        total_checks = 3

        # 1. Agency name not empty
        agency = str(item.get("agency_name", "") or "").strip()
        if not agency:
            issues.append("Missing agency_name")
        elif len(agency) < 2:
            issues.append(f"agency_name too short: '{agency}'")
        else:
            checks_passed += 1

        # 2. Status is a valid enum value
        status = str(item.get("status", "") or "").strip().lower()
        if not status:
            issues.append("Missing status")
        elif status not in VALID_FOI_STATUSES:
            issues.append(
                f"Unknown FOI status: '{status}'. "
                f"Expected one of: {sorted(VALID_FOI_STATUSES)}"
            )
        else:
            checks_passed += 1

        # 3. Processing days is reasonable
        days = item.get("processing_days")
        if days is not None and days != "":
            try:
                days_val = int(days)
                if not (0 <= days_val <= 365):
                    issues.append(
                        f"processing_days out of range (0-365): {days_val}"
                    )
                else:
                    checks_passed += 1
            except (ValueError, TypeError):
                issues.append(f"processing_days not an integer: '{days}'")
        else:
            # Processing days may not be available for pending requests
            checks_passed += 1

        score = checks_passed / total_checks
        return ValidationResult(score=score, issues=issues)

    def _validate_generic(self, item: dict) -> ValidationResult:
        """Fallback validation for GovernmentDocumentItem or unknown types."""
        issues: list[str] = []
        checks_passed = 0
        total_checks = 2

        title = str(item.get("title", "") or "").strip()
        if not title:
            issues.append("Missing title")
        else:
            checks_passed += 1

        source_url = str(item.get("source_url", "") or "").strip()
        if not source_url:
            issues.append("Missing source_url")
        else:
            checks_passed += 1

        score = checks_passed / total_checks
        return ValidationResult(score=score, issues=issues)

    # ------------------------------------------------------------------
    # Duplicate detection
    # ------------------------------------------------------------------

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        """Lowercase tokenisation for Jaccard similarity."""
        return {
            w
            for w in re.split(r"\W+", text.lower())
            if len(w) > 2  # skip very short tokens
        }

    def _check_duplicate_similarity(
        self, item: dict, existing_items: list[set[str]]
    ) -> float:
        """Jaccard similarity of title tokens against recently seen items.

        Returns the *maximum* similarity found (0.0 - 1.0).
        """
        title = str(item.get("title", "") or "")
        tokens = self._tokenize(title)
        if not tokens or not existing_items:
            return 0.0

        max_sim = 0.0
        for existing_tokens in existing_items:
            if not existing_tokens:
                continue
            intersection = tokens & existing_tokens
            union = tokens | existing_tokens
            sim = len(intersection) / len(union) if union else 0.0
            if sim > max_sim:
                max_sim = sim
        return max_sim

    # ------------------------------------------------------------------
    # Budget reasonability
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_budget_reasonability(
        amount: float,
        category: str,
        lgu_population: int | None = None,
    ) -> bool:
        """Sanity-check a budget amount against known ranges per category."""
        key = category.lower() if category else "_default"
        lo, hi = _BUDGET_RANGES.get(key, _BUDGET_RANGES["_default"])

        # If we know the population, scale the upper bound
        if lgu_population and lgu_population > 0:
            per_capita_max = 200_000  # generous PHP 200K per capita ceiling
            hi = min(hi, lgu_population * per_capita_max)

        return lo <= amount <= hi

    # ------------------------------------------------------------------
    # Claude edge-case verification
    # ------------------------------------------------------------------

    def _claude_verify(
        self,
        item: dict,
        item_type: str,
        preliminary: ValidationResult,
    ) -> ValidationResult:
        """Ask Claude to verify an ambiguous item.

        Only called when the rule-based score is between 0.4 and 0.7 and
        there are flagged issues.  Returns an updated ``ValidationResult``.
        """
        if self._claude_client is None:
            return preliminary

        # Build a concise prompt
        item_summary = json.dumps(
            {k: v for k, v in item.items() if not str(k).startswith("_")},
            default=str,
            indent=2,
        )
        issues_text = "\n".join(f"- {i}" for i in preliminary.issues)

        prompt = (
            "You are a data-quality reviewer for Philippine government data "
            "scraped from official portals (PhilGEPS, DBM, COA, e-FOI).\n\n"
            f"Item type: {item_type}\n"
            f"Preliminary quality score: {preliminary.score:.2f}\n"
            f"Flagged issues:\n{issues_text}\n\n"
            f"Item data:\n```json\n{item_summary}\n```\n\n"
            "Evaluate whether the flagged issues are genuine data-quality "
            "problems or false positives.  Respond with ONLY a JSON object:\n"
            '{"adjusted_score": <float 0-1>, "real_issues": [<strings>], '
            '"explanation": "<brief>"}'
        )

        try:
            message = self._claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            response_text = message.content[0].text.strip()

            # Strip markdown fences if present
            if response_text.startswith("```"):
                response_text = (
                    response_text.split("\n", 1)[1].rsplit("```", 1)[0]
                )

            data = json.loads(response_text)
            adjusted = float(data.get("adjusted_score", preliminary.score))
            real_issues = data.get("real_issues", preliminary.issues)

            logger.info(
                "Claude verification: score %.2f -> %.2f for %s",
                preliminary.score,
                adjusted,
                item_type,
            )

            return ValidationResult(
                score=max(0.0, min(1.0, adjusted)),
                issues=real_issues if isinstance(real_issues, list) else preliminary.issues,
                claude_verified=True,
            )

        except (json.JSONDecodeError, anthropic.APIError, KeyError) as exc:
            logger.warning("Claude verification failed: %s", exc)
            return preliminary

    # ------------------------------------------------------------------
    # Date parsing helper
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_date(value: str) -> datetime | None:
        """Try common date formats and return a datetime or None."""
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
        ]
        value = value.strip()
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None
