from rest_framework import serializers

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


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "full_name")


class CrewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
        )


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "full_path")


class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance", "full_path")


class RouteFlightSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_per_row",
            "airplane_type",
        )


class AirplaneDetailSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_per_row", "airplane_type", "capacity")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type", "capacity")


class AirplaneFlightSerializer(serializers.ModelSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airplane
        fields = ("name", "capacity", "airplane_type")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
        )


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.CharField(
        source="route.full_path",
        read_only=True,
    )
    airplane = serializers.CharField(
        source="airplane.name",
        read_only=True,
    )
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    tickets_left = serializers.IntegerField(read_only=True)

    departure_time = serializers.DateTimeField(format="%B-%d, %Y %H:%M")
    arrival_time = serializers.DateTimeField(format="%B-%d, %Y %H:%M")

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
            "tickets_left",
        )


class FlightDetailSerializer(FlightListSerializer):
    route = RouteFlightSerializer(read_only=True)
    airplane = AirplaneFlightSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    tickets_left = serializers.IntegerField(read_only=True)


class FlightTicketSerializer(serializers.ModelSerializer):
    route = serializers.CharField(
        source="route.full_path",
        read_only=True,
    )
    departure_time = serializers.DateTimeField(format="%B-%d, %Y %H:%M")
    arrival_time = serializers.DateTimeField(format="%B-%d, %Y %H:%M")

    class Meta:
        model = Flight
        fields = (
            "route",
            "departure_time",
            "arrival_time",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightTicketSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)
    created_at = serializers.DateTimeField(format="%B-%d, %Y %H:%M")

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        Ticket.objects.bulk_create([Ticket(order=order, **td) for td in tickets_data])
        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
