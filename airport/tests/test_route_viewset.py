from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from airport.models import Airport, Route

User = get_user_model()

class RouteAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@admin.com", password="admin123"
        )
        self.regular_user = User.objects.create_user(
            username="user", email="user@admin.com", password="user123"
        )

        self.airport1 = Airport.objects.create(name="Boryspil", closest_big_city="Kyiv")
        self.airport2 = Airport.objects.create(name="Lviv", closest_big_city="Lviv")
        self.airport3 = Airport.objects.create(name="Odesa", closest_big_city="Odesa")

        self.route1 = Route.objects.create(source=self.airport1, destination=self.airport2, distance=540)
        self.route2 = Route.objects.create(source=self.airport2, destination=self.airport3, distance=625)

        self.base_url = "/api/airport/routes/"

    def test_create_route_admin_only(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"source": self.airport1.pk, "destination": self.airport3.pk, "distance": 480}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 3)

        self.client.force_authenticate(user=self.regular_user)
        data2 = {"source": self.airport2.pk, "destination": self.airport1.pk, "distance": 500}
        response2 = self.client.post(self.base_url, data2)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_routes(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_routes_by_source(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.base_url, {"source": self.airport1.closest_big_city})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["source"], self.airport1.closest_big_city)

    def test_filter_routes_by_destination(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.base_url, {"destination": self.airport3.closest_big_city})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["destination"], self.airport3.closest_big_city)

    def test_retrieve_route_detail(self):
        self.client.force_authenticate(user=self.regular_user)
        url = f"{self.base_url}{self.route1.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["source"], self.route1.source.pk)
        self.assertEqual(response.data["destination"], self.route1.destination.pk)
        self.assertEqual(response.data["distance"], self.route1.distance)
