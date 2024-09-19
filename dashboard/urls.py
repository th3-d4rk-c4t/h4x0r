from django.urls import path

from dashboard import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("question/", views.SecretQuestionView.as_view(), name="question"),
    path("logout/", views.logout_view, name="logout"),
    path("template/", views.TemplateView.as_view(), name="template"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
