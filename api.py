import os
import json
from openai import OpenAI
from datetime import datetime

from llm_model import LLMApi
from utils import crawl
from match import MatchList, Match
from company import Company
from firms_db import firms
from constants import OPENAI_API_KEY

class CoveAI:
    """AI agent that generates private equity insights using LLM"""

    def __init__(self, llm_api: str, llm_api_key: str = OPENAI_API_KEY):
        self.llm_api_key = llm_api_key
        if llm_api == LLMApi.OPENAI.value:
            os.environ["OPENAI_API_KEY"] = self.llm_api_key
            self.openai_client = OpenAI()
            self.default_model = "gpt-4o-mini"
        else:
            raise NotImplementedError(f"{llm_api} not supported.")

    def get_company_profile(self, url: str, model: str = None, crawl_depth_limit: int = 5) -> Company:
        """
        Get a company's profile using information from its website using LLM
        :param url: company's website URL
        :param model: LLM model to use
        :param crawl_depth_limit: number of web pages to scrape, starting from and including url
        :return: Company profile object
        """
        model = model if model else self.default_model

        # Crawl company's website
        website_content = crawl(base_url=url, depth_limit=crawl_depth_limit)

        # Create company profile using LLM
        t0 = datetime.now()
        print("Chat begins")
        chat_completion = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "You are a private equity investor trying to learn about a company you are interested in acquiring."},
                {"role": "user", "content": f"Here is the content of the company's website at 'osmo.ai'. {website_content}"},
                {"role": "user", "content": "Do not make up any information if you can not find the answer. Create a new Company object describing this company."}
            ],
            functions=[
                {
                    "name": "createCompanyObject",
                    "parameters": Company.model_json_schema()
                }
            ],
            function_call={"name": "createCompanyObject"},
        )
        print(f"Chat took {(datetime.now() - t0).seconds}s")
        args = json.loads(chat_completion.choices[0].message.function_call.arguments)
        return Company(**args)

    def match_firm(self, company: Company, num_firms: int = 3, reason_word_count: int = 30) -> list[Match]:
        """
        Find private equity firms that would most likely be interested in acquiring the input company.
        :param company: company profile
        :param num_firms: number of private equity firms to match
        :param reason_word_count: approximate word count of the reasons that the LLM model will provide
        :return: list of Matches made
        """
        t0 = datetime.now()
        print("Chat begins")
        chat_completion = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": "You are a private equity investor trying to guess which private equity firm is likely to be interested in acquiring a company."},
                {"role": "user",
                 "content": f"The next message contains relevant information about this company in the format of a JSON string. Add it to your context."},
                {"role": "user", "content": str(company.model_dump_json())},
                {"role": "user",
                 "content": f"The next message contains a list of 10 private equity funds that you should consider, each in the format of a JSON string. Specifically, " +
                            "industry is a list of top industries that this firm focuses on, in the order from most preferred to least preferred." +
                            "revenue means the approximate minimum yearly revenue in USD of companies that this firm prefers to acquire, converted to integer." +
                            "valuation means the approximate valuation in USD of companies that this firm prefers to acquire, converted to integer." +
                            "num_employees means the approximate minimum number of employees of companies that this firm prefers to acquire, converted to integer." +
                            "geography is a list of geographical areas that this firm focuses on." +
                            "distressed means whether this firm is interested in acquiring distressed companies."},
                {"role": "user", "content": str([firm.json() for firm in firms])},
                {"role": "user",
                 "content": f"Give me the top {num_firms} private equity firms from this list that are most likely to be interested in acquiring the company."+
                            f"For each choice, you should also provide a reason for why this firm would be interested in acquiring the company in around {reason_word_count} words that takes into consideration characteristics of this company."+
                            f"For each choice, you should also provide a reason for why this firm would be not interested in acquiring the company in around {reason_word_count} words that takes into consideration characteristics of this company." +
                            f"Based on these reasons, you should also give this match a score with an integer from 1 to 10, 10 being the most aligned match." +
                            f"Create a MatchList object from these {num_firms} choices, ordered from best match to worst match."}
            ],
            functions=[
                {
                    "name": "createMatchList",
                    "parameters": MatchList.model_json_schema()
                }
            ],
            function_call={"name": "createMatchList"},
        )
        print(f"Chat took {(datetime.now() - t0).seconds}s")
        args = json.loads(chat_completion.choices[0].message.function_call.arguments)
        return MatchList(**args).matches
