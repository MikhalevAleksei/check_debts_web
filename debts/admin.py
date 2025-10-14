
from django.contrib import admin
from .models import Contract, Tenant, Payment, Notification

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("number", "date")

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "contract", "monthly_rent", "payment_day", "has_debt")
    list_filter = ("contract",)
    search_fields = ("name", "email", "phone")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("tenant", "amount", "payment_date", "period_start", "period_end", "is_paid")
    list_filter = ("is_paid", "payment_date")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("tenant", "notification_type", "sent_date", "pdf_file")
    list_filter = ("notification_type", "sent_date")
