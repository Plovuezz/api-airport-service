from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from airport.models import Airport, Route, AirplaneType, Airplane, Crew, Flight

User = get_user_model()

class FlightAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@admin.com", "1234!@#$")
        self.user = User.objects.create_user("user", "user@user.com", "1234!@#$")

        self.airport1 = Airport.objects.create(name="Boryspil", closest_big_city="Kyiv")
        self.airport2 = Airport.objects.create(name="Lviv", closest_big_city="Lviv")

        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=540)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(name="UR-PSA", rows=10, seats_per_row=4, airplane_type=self.airplane_type)
        self.crew = Crew.objects.create(first_name="Vasya", last_name="Pupkin")

        self.future_flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
        )
        self.future_flight.crew.add(self.crew)

        self.past_flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() - timezone.timedelta(days=2),
            arrival_time=timezone.now() - timezone.timedelta(days=2, hours=2),
        )
        self.past_flight.crew.add(self.crew)

        self.base_url = "/api/airport/flights/"

    def test_list_future_flights_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.future_flight.id)

    def test_list_all_flights_admin_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)
        self.assertEqual(len(response.data["results"]), 2)

    def test_flight_tickets_left_annotation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.base_url)
        flight_data = [f for f in response.data["results"] if f["id"] == self.future_flight.id][0]
        self.assertEqual(flight_data["tickets_left"], self.airplane.rows * self.airplane.seats_per_row)

    def test_retrieve_flight_detail(self):
        self.client.force_authenticate(user=self.user)
        url = f"{self.base_url}{self.future_flight.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["route"]["source"], self.route.source.closest_big_city)
