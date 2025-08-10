from django.urls import path
from support.views import TicketView
app_name='support'

urlpatterns = [
    path('ticket/',TicketView.as_view(),name='ticket')
]
