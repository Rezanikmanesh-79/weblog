from django.forms import ModelForm
from support.models import Ticket

class TicketForm(ModelForm):
    class Meta:
        model=Ticket
        fields=['name','email','phone','subject','message','status']