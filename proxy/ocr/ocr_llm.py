import os
import dspy
import sys
import asyncio

sys.path.append(".")
sys.path.append("./data/")
from rich.console import Console
from rich.markdown import Markdown
from rich.console import Console
from rich.markdown import Markdown
from dataclasses import dataclass
from pydantic import BaseModel
import dspy

console = Console()


@dataclass
class LLMConfig:
    promt_file = "system_prompt.txt"
    llm = "ollama_chat/deepseek-r1:1.5b"
    api = "http://ollama:11434"


class Date(BaseModel):
    year: int
    month: int
    day: int
    hour: int


class InvoiceData(dspy.Signature):
    """You are invoice extractor service, by given the filecontent you extract the required fields"""

    invoiceNumber: str = dspy.OutputField(desc="Invoice number")
    invoiceDate: Date = dspy.OutputField(desc="Date when invoice was issued")
    seller: str = dspy.OutputField(desc="The name of the seller")
    sellerRegNumber: int = dspy.OutputField(desc="Seller registration number")
    buyer: str = dspy.OutputField(desc="The name of buyer")
    buyerRegNumber: int = dspy.OutputField(desc="Buyer registration number")
    paymentDeadline: Date = dspy.OutputField(
        desc="Deadline of payment mantioned in the invoice"
    )
    netPrice: float = dspy.OutputField(desc="Net price")
    vat: float = dspy.OutputField(desc="VAT price")
    totalPrice: float = dspy.OutputField(desc="Total price")
    currency: str = dspy.OutputField(desc="Currency")
    summary: str = dspy.OutputField(desc="Summary of the invoice file")
    filecontent: str = dspy.InputField(desc="The content of the invoice file")


class OCRLLM:
    def __init__(self, config):
        self.config = config
        self.llm = dspy.LM(
            model=config.llm,
            api_base=config.api,
            api_key="",
            temperature=0.9,
        )
        dspy.configure(lm=self.llm)
        self.predict = dspy.ChainOfThought(InvoiceData)
        self.validator = dspy.ChainOfThought(
            "extracted_data, parsed_data -> answer: bool"
        )

    def _get_prompt(self):
        with open(self.config.prompt_file) as f:
            self.prompt = f.read()

    def extract_text(self, filecontent):
        outputs = self.predict(filecontent=str(filecontent))
        return outputs
