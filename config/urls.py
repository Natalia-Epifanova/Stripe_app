
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stripe_app/", include("stripe_app.urls", namespace="stripe_app")),
]
