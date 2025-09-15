from threading import settrace

from django.conf import settings
from django.db import models
from django.db.models import CASCADE, ForeignKey


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)


class Route(models.Model):
    source = models.ForeignKey(Airport, related_name="routes_from", on_delete=CASCADE)
    destination = models.ForeignKey(Airport, related_name="routes_to", on_delete=CASCADE)
    distance = models.PositiveIntegerField()


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)


class Airplane(models.Model):
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    airplane_type = models.ForeignKey(AirplaneType, on_delete=CASCADE, related_name="airplanes")


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=CASCADE, related_name="flights")
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="orders")


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(Flight, on_delete=CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=CASCADE, related_name="tickets")
