from pydantic import BaseModel
import dspy

class Date(BaseModel):
    year: int
    month: int
    day: int
    hour: int

class InvoiceData(dspy.Signature):
    """You are invoice extractor service, by given the filecontent you extract the required fields
    """
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
    # filename:str = dspy.InputField();
    filecontent: str = dspy.InputField(desc="The content of the invoice file")
    #prompt: str = dspy.InputField()
    # error:str = dspy.InputField();
