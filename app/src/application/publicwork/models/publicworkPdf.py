from typing import List

from pydantic import BaseModel

from application.inspection.models.pdfPhoto import PdfPhoto


class Inspector(BaseModel):
  name: str
  email: str
  role: str


class PdfCollect(BaseModel):
  date: str
  observations: str
  inspector: Inspector  
  photos: List[PdfPhoto]


class PublicWorkPdfDTO(BaseModel):
  name: str
  address: str
  content: List[PdfCollect]