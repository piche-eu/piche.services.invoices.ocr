import os
import base64
import json
import mimetypes
from torch.utils.data import Dataset
from pdf2image import convert_from_path
from PIL import Image

class InvoiceDataset(Dataset):
    def __init__(self, config):
        self.path = config["path"]
        self.files_invoices = os.listdir(self.path+"/pdf/")
        self.files_parsed = os.listdir(self.path+"/json/")
        #Sort the lists:
        self.files_invoices.sort()
        self.files_parsed.sort()
        return

    def __len__(self):
        len = len(self.files)
        return len

    def __getitem__(self, idx):        
        filename = self.files_invoices[idx]
        print(filename)
        images = convert_from_path(self.path + "/pdf/"+filename)[0]
        images.save(self.path + filename + ".png")
        
        if encoded_image:
            result = Image.open(self.path + filename + ".png").convert('RGB')
        else:
            with open(self.path + filename + ".png", "rb") as f:
                image = f.read()
            encoded_image = base64.b64encode(image).decode("utf-8")
            mime_type, _ = mimetypes.guess_type(self.path + filename + ".png")
            result = f"data:{mime_type};base64,{encoded_image}"
        
        #read the json file:
        print(self.files_parsed[idx])
        with open(self.path + "/json/" +self.files_parsed[idx], 'r') as file:
            data = json.load(file)
        
        #find the relevant json and return as target value
        return result, data
    

    