from django.db import models


llm_type = [
    (0, "chatglm3"),
    (1, "gpt3.5")
]

# Create your models here.
class OcrModel(models.Model):
    case_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    pdf_file = models.FileField(upload_to='tmp/pdf/')
    mmd_file = models.FilePathField()
    
    # ocr_model_type = 