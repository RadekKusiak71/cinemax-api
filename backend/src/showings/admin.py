# admin.py
from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from showings.models import Showing, ShowingFormat, ShowingVariant


class ShowingInline(admin.TabularInline):
    model = Showing
    extra = 1
    autocomplete_fields = ("theater_hall", "variant")
    fields = ("theater_hall", "start_time", "ticket_price")
    ordering = ("start_time",)


class ShowingInlineForVariant(admin.TabularInline):
    model = Showing
    extra = 1
    autocomplete_fields = ("theater_hall",)
    fields = ("theater_hall", "start_time", "ticket_price")
    ordering = ("start_time",)


@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):
    list_display = (
        "movie_title",
        "hall_number",
        "start_time",
        "end_time",
        "format_name",
        "ticket_price",
    )
    list_filter = (
        "theater_hall",
        "variant__format",
        "variant__dubbing",
        "variant__subtitles",
        "start_time",
    )
    search_fields = (
        "variant__movie__title",
        "theater_hall__number",
    )
    autocomplete_fields = ("theater_hall", "variant")
    list_select_related = (
        "theater_hall",
        "variant",
        "variant__movie",
        "variant__format",
        "variant__dubbing",
        "variant__subtitles",
    )
    ordering = ("-start_time",)

    @admin.display(ordering="variant__movie__title", description="Movie")
    def movie_title(self, obj: Showing):
        return obj.variant.movie.title

    @admin.display(ordering="theater_hall__number", description="Hall")
    def hall_number(self, obj: Showing):
        return obj.theater_hall.number

    @admin.display(ordering="variant__format__name", description="Format")
    def format_name(self, obj: Showing):
        return obj.variant.format.name

    @admin.display(description="End time")
    def end_time(self, obj: Showing):
        return obj.start_time + timedelta(minutes=obj.variant.movie.duration + obj.CLEANUP_BUFFER_MINUTES)


@admin.register(ShowingFormat)
class ShowingFormatAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = []


@admin.register(ShowingVariant)
class ShowingVariantAdmin(admin.ModelAdmin):
    list_display = ("movie", "format", "dubbing", "subtitles", "variant_label")
    list_filter = ("format", "dubbing", "subtitles", "movie")
    search_fields = ("movie__title", "format__name")
    autocomplete_fields = ("movie", "format", "dubbing", "subtitles")
    list_select_related = ("movie", "format", "dubbing", "subtitles", "movie__original_language")
    inlines = [ShowingInlineForVariant]

    @admin.display(description="Label")
    def variant_label(self, obj: ShowingVariant):
        return str(obj)
