# chatbot_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Cluster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='chat_data/')
    openai_api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    