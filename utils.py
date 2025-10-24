from dataclasses import dataclass


@dataclass
class TypeClass:
    EDOC = "edoc"
    PDF = "pdf"
    HTML = "html"
    IMAGE = "image"
    PDF = "pdf"
    ASCIIDOC = "asciidoc"
    MD = "md"
    CSV = "csv"
    XLSX = "xlsx"
    JSON_DOCLING = "json_docling"
    AUDIO = "audio"


@dataclass
class ModelClass:
    PADDLE = "paddle"
    MISTRAL = "mistral"
    OPENAI = "openai"
    DOCLING = "docling"
    GRANITE = "granite"
    LLAVA = "llava"
