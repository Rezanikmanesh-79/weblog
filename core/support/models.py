from django.db import models

class Ticket(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField()
    subject=models.CharField()
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)