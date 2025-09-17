from django.db.models import F, Count
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from airport.filters import (
    RouteFilter,
    AirportFilter,
    AirplaneFilter,
    FlightFilter,
    TicketFilter
)
from airport.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket,
)
from airport.serializers import (
    CrewDetailSerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    OrderSerializer,
    TicketSerializer,
    CrewSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneDetailSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightSerializer,
    FlightDetailSerializer,
    TicketListSerializer,
    OrderListSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CrewSerializer
        return CrewDetailSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AirportFilter
    search_fields = ["name", "closest_big_city"]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("destination", "source")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RouteFilter
    search_fields = ["source__name", "destination__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AirplaneFilter
    search_fields = ["name", "airplane_type__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects.select_related(
            "route__source", "route__destination", "airplane"
        )
        .prefetch_related("crew", "tickets")
        .annotate(
            tickets_left=(
                F("airplane__rows") * F("airplane__seats_per_row") - Count("tickets")
            )
        )
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = FlightFilter
    search_fields = [
        "route__source__name",
        "route__destination__name",
        "airplane__name",
    ]

    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_staff:
            return qs
        return qs.filter(departure_time__gt=timezone.now())

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
    Order.objects.select_related("user")
    .prefetch_related(
        "tickets",
        "tickets__flight__route__source",
        "tickets__flight__route__destination",
        "tickets__flight__airplane",
    )
)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = [
        "created_at"
    ]


    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ticket.objects.select_related(
        "flight",
        "flight__route__source",
        "flight__route__destination",
        "flight__airplane"
    )
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TicketFilter
    search_fields = [
        "flight__route__source__name",
        "flight__route__destination__name"
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.request.user.is_staff:
            return qs
        return qs.filter(order__user=self.request.user)
