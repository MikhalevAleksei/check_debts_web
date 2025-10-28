from django.contrib import admin
from django.urls import path
from debts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.tenants_list, name="tenants_list"),
    path("tenant/<int:pk>/", views.tenant_detail, name="tenant_detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "debts" / "static")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
