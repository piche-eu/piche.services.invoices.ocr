import os
from torch.utils.data import Dataset
from pdf2image import convert_from_path
import base64
import mimetypes

class InvoiceDataset(Dataset):
    def __init__(self, config):
        self.path = config["path"]
        self.files = os.listdir(self.path)
        return

    def __len__(self):
        len = len(self.files)
        return len

    def __getitem__(self, idx):
        filename = self.files[idx]
        images = convert_from_path(self.path + filename)[0]
        images.save(self.path + filename + ".png")
        with open(self.path + filename + ".png", "rb") as f:
            image = f.read()
        encoded_image = base64.b64encode(image).decode("utf-8")
        mime_type, _ = mimetypes.guess_type(self.path + filename + ".png")
        base64_url = f"data:{mime_type};base64,{encoded_image}"
        return base64_url

