from __future__ import annotations
from typing import List
from fastapi import UploadFile
from pypdf import PdfReader
from docx import Document
import io


async def extract_text_from_file(file: UploadFile) -> str:
    data = await file.read()
    filename = file.filename or ""
    if filename.lower().endswith(".pdf"):
        return _read_pdf(data)
    if filename.lower().endswith(".docx"):
        return _read_docx(data)
    # plain text fallback
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _read_pdf(data: bytes) -> str:
    buf = io.BytesIO(data)
    reader = PdfReader(buf)
    texts: List[str] = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


def _read_docx(data: bytes) -> str:
    buf = io.BytesIO(data)
    doc = Document(buf)
    return "\n".join(p.text for p in doc.paragraphs)


_COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "react", "node", "fastapi", "django",
    "flask", "aws", "gcp", "azure", "docker", "kubernetes", "sql", "postgresql", "mongodb",
    "redis", "graphql", "rest", "microservices", "ci", "cd", "terraform", "ansible",
}


def extract_skills_simple(text: str) -> List[str]:
    tokens = set(t.lower() for t in ''.join(c.lower() if c.isalnum() else ' ' for c in text).split())
    return sorted(s for s in _COMMON_SKILLS if s in tokens)
