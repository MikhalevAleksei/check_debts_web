
from django.db import models
from django.utils import timezone

class Contract(models.Model):
    number = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"{self.number} от {self.date:%d.%m.%Y}"

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name="tenants")
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    payment_day = models.PositiveIntegerField(help_text="День месяца оплаты")

    def __str__(self):
        return self.name

    @property
    def has_debt(self) -> bool:
        return self.payment_set.filter(is_paid=False).exists()

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        status = "оплачено" if self.is_paid else "долг"
        return f"{self.tenant.name}: {self.amount} руб., {self.payment_date:%d.%m.%Y} ({status})"

class Notification(models.Model):
    TYPE_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("claim", "Досудебная претензия"),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    sent_date = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    pdf_file = models.FileField(upload_to="pdfs/", blank=True, null=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} для {self.tenant.name} от {self.sent_date:%d.%m.%Y}"
