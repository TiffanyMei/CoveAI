from pydantic import BaseModel, Field
from typing import Union
import pprint

class Company(BaseModel):
    """A small to medium-sized business (SMB)"""
    name: str = Field(..., description="The name of the company.")
    website: str = Field(..., description="The website URL of the company. None if not found")
    industry: list[str] = Field(..., description="A list of strings, each describing an industry that this company is in, converted to all lower case.")
    funding_stage: str = Field(..., description="The funding stage that this company is currently in, converted to all lower case.")
    valuation: int = Field(..., description="The approximate valuation of this company in USD, converted into an integer.")
    revenue: Union[int, None] = Field(..., description="The approximate yearly revenue of this company in USD, converted to an integer. None if cannot be approximated.")
    investors: list[str] = Field(..., description="A list of strings, each being the name of an investor or fund from which this company has received funding. Empty list if not found.")
    num_employees: Union[int, None] = Field(..., description="The approximate number of employees working for this company or the size of this company's team, converted to integer. None if cannot be counted or approximated.")
    distressed: bool = Field(..., description="Whether this company is a distressed company. False if not found.")
    headquarter_city: Union[str, None] = Field(..., description="The city name of this company's headquarter location, converted to all lower cased. None if not found.")
    headquarter_state: Union[str, None] = Field(..., description="The state name of this company's headquarter location, converted to all lower cased. None if not found.")
    headquarter_country: Union[str, None] = Field(..., description="The country name of this company's headquarter location, converted to all lower cased. None if not found.")
    description: str = Field(..., description="A short description of this company's product offerings, around 100 words.")

    def __str__(self):
        return pprint.pformat(self.__dict__)