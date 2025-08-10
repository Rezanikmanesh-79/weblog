# views.py
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from support.forms import TicketForm
from support.models import Ticket

class TicketView(TemplateView):
    template_name = "forms/ticket.html"

    def get(self, request, *args, **kwargs):
        form = TicketForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('blog:post-list')
        return render(request, self.template_name, {'form': form})
