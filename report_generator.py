from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from database import session, Message
from datetime import datetime

def generate_user_dossier(username, output_path="dossier.pdf"):
    messages = session.query(Message).filter(Message.username == username).order_by(Message.timestamp).all()
    
    if not messages:
        print(f"No hay mensajes registrados para el usuario '{username}'")
        return

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    def draw_header(title):
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(2 * cm, y, title)

    draw_header(f"Dossier de Usuario: @{username}")
    y -= 1.2 * cm

    first = messages[0]
    last = messages[-1]
    counts = {"safe": 0, "suspicious": 0, "threat": 0, "unknown": 0}
    for m in messages:
        counts[m.evaluation] = counts.get(m.evaluation, 0) + 1

    # Datos generales
    c.setFont("Helvetica", 11)
    general_info = [
        f"User ID: {first.user_id}",
        f"Nombre de usuario: @{username}",
        f"Primera actividad: {first.timestamp.strftime('%Y-%m-%d %H:%M')}",
        f"Última actividad: {last.timestamp.strftime('%Y-%m-%d %H:%M')}",
        f"Total de mensajes: {len(messages)}",
        f"Clasificación de riesgo:",
        f"  - SAFE: {counts['safe']}",
        f"  - SUSPICIOUS: {counts['suspicious']}",
        f"  - THREAT: {counts['threat']}",
        f"  - UNKNOWN: {counts['unknown']}",
    ]
    for line in general_info:
        c.drawString(2 * cm, y, line)
        y -= 0.6 * cm

    y -= 0.8 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Mensajes Analizados:")
    y -= 0.8 * cm
    c.setFont("Helvetica", 10)

    for msg in messages:
        date_str = msg.timestamp.strftime('%Y-%m-%d %H:%M')
        preview = msg.message.replace("\n", " ").strip()
        preview = preview if len(preview) <= 140 else preview[:140] + "..."
        line = f"[{date_str}] ({msg.evaluation.upper()}) {preview}"
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
        c.drawString(2 * cm, y, line)
        y -= 0.5 * cm

    c.save()
    print(f"Dossier exportado como '{output_path}'")
