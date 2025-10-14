
from django.urls import path
from . import views

urlpatterns = [
    path("", views.tenants_list, name="tenants_list"),
    path("tenants/<int:pk>/", views.tenant_detail, name="tenant_detail"),
    path("notifications/<int:pk>/", views.notification_pdf_view, name="notification_pdf"),
]
