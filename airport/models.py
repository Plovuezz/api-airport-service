from idlelib.debugobj_r import remote_object_tree_item

from django.conf import settings
from django.db import models
from django.db.models import CASCADE, ForeignKey
from django.db.models.constraints import UniqueConstraint


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return f"Crew member {self.first_name} {self.last_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}, {self.closest_big_city}"


class Route(models.Model):
    source = models.ForeignKey(Airport, related_name="routes_from", on_delete=CASCADE)
    destination = models.ForeignKey(
        Airport, related_name="routes_to", on_delete=CASCADE
    )
    distance = models.PositiveIntegerField()

    @property
    def full_path(self):
        return (
            f"{self.source.name}({self.source.closest_big_city}) - "
            f"{self.destination.name}({self.destination.closest_big_city})"
            f" {self.distance}km."
        )

    class Meta:
        ordering = ("source", "destination")

    def __str__(self):
        return (
            f"{self.source.name}({self.source.closest_big_city}) - "
            f"{self.destination.name}({self.destination.closest_big_city})"
        )


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Airplane(models.Model):
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self):
        return self.rows * self.seats_per_row

    class Meta:
        ordering = ("airplane_type", "rows", "seats_per_row")

    def __str__(self):
        return f"{self.name} {self.airplane_type.name}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=CASCADE, related_name="flights")
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ("-departure_time",)

    def __str__(self):
        return (
            f"{str(self.route)}, "
            f"{self.airplane.name} "
            f"{self.departure_time:%Y-%m-%d %H:%M}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="orders"
    )

    class Meta:
        ordering = ("-created_at",)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=CASCADE, related_name="tickets")

    class Meta:
        constraints = (
            UniqueConstraint(fields=("row", "seat", "flight"), name="unique_ticket"),
        )
        ordering = ("flight", "row", "seat")
