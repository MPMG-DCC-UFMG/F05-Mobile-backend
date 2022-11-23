from typing import List

from pydantic import BaseModel

from application.inspection.models.pdfPhoto import PdfPhoto


class Inspector(BaseModel):
  name: str
  email: str
  role: str


class InspectionPdfDTO(BaseModel):
  inspection_id: str
  inquiry_number: str
  local: str
  inspection_date: str
  observations: str
  content: List[PdfPhoto]
  inspector: Inspector