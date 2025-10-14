import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


def ensure_notification_pdf(notification):
    """
    Создает PDF письмо-напоминание об оплате аренды.
    Возвращает полный путь к PDF-файлу.
    """
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    file_path = os.path.join(pdf_dir, f"notification_{notification.id}.pdf")

    # ✅ Регистрируем шрифт с поддержкой кириллицы
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

    # Настройки документа
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
    )

    # Стили
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CustomTitle",
            fontName="STSong-Light",
            fontSize=18,
            leading=22,
            alignment=1,
            textColor=colors.darkblue,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="STSong-Light",
            fontSize=12,
            leading=16,
            spaceAfter=10,
        )
    )

    elements = []

    # ✅ Логотип
    logo_path = os.path.join(settings.MEDIA_ROOT, "logo.png")
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=4 * cm, height=4 * cm))
        elements.append(Spacer(1, 0.4 * cm))

    # ✅ Заголовок
    elements.append(Paragraph("Напоминание об оплате", styles["CustomTitle"]))

    # Горизонтальная линия
    elements.append(Spacer(1, 0.2 * cm))
    line_table = Table([[""]], colWidths=[16 * cm])
    line_table.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1, colors.grey)]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.8 * cm))

    # ✅ Основной текст письма
    text = f"""
    <b>Арендатор:</b> {notification.tenant.name}<br/>
    <b>Тип уведомления:</b> {notification.get_notification_type_display()}<br/>
    <b>Дата:</b> {notification.sent_date.strftime('%d.%m.%Y %H:%M')}<br/><br/>
    <b>Сообщение:</b><br/>{notification.message or 'Текст уведомления отсутствует.'}
    """
    elements.append(Paragraph(text, styles["Body"]))
    elements.append(Spacer(1, 1.5 * cm))

    # ✅ Подпись
    elements.append(Paragraph("<b>Директор:</b> Иванов И.И.", styles["Body"]))
    elements.append(Paragraph("<b>Управляющая компания</b>", styles["Body"]))

    # ✅ Функция отрисовки рамки
    def draw_border(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.lightgrey)
        canvas.setLineWidth(1)
        canvas.rect(1.5 * cm, 1.5 * cm, A4[0] - 3 * cm, A4[1] - 3 * cm)
        canvas.restoreState()

    # Создаем PDF
    doc.build(elements, onFirstPage=draw_border, onLaterPages=draw_border)

    # Обновляем путь в базе
    relative_path = f"pdfs/notification_{notification.id}.pdf"
    notification.pdf_file.name = relative_path
    notification.save(update_fields=["pdf_file"])

    print(f"[PDF CREATED] {file_path}")
    return file_path
