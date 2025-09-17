from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket
)

User = get_user_model()


class TicketAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", "user@user.com", "1234!@#$")
        self.admin = User.objects.create_superuser("admin", "admin@admin.com", "1234!@#$")

        self.airport1 = Airport.objects.create(name="Boryspil", closest_big_city="Kyiv")
        self.airport2 = Airport.objects.create(name="Lviv", closest_big_city="Lviv")

        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=540)

        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")

        self.airplane = Airplane.objects.create(name="UR-PSA", rows=10, seats_per_row=4, airplane_type=self.airplane_type)

        self.crew = Crew.objects.create(first_name="Vasya", last_name="Pupkin")

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2)
        )
        self.flight.crew.add(self.crew)

        self.base_url = "/api/airport/tickets/"

    def test_list_tickets_user(self):
        order_admin = Order.objects.create(user=self.admin)
        Ticket.objects.create(row=1, seat=1, flight=self.flight, order=order_admin)

        order_user = Order.objects.create(user=self.user)
        ticket_user = Ticket.objects.create(row=1, seat=2, flight=self.flight, order=order_user)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], ticket_user.id)

    def test_list_tickets_admin(self):
        order_admin = Order.objects.create(user=self.admin)
        ticket_admin = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=order_admin)

        order_user = Order.objects.create(user=self.user)
        ticket_user = Ticket.objects.create(row=1, seat=2, flight=self.flight, order=order_user)

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        ids = [t["id"] for t in response.data["results"]]
        self.assertIn(ticket_admin.id, ids)
        self.assertIn(ticket_user.id, ids)

    def test_retrieve_ticket_user(self):
        order_user = Order.objects.create(user=self.user)
        ticket_user = Ticket.objects.create(row=1, seat=2, flight=self.flight, order=order_user)

        order_admin = Order.objects.create(user=self.admin)
        ticket_admin = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=order_admin)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.base_url}{ticket_admin.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
