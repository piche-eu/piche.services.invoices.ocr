# Piche OCR

The piche OCR system aims to automatize the invoice document parsing and understanding 
[piche.invoice.ocr](https://github.com/piche-eu/piche.services.invoices.ocr).

## Benchmark Results:

| OCR |  Accuracy (n_parsed_doct/n_total_docs)/ExtractedWordsRate | Efficiency |
| :--- | :---: | ---: |
| PaddleOCR | 100 | 2e-6s/it |
| OpenaAI | 100 |  |
| MistralOCR|100 |  |
|Docling ||127s/it | 
|LLAVA| 50%|69s/it |

## Project layout

    mkdocs.yml    # The configuration file.
    requirements.txt
    tests/ The folder with tests
        test_rabbit_mq.py #Test the rabbit_mq invoice streamer
        test_dataset.py # Test the torch.Dataset work
        test_ocr.py 
        test_llm.py
    logger/
    finetuning/
    data/
        InvoiceDataset #The dataset wrapper for ocr evaluation
    metrics/
        metrics.py #The collection of metrics 
    experiment/ #Folder with different ocr-engines experiments
    
    proxy/ #Proxy server 
    docs/
        index.md  # The documentation homepage.

## Quick Run:
```
git clone https://github.com/piche-eu/piche.services.invoices.ocr
cd ./piche.invoice.ocr/
pip3 install -r requirements.txt
gradio ui.py
```
## Reproduce the experiments:

