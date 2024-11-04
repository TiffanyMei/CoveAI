from pydantic import BaseModel, Field
from constants import MM, BN

class Firm(BaseModel):
    """A private equity firm"""
    name: str = Field(..., description="Name of this firm, converted to all lower case.")
    industries: list[str] = Field(..., description="A list of 3 to 5 strings, each being an industry that this firm focuses on, converted to all lower case.")
    revenue: int = Field(..., description="The approximate minimum yearly revenue in USD of companies that this firm prefers to acquire, converted to integer.")
    valuation: int = Field(..., description="The approximate valuation in USD of companies that this firm prefers to acquire, converted to integer.")
    num_employees: int = Field(..., description="The approximate minimum number of employees of companies that this firm prefers to acquire, converted to integer.")
    geography: list[str] = Field(..., description="A list of strings, each being a geographical focus of this firm.")
    distressed: bool = Field(..., description="Whether this firm is interested in acquiring distressed companies.")

"""
Mock database of private equity firms
"""
firms = [
    Firm(
        name="Blackstone",
        industries=["real estate", "energy", "infrastructure", "healthcare", "technology"],
        revenue=50*MM,
        valuation=500*MM,
        num_employees=500,
        geography=["global", "north america", "europe", "asia"],
        distressed=False,
    ),
    Firm(
        name="KKR",
        industries=["healthcare", "technology", "consumer", "energy", "financial services"],
        revenue=100*MM,
        valuation=1 * BN,
        num_employees=1000,
        geography=["global", "united states", "europe", "asia"],
        distressed=True,
    ),
    Firm(
        name="Carlyle Group",
        industries=["aerospace", "defense", "technology", "healthcare", "consumer"],
        revenue=75*MM,
        valuation=750*MM,
        num_employees=500,
        geography=["united states", "europe", "asia", "latin america"],
        distressed=False,
    ),
    Firm(
        name="TPG",
        industries=["healthcare", "technology", "consumer", "financial services"],
        revenue=60*MM,
        valuation=700*MM,
        num_employees=500,
        geography=["north america"],
        distressed=False,
    ),
    Firm(
        name="Thomas Bravo",
        industries=["technology"],
        revenue=50*MM,
        valuation=500*MM,
        num_employees=500,
        geography=["north america"],
        distressed=True,
    ),
    Firm(
        name="Advent International",
        industries=["healthcare", "technology", "industrial", "consumer"],
        revenue=50*MM,
        valuation=500*MM,
        num_employees=500,
        geography=["north america", "europe", "latin america", "asia"],
        distressed=True,
    ),
    Firm(
        name="Walburg Pincus",
        industries=["healthcare", "technology", "energy", "financial services"],
        revenue=75*MM,
        valuation=750*MM,
        num_employees=500,
        geography=["united states", "asia", "europe"],
        distressed=False,
    ),
    Firm(
        name="EQT Partners",
        industries=["healthcare", "technology", "consumer"],
        revenue=100*MM,
        valuation=1 * BN,
        num_employees=1000,
        geography=["europe", "north america", "asia"],
        distressed=False,
    ),
    Firm(
        name="Apollo Global Management",
        industries=["financial services", "natural resources", "real estate", "technology"],
        revenue=100*MM,
        valuation=1 * BN,
        num_employees=1000,
        geography=["global"],
        distressed=True,
    ),
    Firm(
        name="Bain Capital",
        industries=["technology", "healthcare", "financial_services", "industrial"],
        revenue=75*MM,
        valuation=500*MM,
        num_employees=200,
        geography=["global"],
        distressed=False,
    )
]

