from django.contrib import admin
from django.urls import include, path

from business_case_approval.rbca import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("home/", views.homepage_view, name="homepage"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
