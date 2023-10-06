# chatbot_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Cluster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    txt_file = models.FileField(upload_to='chat_data/')
    # openai_api_key = models.CharField(max_length=100)
    chroma_db_directory = models.CharField(max_length=255)  # Store the directory name (relative path)
    

    def __str__(self):
        return self.name
    
    @property
    def get_absolute_url(self):
        return reverse(f'getAnswer', kwargs={'cluster_id': self.id})
    