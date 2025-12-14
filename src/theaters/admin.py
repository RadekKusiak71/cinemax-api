from django.contrib import admin
from django.db.models import Count
from django.http import HttpRequest

from .models import Seat, TheaterHall


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = ('row', 'number')
    ordering = ('row', 'number')
    show_change_link = True
    autocomplete_fields: list[str] = []

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'theater_hall', 'row', 'number', 'seat_label')
    list_select_related = ('theater_hall',)
    list_filter = ('theater_hall', 'row')
    search_fields = ('theater_hall__number',)
    ordering = ('theater_hall__number', 'row', 'number')
    list_per_page = 50
    autocomplete_fields = ('theater_hall',)

    @admin.display(description='Label')
    def seat_label(self, obj: Seat) -> str:
        return f'Row {obj.row} • Seat {obj.number}'

@admin.register(TheaterHall)
class TheaterHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'seats_count', 'rows_count',)
    search_fields = ('number',)
    ordering = ('number',)
    inlines = (SeatInline,)
    list_per_page = 50

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        return qs.annotate(seats_count=Count('seats', distinct=True))

    @admin.display(description='Seats', ordering='seats_count')
    def seats_count(self, obj: TheaterHall) -> int:
        return getattr(obj, 'seats_count', obj.seats.count())

    @admin.display(description='Rows')
    def rows_count(self, obj: TheaterHall) -> int:
        return obj.seats.values('row').distinct().count()
