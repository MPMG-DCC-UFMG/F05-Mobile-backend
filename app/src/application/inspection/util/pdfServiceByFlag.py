from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from application.inspection.models.inspectionPdf import InspectionPdfDTO, Inspector
from application.inspection.models.pdfPhoto import PdfPhoto

MPMG_logo = ImageReader('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAh1FmzGdI-yOVfQFas-ZPtLdNMRjky0lVlhxPed8C&s')

PDF_SIDE_SPACING = 24.45
PDF_TOP_SPACING = 8.10

PDF_SIDE_INITIAL_VALUE = 25
PDF_TOP_INITIAL_VALUE = 100
PDF_BOTTOM_LIMIT = 160

def __mm_to_p(mm):
  return mm / 0.352777

def __draw_header(pdf: canvas.Canvas):
  pdf.drawImage(MPMG_logo,__mm_to_p(PDF_SIDE_INITIAL_VALUE), __mm_to_p(265) , width=150, height=60)
  pdf.setFont("Helvetica-Bold", 12)
  pdf.drawString(__mm_to_p(110), __mm_to_p(280) , '   Procuradoria-Geral de Justiça')
  pdf.drawString(__mm_to_p(110), __mm_to_p(275), 'Centro de Apoio Técnico - CEAT')
  pdf.drawString(__mm_to_p(110), __mm_to_p(270), '        Setor de Engenharia')
  pdf.setFont("Helvetica", 12)

def __draw_footer(pdf: canvas.Canvas):
  page_num = pdf.getPageNumber()
  pdf.setFont("Helvetica-Bold", 8)
  pdf.drawString(__mm_to_p(160), __mm_to_p(21), f'Página {page_num}')
  pdf.line(__mm_to_p(20), __mm_to_p(20), __mm_to_p(180), __mm_to_p(20))
  pdf.setFont("Helvetica", 9)
  pdf.drawString(__mm_to_p(45), __mm_to_p(15), 'Avenida Álvares Cabral, 1690. Bairro Santo Agostinho. Belo Horizonte/MG. CEP: 30170-008')
  pdf.drawString(__mm_to_p(70), __mm_to_p(10), 'Telefone: (31) 3330-8283. E-mail: ceat@mpmg.mp.br')
  pdf.setFont("Helvetica-Bold", 9)
  pdf.drawString(__mm_to_p(148), __mm_to_p(10), 'www.mpmg.mp.br')
  pdf.setFont("Helvetica", 12)

#TO-DO: clickabe see on map with coordinates
def __draw_content(pdf: canvas.Canvas, position: tuple, content: PdfPhoto):
  width = 400
  height = 200
  x, y = position
  image = ImageReader(getattr(content, 'image_path'))
  end_point_x = x
  end_point_y = y - 40
  latitude = getattr(content, 'latitude')
  longitude = getattr(content, 'longitude')

  pdf.setFont("Helvetica", 9)
  pdf.rect(x, y, width, height)
  pdf.drawImage(image, x, y, width, height)
  pdf.rect(end_point_x, end_point_y, width, height/5)
  pdf.drawString(x + 4, end_point_y + 6, f"Descrição: {getattr(content, 'description')}")
  pdf.drawString(x + 4, end_point_y + 28, f"Coordenadas geográficas: {latitude}, {longitude}")
  pdf.drawString(x + 220, end_point_y + 28, "(ver no mapa)")

  pdf.setFont("Helvetica", 12)

  return end_point_x, end_point_y - 215

def __draw_comments(pdf: canvas.Canvas, inspector: Inspector):
  pdf.showPage()
  __draw_header(pdf)
  __draw_footer(pdf)
  pdf.setFont("Helvetica", 12)
  pdf.drawString(__mm_to_p(30), __mm_to_p(235), 'Observações:')

  spacing = 0 # spacing between lines
  for _ in range(10):
    pdf.line(__mm_to_p(30), __mm_to_p(220 - spacing), __mm_to_p(180), __mm_to_p(220 - spacing))
    spacing += 5

  pdf.line(__mm_to_p(50), __mm_to_p(140), __mm_to_p(150), __mm_to_p(140))
  pdf.drawString(__mm_to_p(70), __mm_to_p(135), f"{getattr(inspector, 'name')}")
  pdf.drawString(__mm_to_p(70), __mm_to_p(130), f"{getattr(inspector, 'role')}")


def generate_pdf_by_flag(data: InspectionPdfDTO):
  pdf = canvas.Canvas(f"../reports/relatorio-vistoria-{getattr(data, 'inspection_id')}.pdf", pagesize=A4)
  pdf.setAuthor("Equipe F05")
  pdf.setTitle(f"Relatório da Vistoria {getattr(data, 'inspection_id')}")
  __draw_header(pdf)
  __draw_footer(pdf)

  pdf.setFont("Helvetica-Bold", 14)
  pdf.drawString(__mm_to_p(70), __mm_to_p(250), "Relatório de Vistoria")
  pdf.setFont("Helvetica", 12)

  pdf.drawString(__mm_to_p(30), __mm_to_p(235), f"Local: {getattr(data, 'local')}")
  pdf.drawString(__mm_to_p(30), __mm_to_p(225), f"Data da Vistoria: {getattr(data, 'inspection_date')}")
  entry_point = (__mm_to_p(30), __mm_to_p(150))
  end_point = (0, 0)

  for content in getattr(data, 'content'):
    if end_point[1] <= PDF_BOTTOM_LIMIT and end_point[1] != 0: # Reset axis on new page
      pdf.showPage()
      __draw_header(pdf)
      __draw_footer(pdf)
      entry_point = (__mm_to_p(30), __mm_to_p(170))
      end_point = __draw_content(pdf, entry_point, content)
      entry_point = end_point
    else:
      end_point = __draw_content(pdf, entry_point, content)
      entry_point = end_point

  __draw_comments(pdf, getattr(data, 'inspector'))
  pdf.save()

  return f"../reports/relatorio-vistoria-{getattr(data, 'inspection_id')}.pdf"
