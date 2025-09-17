from django.contrib import admin

from airport.models import (
    Ticket,
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Route.objects.select_related("destination", "source")


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    pass


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
