import os
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from .models import Tenant, Notification, Payment
from .utils.pdf_generator import ensure_notification_pdf


def tenants_list(request):
    tenants = Tenant.objects.all()
    return render(request, "debts/tenants_list.html", {"tenants": tenants})


def tenant_detail(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    payments = Payment.objects.filter(tenant=tenant)
    notifications = Notification.objects.filter(tenant=tenant).order_by("-sent_date")
    return render(
        request,
        "debts/tenant_detail.html",
        {
            "tenant": tenant,
            "payments": payments,
            "notifications": notifications,
        },
    )


def notification_pdf_view(request, pk):
    """Открывает PDF уведомления (создает, если его нет)."""
    try:
        notification = Notification.objects.get(id=pk)
    except Notification.DoesNotExist:
        raise Http404("Уведомление не найдено")

    # ✅ Безопасно получаем путь
    pdf_path = notification.pdf_file.path if notification.pdf_file else None

    # ✅ Если файла нет или он не существует — генерируем заново
    if not pdf_path or not os.path.exists(pdf_path):
        pdf_path = ensure_notification_pdf(notification)
        notification.refresh_from_db()  # обновляем объект, чтобы получить путь из БД

    # ✅ Проверяем, что теперь путь есть и файл существует
    if not pdf_path or not os.path.exists(pdf_path):
        raise Http404("PDF-файл не удалось создать")

    # ✅ Возвращаем PDF пользователю
    return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
