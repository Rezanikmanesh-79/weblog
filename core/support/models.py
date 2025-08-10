from django.db import models

class Ticket(models.Model):
    class Status(models.TextChoices):
        open="open"
        close='close'
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=11)
    subject=models.CharField(max_length=50)
    message=models.TextField()
    status = models.CharField(max_length=20,choices=Status.choices ,default=Status.open)
    created_at=models.DateTimeField(auto_now_add=True)