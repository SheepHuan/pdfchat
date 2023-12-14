from django import forms
from .models import OcrModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class PdfForm(forms.Form):

    class Meta:
        model = OcrModel
        fields = ('pdf_file')
        
        labels = {
            'pdf_file': 'PDF File',  
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['description'].required = False
        self.helper.layout = Layout(
            'pdf_file',   
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )