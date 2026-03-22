import pytest


@pytest.fixture
def sample_bid_html():
    """Sample PhilGEPS bid notice HTML for spider testing."""
    return """
    <html>
    <body>
        <h2 class="opportunity-title">Construction of Municipal Health Center</h2>
        <span id="ContentPlaceHolder1_lblRefNo">12345678</span>
        <span id="ContentPlaceHolder1_lblProcEntity">Municipality of San Isidro</span>
        <span id="ContentPlaceHolder1_lblABC">PHP 5,000,000.00</span>
        <span id="ContentPlaceHolder1_lblDeadline">2026-04-15</span>
        <a href="/docs/bid_doc.pdf">Download Bid Document</a>
    </body>
    </html>
    """
