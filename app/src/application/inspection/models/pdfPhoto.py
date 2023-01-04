from pydantic import BaseModel


class PdfPhoto(BaseModel):
  image_path: str
  description: str
  latitude: str
  longitude: str