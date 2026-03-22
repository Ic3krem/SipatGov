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

# ---------------------------------------------------------------------------
# Mock OCR output  (simulates Textract raw text from a GAA budget document)
# ---------------------------------------------------------------------------
MOCK_OCR_BUDGET_DOCUMENT_TEXT = """\
Republic of the Philippines
DEPARTMENT OF BUDGET AND MANAGEMENT

GENERAL APPROPRIATIONS ACT (GAA)
FISCAL YEAR 2025

LOCAL GOVERNMENT UNIT: QUEZON CITY
Region: National Capital Region (NCR)

SUMMARY OF APPROPRIATIONS BY SECTOR

I. GENERAL PUBLIC SERVICES
   A. Executive Services
      Personal Services .......................... PHP 1,250,000,000.00
      Maintenance and Other Operating Expenses ...  PHP   380,000,000.00
      Capital Outlay .............................  PHP   120,000,000.00
   Subtotal, Executive Services ..................  PHP 1,750,000,000.00

   B. Legislative Services
      Personal Services ..........................  PHP   210,000,000.00
      MOOE .......................................  PHP    85,000,000.00
   Subtotal, Legislative Services ................  PHP   295,000,000.00

II. EDUCATION, CULTURE AND SPORTS / MANPOWER DEVELOPMENT
    A. Elementary and Secondary Education
       Classroom Construction ....................  PHP   420,000,000.00
       School Supplies and Textbooks .............  PHP    95,000,000.00
       Teacher Training and Development ..........  PHP    45,000,000.00
    Subtotal, Education ..........................  PHP   560,000,000.00

    B. Sports Development
       Facility Maintenance ......................  PHP    38,000,000.00
       Youth Sports Programs .....................  PHP    22,000,000.00
    Subtotal, Sports .............................  PHP    60,000,000.00

III. HEALTH, NUTRITION AND POPULATION CONTROL
     A. Hospital Services
        QC General Hospital Operations ...........  PHP   350,000,000.00
        Medical Equipment Acquisition ............  PHP   120,000,000.00
     B. Primary Healthcare
        Barangay Health Centers ..................  PHP   180,000,000.00
        Immunization Programs ....................  PHP    45,000,000.00
        Maternal and Child Health ................  PHP    65,000,000.00
     Subtotal, Health ............................  PHP   760,000,000.00

IV. INFRASTRUCTURE / UTILITIES
    A. Roads and Bridges
       Road Construction and Widening ............  PHP   680,000,000.00
       Bridge Rehabilitation .....................  PHP   150,000,000.00
    B. Drainage and Flood Control
       Flood Control Systems .....................  PHP   520,000,000.00
       Drainage Improvement ......................  PHP   180,000,000.00
    C. Public Buildings
       Government Facility Construction ..........  PHP   220,000,000.00
    Subtotal, Infrastructure .....................  PHP 1,750,000,000.00

V. SOCIAL SERVICES AND SOCIAL WELFARE
   A. Social Welfare Programs
      Cash Transfer Programs .....................  PHP   280,000,000.00
      Livelihood Support .........................  PHP   120,000,000.00
   B. Housing
      Socialized Housing ........................  PHP   350,000,000.00
   C. Disaster Risk Reduction
      DRRM Fund .................................  PHP   180,000,000.00
   Subtotal, Social Services .....................  PHP   930,000,000.00

VI. ECONOMIC SERVICES
    A. Agricultural Programs .....................  PHP    45,000,000.00
    B. Tourism Development ......................  PHP    35,000,000.00
    C. Trade and Industry Support ................  PHP    60,000,000.00
    Subtotal, Economic Services ..................  PHP   140,000,000.00

VII. ENVIRONMENT AND NATURAL RESOURCES
     A. Solid Waste Management ...................  PHP   185,000,000.00
     B. Urban Greening Program ...................  PHP    55,000,000.00
     C. Air Quality Monitoring ...................  PHP    25,000,000.00
     Subtotal, Environment .......................  PHP   265,000,000.00

                                                   =====================
GRAND TOTAL APPROPRIATIONS ......................  PHP 6,510,000,000.00
                                                   =====================

Approved by:
HON. JOY BELMONTE
City Mayor, Quezon City

Date: January 8, 2025
"""

# ---------------------------------------------------------------------------
# Mock structured extraction  (simulates Claude NLP output for budget doc)
# ---------------------------------------------------------------------------
MOCK_STRUCTURED_BUDGET = {
    "lgu_name": {
        "value": "Quezon City",
        "confidence": 0.97,
    },
    "fiscal_year": {
        "value": 2025,
        "confidence": 0.99,
    },
    "allocations": {
        "value": [
            {
                "category": "General Public Services",
                "subcategory": "Executive Services",
                "amount": 1750000000.00,
            },
            {
                "category": "General Public Services",
                "subcategory": "Legislative Services",
                "amount": 295000000.00,
            },
            {
                "category": "Education",
                "subcategory": "Elementary and Secondary Education",
                "amount": 560000000.00,
            },
            {
                "category": "Education",
                "subcategory": "Sports Development",
                "amount": 60000000.00,
            },
            {
                "category": "Health",
                "subcategory": "Hospital Services",
                "amount": 470000000.00,
            },
            {
                "category": "Health",
                "subcategory": "Primary Healthcare",
                "amount": 290000000.00,
            },
            {
                "category": "Infrastructure",
                "subcategory": "Roads and Bridges",
                "amount": 830000000.00,
            },
            {
                "category": "Infrastructure",
                "subcategory": "Drainage and Flood Control",
                "amount": 700000000.00,
            },
            {
                "category": "Infrastructure",
                "subcategory": "Public Buildings",
                "amount": 220000000.00,
            },
            {
                "category": "Social Services",
                "subcategory": "Social Welfare Programs",
                "amount": 400000000.00,
            },
            {
                "category": "Social Services",
                "subcategory": "Housing",
                "amount": 350000000.00,
            },
            {
                "category": "Social Services",
                "subcategory": "Disaster Risk Reduction",
                "amount": 180000000.00,
            },
            {
                "category": "Economic Services",
                "subcategory": "Agricultural Programs",
                "amount": 45000000.00,
            },
            {
                "category": "Economic Services",
                "subcategory": "Tourism Development",
                "amount": 35000000.00,
            },
            {
                "category": "Economic Services",
                "subcategory": "Trade and Industry Support",
                "amount": 60000000.00,
            },
            {
                "category": "Environment",
                "subcategory": "Solid Waste Management",
                "amount": 185000000.00,
            },
            {
                "category": "Environment",
                "subcategory": "Urban Greening Program",
                "amount": 55000000.00,
            },
            {
                "category": "Environment",
                "subcategory": "Air Quality Monitoring",
                "amount": 25000000.00,
            },
        ],
        "confidence": 0.91,
    },
    "total_budget": {
        "value": 6510000000.00,
        "confidence": 0.96,
    },
    "source_document_type": {
        "value": "GAA",
        "confidence": 0.98,
    },
}

# ---------------------------------------------------------------------------
# Mock OCR output  (simulates Textract raw text from a COA audit report)
# ---------------------------------------------------------------------------
MOCK_OCR_AUDIT_REPORT_TEXT = """\
Republic of the Philippines
COMMISSION ON AUDIT
Commonwealth Avenue, Quezon City

ANNUAL AUDIT REPORT
For the Year Ended December 31, 2024

AUDITED ENTITY: CITY GOVERNMENT OF QUEZON CITY
Cluster: Local Government Sector — National Capital Region

I. EXECUTIVE SUMMARY

The audit covered the financial transactions and operations of the City
Government of Quezon City for Calendar Year 2024. The total appropriations
amounted to PHP 6,510,000,000.00 while the total obligations incurred
amounted to PHP 5,892,340,000.00 representing an obligation rate of 90.51%.

II. SIGNIFICANT AUDIT OBSERVATIONS AND RECOMMENDATIONS

Observation No. 1 — Disallowance on Infrastructure Projects
The audit team noted that a total of PHP 48,250,000.00 in payments to
contractors for the Tullahan River Flood Control project were not supported
by complete documentation. Specifically, accomplishment reports for Phases 2
and 3 were not submitted, making it impossible to verify actual physical
progress against billed amounts.

Recommendation: Management should require contractors to submit complete
accomplishment reports before processing payments. The amount of
PHP 48,250,000.00 should be immediately settled or the Notice of
Disallowance shall become final and executory.

Observation No. 2 — Suspension on Procurement Irregularities
Procurement of medical supplies totaling PHP 12,800,000.00 for the QC
General Hospital did not undergo competitive public bidding as required
under RA 9184 (Government Procurement Reform Act). The supplies were
procured through negotiated procurement without proper justification
for the alternative mode.

Recommendation: The BAC and Procurement Office should strictly comply
with RA 9184. Future procurement through alternative modes must include
proper documentation and justification. The amount is hereby suspended
pending submission of justification documents.

Observation No. 3 — Charge on Unliquidated Cash Advances
Cash advances totaling PHP 8,450,000.00 granted to various officials
and employees remained unliquidated beyond the reglementary period
prescribed under COA Circular No. 97-002. Of this amount,
PHP 3,200,000.00 has been outstanding for more than two years.

Recommendation: Management should require immediate liquidation of
outstanding cash advances. Officials with cash advances outstanding
beyond two years should be issued a demand letter. The amount of
PHP 3,200,000.00 is hereby charged to the accountable officers.

Observation No. 4 — Observation on Revenue Collection Efficiency
Real property tax collection efficiency was at 68.2%, below the
national average of 75.4% for highly urbanized cities. Estimated
uncollected real property taxes amount to PHP 2,150,000,000.00
representing a significant revenue gap.

Recommendation: The City Treasurer's Office should intensify
collection efforts, update the tax mapping system, and consider
offering amnesty programs to encourage settlement of delinquencies.

III. STATUS OF PRIOR YEAR'S AUDIT RECOMMENDATIONS

Of the 12 audit recommendations issued in the previous year's report:
- 5 recommendations were fully implemented
- 4 recommendations were partially implemented
- 3 recommendations were not implemented

IV. SUMMARY OF AUDIT DISALLOWANCES, SUSPENSIONS AND CHARGES

                                Amount (PHP)
Disallowances .............. 48,250,000.00
Suspensions ................ 12,800,000.00
Charges ....................  3,200,000.00
                            ===============
Total ...................... 64,250,000.00

Auditor:
ATTY. MARIA LOURDES P. GERMINO
Supervising Auditor
Date: April 15, 2025
"""

# ---------------------------------------------------------------------------
# Mock structured extraction  (simulates Claude NLP output for audit report)
# ---------------------------------------------------------------------------
MOCK_STRUCTURED_AUDIT = {
    "lgu_name": {
        "value": "Quezon City",
        "confidence": 0.98,
    },
    "audit_year": {
        "value": 2024,
        "confidence": 0.99,
    },
    "findings": {
        "value": [
            {
                "finding_type": "disallowance",
                "description": (
                    "Payments totaling PHP 48.25M to contractors for the Tullahan River "
                    "Flood Control project lacked complete accomplishment reports for "
                    "Phases 2 and 3, preventing verification of actual progress."
                ),
                "amount": 48250000.00,
                "recommendation": (
                    "Require contractors to submit complete accomplishment reports "
                    "before processing payments. Settle the amount or the Notice of "
                    "Disallowance becomes final and executory."
                ),
            },
            {
                "finding_type": "suspension",
                "description": (
                    "Procurement of medical supplies worth PHP 12.8M for QC General "
                    "Hospital used negotiated procurement without proper justification, "
                    "violating RA 9184 (Government Procurement Reform Act)."
                ),
                "amount": 12800000.00,
                "recommendation": (
                    "Strictly comply with RA 9184. Alternative procurement modes "
                    "must include proper documentation. Amount suspended pending "
                    "submission of justification documents."
                ),
            },
            {
                "finding_type": "charge",
                "description": (
                    "Cash advances totaling PHP 8.45M remained unliquidated beyond "
                    "the reglementary period. PHP 3.2M has been outstanding for more "
                    "than two years."
                ),
                "amount": 3200000.00,
                "recommendation": (
                    "Require immediate liquidation of outstanding cash advances. "
                    "Issue demand letters to officials with advances outstanding "
                    "beyond two years."
                ),
            },
            {
                "finding_type": "observation",
                "description": (
                    "Real property tax collection efficiency was 68.2%, below the "
                    "national average of 75.4% for highly urbanized cities. Estimated "
                    "uncollected taxes amount to PHP 2.15B."
                ),
                "amount": 2150000000.00,
                "recommendation": (
                    "Intensify collection efforts, update tax mapping system, and "
                    "consider amnesty programs to encourage settlement of delinquencies."
                ),
            },
        ],
        "confidence": 0.93,
    },
    "total_disallowances": {
        "value": 64250000.00,
        "confidence": 0.96,
    },
    "overall_assessment": {
        "value": (
            "The City Government of Quezon City achieved a 90.51% obligation rate "
            "against total appropriations. However, significant findings include "
            "PHP 48.25M in unsupported contractor payments, PHP 12.8M in procurement "
            "irregularities, and PHP 3.2M in unliquidated cash advances. Revenue "
            "collection efficiency at 68.2% is below national averages. Of 12 prior-year "
            "recommendations, only 5 were fully implemented."
        ),
        "confidence": 0.90,
    },
}

# ---------------------------------------------------------------------------
# Mock structured extraction  (simulates Claude NLP output for promise extraction)
# ---------------------------------------------------------------------------
MOCK_STRUCTURED_PROMISES = {
    "promises": {
        "value": [
            {
                "official_name": "Joy Belmonte",
                "position": "City Mayor",
                "promise_text": "Build 5 new public schools in District 1 to address classroom shortage",
                "target_date": "2027-12-31",
                "budget_mentioned": 420000000.00,
                "category": "Education",
                "confidence": 0.88,
            },
            {
                "official_name": "Joy Belmonte",
                "position": "City Mayor",
                "promise_text": "Complete the Tullahan River Flood Control System to protect 50,000 residents",
                "target_date": "2026-06-30",
                "budget_mentioned": 520000000.00,
                "category": "Infrastructure",
                "confidence": 0.92,
            },
            {
                "official_name": "Joy Belmonte",
                "position": "City Mayor",
                "promise_text": "Reduce crime rate by 30% through expanded CCTV network and community policing",
                "target_date": "2026-06-30",
                "budget_mentioned": 125000000.00,
                "category": "Public Safety",
                "confidence": 0.75,
            },
        ],
        "confidence": 0.85,
    },
}
