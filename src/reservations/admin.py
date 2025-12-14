from django.contrib import admin
from reservations.models import Reservation, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'showing', 'full_price', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'showing__movie__title')
    ordering = ('-created_at',)
    inlines = [TicketInline]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation', 'seat')
    search_fields = ('reservation__id', 'seat__row', 'seat__number')
    ordering = ('id',)


