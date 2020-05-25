from django import forms
from app.models import BashScript

class BashScriptForm(forms.ModelForm):
    class Meta:
        model = BashScript
        fields=('name','script')
