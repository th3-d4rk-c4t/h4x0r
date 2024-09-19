from django.views.generic import TemplateView


class OvhView(TemplateView):
    template_name = "ovh/index.html"
