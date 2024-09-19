from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from dashboard.forms import MemberForm, SecretQuestionForm
from dashboard.models import Member


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


class TemplateView(TemplateView):
    template_name = "dashboard/template.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/profile.html"


class LoginView(FormView):
    template_name = "dashboard/login.html"
    form_class = MemberForm
    success_url = reverse_lazy("question")

    def dispatch(self, request, *args, **kwargs):

        # Flush the current identified user
        if "identified_user_id" in request.session:
            del request.session["identified_user_id"]

        if request.user.is_authenticated:
            return redirect("profile")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            user = Member.objects.filter(username=form.cleaned_data["username"]).first()
            if not user:
                messages.error(request, "Member does not exist")
                return redirect("login")

            # Identify the user and redirect him to the
            request.session["identified_user_id"] = str(user.id)
            return redirect("question")

        return super().post(request, *args, **kwargs)


class SecretQuestionView(FormView):
    template_name = "dashboard/question.html"
    form_class = SecretQuestionForm
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super(SecretQuestionView, self).get_context_data(**kwargs)
        context["member"] = Member.objects.filter(id=self.request.session["identified_user_id"]).first()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")

        if not "identified_user_id" in request.session:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            user = Member.objects.filter(
                id=request.session["identified_user_id"],
                answer=form.cleaned_data["answer"].lower(),
            ).first()
            if not user:
                messages.error(request, "Bad answer")
                del request.session["identified_user_id"]
                return redirect("login")

            # Authenticate the user
            login(request, user)
            return redirect("profile")

        return super().post(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('login')
