from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, Div, Field, Layout, Submit
from django import forms


class MemberForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})

        self.helper = FormHelper()
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
            "username",
            FormActions(
                HTML(
                    """
                    <a href="{% url 'dashboard' %}" class="btn btn-default">
                    Cancel
                    </a>
                    """
                ),
                Submit("save", "Login"),
                css_class="text-right",
            ),
        )


class SecretQuestionForm(forms.Form):
    answer = forms.CharField(label="Answer", max_length=250)

    def __init__(self, *args, **kwargs):
        super(SecretQuestionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
            "answer",
            FormActions(
                HTML(
                    """
                    <a href="{% url 'login' %}" class="btn btn-default">
                    Cancel
                    </a>
                    """
                ),
                Submit("save", "Submit"),
                css_class="text-right",
            ),
        )
