from pydantic import BaseModel


class PdfPhoto(BaseModel):
  image_path: str
  description: str
  coordinates: str