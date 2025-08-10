from django.contrib import admin
from support.models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('email','subject','status','created_at')
    list_filter = ('status',)
    search_fields = ('subject','email')