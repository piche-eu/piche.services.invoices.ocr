import os
import dspy
import pydantic
import sys
sys.path.append("./data/")
import dataset
from dataset import InvoiceDataset
#read the config file:

#prompt_file = "/Users/leonid/Desktop/HotCode/piche.invoice.ocr/prompt.txt"
#with open(prompt_file) as f:
#    prompt = f.read()
    
def get_parsed_text(i):
    parsed_text_file = f"/Users/leonid/Desktop/HotCode/piche.invoice.ocr/data/dataset/markdown/invoice_{i}.pdf.md"
    with open(parsed_text_file) as f:
        text = f.read()
    return text

#Add the structured output:
class Date(pydantic.BaseModel):
    year:int
    month:int
    day:int
    
class Address(pydantic.BaseModel):
    adreess:str
    
class Invoice(pydantic.BaseModel):
    invoice_id: int
    date: Date
    seller_name:str
    buyer_name:str

class Seller(pydantic.BaseModel):
    seller_name: str
    address: str
    
class Buyer(pydantic.BaseModel):
    buyer_name: str
    


ollama_model = dspy.LM(model="ollama_chat/deepseek-r1:1.5b",
                                #model_type='text',
                                #max_tokens=300,
                                api_base="http://localhost:11434", 
                                api_key=''
                       )
                                #temperature=0.9,
                                #top_p=0.8,
                                #frequency_penalty=1.17, 
                                #top_k=40)
dspy.configure(lm=ollama_model)
#predict = dspy.Predict(Invoice)

markdown = dspy.Predict(
        dspy.Signature("invoice -> md:dict[str,str]"),
        instructions="Convert markdown to the key-value markdown"
        )

invoice_number = dspy.Predict(
    dspy.Signature(
        "invoice -> invoice_number: str",
        instructions="Extract the invoice number from the given text, usually it's possible to find it in the right upper corner near the date of the invoice, usually it is start with the Nr or # and contain only numbers, please don't confuse it with date or currency. Please provide several answers",
    )
)

buyer_information = dspy.Predict(
    dspy.Signature(
        "invoice -> buyer_information: str",
        instructions="Extract the name of receiver/buyer of invoice from the given text",
    )
)

#Test the invoice extaction:
base_path = os.path.dirname(dataset.__file__)
config = {"path": f"{base_path}/dataset/", "encode_image": True}
invoice_dataset = InvoiceDataset(config)
for data in iter(invoice_dataset):
    image, text = data
    #if i==8:continue
    text = get_parsed_text(i)
    invoice = f"{text}"
    print("Convert to markdown k-v:", markdown(invoice=incoive).md)
    #print(f"Invoice number {i}:", invoice_number(invoice=invoice).invoice_number)
    #print(buyer_information(invoice=invoice).buyer_information)
    
#print(ollama_model(f"Please extract the language of the invoice provided as markdown text:\n {text}"))
#print(ollama_model(f"Please extract the year of the invoice provided as markdown text:\n {text}"))
#print(ollama_model(f"Please extract the invoice number of the invoice provided as markdown text:\n {text}"))
#print(ollama_model(f"Please extract the seller information of the invoice of the invoice provided as markdown text:\n {text}"))
#print(ollama_model(f"Please extract the  buyer infrormation the invoice provided as markdown text:\n {text}"))
#print(ollama_model(f"Based on provided text:\n {text}, please return in the following format:\n {format}"))

