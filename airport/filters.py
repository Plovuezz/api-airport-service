import django_filters
from airport.models import Route, Airport, Airplane, Flight, Ticket


class RouteFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(
        field_name="source__closest_big_city", lookup_expr="icontains"
    )
    destination = django_filters.CharFilter(
        field_name="destination__closest_big_city", lookup_expr="icontains"
    )

    class Meta:
        model = Route
        fields = []


class AirportFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    city = django_filters.CharFilter(
        field_name="closest_big_city", lookup_expr="icontains"
    )

    class Meta:
        model = Airport
        fields = []


class AirplaneFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )
    airplane_type = django_filters.CharFilter(
        field_name="airplane_type__name", lookup_expr="icontains"
    )

    class Meta:
        model = Airplane
        fields = []


class FlightFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(
        field_name="route__source__closest_big_city", lookup_expr="icontains"
    )
    destination = django_filters.CharFilter(
        field_name="route__destination__closest_big_city", lookup_expr="icontains"
    )
    airplane = django_filters.CharFilter(
        field_name="airplane__name", lookup_expr="icontains"
    )
    departure_date = django_filters.DateFilter(
        field_name="departure_time", lookup_expr="date"
    )
    departure_range = django_filters.DateFromToRangeFilter(
        field_name="departure_time"
    )
    arrival_date = django_filters.DateFilter(
        field_name="arrival_time", lookup_expr="date"
    )
    arrival_range = django_filters.DateFromToRangeFilter(
        field_name="arrival_time"
    )

    class Meta:
        model = Flight
        fields = []


class TicketFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(
        field_name="flight__route__source__name", lookup_expr="icontains"
    )
    destination = django_filters.CharFilter(
        field_name="flight__route__destination__name", lookup_expr="icontains"
    )


    class Meta:
        model = Ticket
        fields = []
