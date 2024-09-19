from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("d4shb04rd-f0r-1337/", include("dashboard.urls")),
    path("", include("ovh.urls")),
]
