from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def export_pdf(df):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = [Paragraph("Report Task Agile", styles["Title"]), Spacer(1,12)]
    elements.append(Paragraph(f"Totale Task: {len(df)}", styles["Normal"]))
    elements.append(Paragraph(f"Task Completati: {len(df[df['Stato']=='Completato'])}", styles["Normal"]))
    doc.build(elements)
    return buffer.getvalue()

def export_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()
