from enum import Enum
from typing import Optional, TypedDict

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


class Category(Enum):
    HOUSING = "Housing"
    TRANSPORTATION = "Transportation"
    FOOD = "Food"
    UTILITIES = "Utilities"
    INSURANCE = "Insurance"
    MEDICAL_HEALTHCARE = "Medical/Healthcare"
    SAVINGS = "Savings"
    DEBT = "Debt"
    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"


class ExpenseResponseModel(BaseModel):
    description: Optional[str] = Field(
        title="Description",
        description="Description of the expense",
        default=None,
    )
    price: Optional[float] = Field(
        title="Price", description="Price of the expense", default=None
    )
    category: Optional[Category] = Field(
        title="Category", description="Category of the expense", default=None
    )


class ExpenseResponseData(TypedDict):
    description: Optional[str]
    price: Optional[float]
    category: Optional[Category]


class IncompleteExpense(Exception):
    pass


class InvalidExpense(Exception):
    pass


class ExpenseJsonOutputParser(JsonOutputParser):
    def __init__(self):
        super().__init__(pydantic_object=ExpenseResponseModel)


class ExpenseParser:
    def __init__(self, model, parser):
        prompt = PromptTemplate(
            template="""
            You are an expense parser.
            You will receive expense queries and parse them into structured data.
            If any of the information is missing or you are not sure about the value, you will return None for that field.
            Do not parse units as prices.
            If the message is not an expense query, return all fields as None.
            {format_instructions}
            User query: "{query}"
            """,
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        self.chain = prompt | model | parser

    def _is_valid(self, res: ExpenseResponseData) -> bool:
        return res["price"] is not None and res["category"] is not None

    def _is_complete(self, res: ExpenseResponseData) -> bool:
        return res["description"] is not None and self._is_valid(res)

    def parse(self, query) -> ExpenseResponseData:
        res: ExpenseResponseData = self.chain.invoke({"query": query})
        if not self._is_complete(res):
            raise IncompleteExpense()
        elif not self._is_valid(res):
            raise InvalidExpense()
        return res
