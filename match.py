from pydantic import BaseModel, Field
import pprint

class Match(BaseModel):
    """Match between a private equity firm and a company"""
    firm_name: str = Field(..., description="Name of the private equity firm.")
    score: int = Field(..., description="On a scale of 1 to 10, 10 being the most aligned match, give this match a score.")
    reason_for: str = Field(..., description="Reason that this private equity firm would be interested in acquiring the company.")
    reason_against: str = Field(..., description="Reason that this private equity firm would not be interested in acquiring the company.")

    def __str__(self):
        return pprint.pformat(self.__dict__)

class MatchList(BaseModel):
    """List of matches between private equity firms and a company"""
    matches: list[Match] = Field(..., description="List of match objects.")