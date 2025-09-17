from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status

from airport.models import (
    Order,
    Ticket,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight
)
from rest_framework.test import APITestCase


User = get_user_model()

class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", "user@user.com", "1234!@#$")
        self.admin = User.objects.create_superuser("admin", "admin@admin.com", "1234!@#4")

        self.airport1 = Airport.objects.create(name="Boryspil", closest_big_city="Kyiv")
        self.airport2 = Airport.objects.create(name="Lviv", closest_big_city="Lviv")

        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=540)

        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")

        self.airplane = Airplane.objects.create(name="UR-PSA", rows=10, seats_per_row=4, airplane_type=self.airplane_type)

        self.crew = Crew.objects.create(first_name="Pupkin", last_name="Vasya")

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2)
        )
        self.flight.crew.add(self.crew)

        self.base_url = "/api/airport/orders/"

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "tickets": [
                {"row": 1, "seat": 1, "flight": self.flight.id},
                {"row": 1, "seat": 2, "flight": self.flight.id},
            ]
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_list_orders_regular_user(self):
        order = Order.objects.create(user=self.user)
        Ticket.objects.create(order=order, flight=self.flight, row=1, seat=1)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.base_url)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_orders_staff_user(self):
        user2 = User.objects.create_user("user2", "user2@user2.com", "1234!@#$")
        order1 = Order.objects.create(user=self.user)
        order2 = Order.objects.create(user=user2)
        Ticket.objects.create(order=order1, flight=self.flight, row=1, seat=1)
        Ticket.objects.create(order=order2, flight=self.flight, row=1, seat=2)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)
        self.assertEqual(len(response.data["results"]), 2)
