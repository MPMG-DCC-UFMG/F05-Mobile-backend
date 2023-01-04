import math
from datetime import datetime

from application.core import config
from application.inspection.models.inspectionPdf import (InspectionPdfDTO,
                                                         Inspector)
from application.inspection.models.pdfPhoto import PdfPhoto
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from textwrap import wrap

MPMG_logo = ImageReader('../assets/mpmg_pdf_logo.png')

PDF_SIDE_SPACING = 24.45
PDF_TOP_SPACING = 8.10

PDF_SIDE_INITIAL_VALUE = 25
PDF_TOP_INITIAL_VALUE = 100
PDF_BOTTOM_LIMIT = 160

def __mm_to_p(mm):
  return mm / 0.352777


def __draw_template(pdf: Canvas):
  timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
  pdf.setFont("Helvetica-Bold", 14)
  pdf.drawString(__mm_to_p(60), __mm_to_p(250), "Relatório Automático de Vistoria")
  pdf.setFont("Helvetica", 12)
  pdf.drawString(__mm_to_p(30), __mm_to_p(235), f"Software: {config.settings.system_name}")
  pdf.drawString(__mm_to_p(30), __mm_to_p(225), f"Versão: {config.settings.system_version}")
  pdf.drawString(__mm_to_p(30), __mm_to_p(215), f"Relatório gerado em: {timestamp}")


def __draw_header(pdf: Canvas):
  pdf.drawImage(MPMG_logo,__mm_to_p(PDF_SIDE_INITIAL_VALUE), __mm_to_p(265) , width=150, height=60)
  pdf.setFont("Helvetica-Bold", 12)
  pdf.drawString(__mm_to_p(110), __mm_to_p(280) , config.settings.report_institution)
  pdf.drawString(__mm_to_p(110), __mm_to_p(275), config.settings.report_department)
  pdf.drawString(__mm_to_p(110), __mm_to_p(270), config.settings.report_section)
  pdf.setFont("Helvetica", 12)


def __draw_footer(pdf: Canvas):
  page_num = pdf.getPageNumber()
  pdf.setFont("Helvetica-Bold", 8)
  pdf.drawString(__mm_to_p(160), __mm_to_p(21), f'Página {page_num}')
  pdf.line(__mm_to_p(20), __mm_to_p(20), __mm_to_p(180), __mm_to_p(20))
  pdf.setFont("Helvetica", 9)
  pdf.drawString(__mm_to_p(45), __mm_to_p(15), config.settings.report_address)
  pdf.drawString(__mm_to_p(70), __mm_to_p(10), config.settings.report_contact)
  pdf.setFont("Helvetica-Bold", 9)
  pdf.drawString(__mm_to_p(148), __mm_to_p(10), config.settings.report_website)

  link_rect = (__mm_to_p(148), __mm_to_p(10), __mm_to_p(148), __mm_to_p(10))
  pdf.linkURL(f'http://{config.settings.report_website}', rect=link_rect, relative=1)
  pdf.setFont("Helvetica", 12)


def __draw_content(pdf: Canvas, position: tuple, content: PdfPhoto, index: int):
  width = 400
  height = 200
  x, y = position
  image_path = getattr(content, 'image_path')
  image = ImageReader(image_path)
  end_point_x = x
  end_point_y = y - 40
  latitude = getattr(content, 'latitude')
  longitude = getattr(content, 'longitude')
  description = getattr(content, 'description') if getattr(content, 'description') is not None else "Não há descrição"

  pdf.setFont("Helvetica", 9)
  pdf.rect(x, y, width, height)
  pdf.drawImage(image, x, y, width, height)
  pdf.linkURL(f'http://0.0.0.0:8000/images/{image_path}', rect=(x, y, width+x, height+y), relative=1)
  pdf.rect(end_point_x, end_point_y, width, height/5)
  pdf.drawString(x + 4, end_point_y + 6, f"Coordenadas geográficas: {__convert_coordinates_to_DMS(latitude, longitude)}")
  pdf.drawString(x + 4, end_point_y + 28, f"Foto {index}: {description}")

  pdf.drawString(x + 250, end_point_y + 6, '(ver no mapa)')
  link_rect = (x + 250, end_point_y + 4, (x+250) + 55, (end_point_y + 6) + 10)
  pdf.linkURL(f'https://maps.google.com/?q={latitude},{longitude}&z=15', rect=link_rect, relative=1)

  pdf.setFont("Helvetica", 12)

  return end_point_x, end_point_y - 215


def __draw_comments(pdf: Canvas, observations: str, inspector: Inspector):
  pdf.showPage()
  __draw_header(pdf)
  __draw_footer(pdf)
  pdf.setFont("Helvetica", 12)
  pdf.drawString(__mm_to_p(30), __mm_to_p(235), 'Observações:')

  # Handle multi-linetext
  textobject = pdf.beginText()
  textobject.setTextOrigin(__mm_to_p(30), __mm_to_p(220))
  observations_with_line_breaks = "\n".join(wrap(observations, 80)) # 80 is line width
  textobject.textLines(observations_with_line_breaks)
  pdf.drawText(textobject)

  pdf.line(__mm_to_p(50), __mm_to_p(140), __mm_to_p(150), __mm_to_p(140))
  pdf.drawString(__mm_to_p(70), __mm_to_p(135), f"{getattr(inspector, 'name')} - {getattr(inspector, 'email')}")
  pdf.drawString(__mm_to_p(70), __mm_to_p(130), f"{getattr(inspector, 'role')}")


def __getDMS(value: str):
  value =  abs(float(value))
  degree = math.floor(value)
  minutes = math.floor((value - degree) * 60)
  seconds = round((value - degree - minutes / 60) * 3600 * 1000) / 1000

  return f"{degree}º{minutes}'{seconds}\""


def __convert_coordinates_to_DMS(lat: str, lng: str):
  finalLat = __getDMS(lat)
  finalLat += 'N' if float(lat) >= 0 else 'S'
  finalLng = __getDMS(lng)
  finalLng += 'L' if float(lat) >= 0 else 'O'

  return finalLat + ", " + finalLng


def generate_pdf_by_flag(data: InspectionPdfDTO):
  pdf = Canvas(f"../reports/relatorio-vistoria-{getattr(data, 'inquiry_number')}.pdf", pagesize=A4)
  pdf.setAuthor("Equipe F05")
  pdf.setTitle(f"Relatório Automático - Vistoria {getattr(data, 'inquiry_number')}")
  __draw_header(pdf)
  __draw_footer(pdf)
  __draw_template(pdf)

  pdf.setFont("Helvetica-Bold", 14)
  pdf.drawString(__mm_to_p(90), __mm_to_p(200), f"Vistoria n° {getattr(data, 'inquiry_number')}")
  pdf.setFont("Helvetica", 12)

  pdf.drawString(__mm_to_p(30), __mm_to_p(185), f"Local: {getattr(data, 'local')}")
  pdf.drawString(__mm_to_p(30), __mm_to_p(175), f"Data da Vistoria: {getattr(data, 'inspection_date')}")
  entry_point = (__mm_to_p(30), __mm_to_p(90))
  end_point = (0, 0)

  for index, content in enumerate(getattr(data, 'content')):
    if end_point[1] <= PDF_BOTTOM_LIMIT and end_point[1] != 0: # Reset axis on new page
      pdf.showPage()
      __draw_header(pdf)
      __draw_footer(pdf)
      entry_point = (__mm_to_p(30), __mm_to_p(170))
      end_point = __draw_content(pdf, entry_point, content, index+1)
      entry_point = end_point
    else:
      end_point = __draw_content(pdf, entry_point, content, index+1)
      entry_point = end_point

  __draw_comments(pdf, getattr(data, 'observations'), getattr(data, 'inspector'))
  pdf.save()

  return f"../reports/relatorio-vistoria-{getattr(data, 'inquiry_number')}.pdf"
