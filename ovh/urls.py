from django.urls import path

from ovh import views

urlpatterns = [
    path("", views.OvhView.as_view(), name="ovh"),
]
