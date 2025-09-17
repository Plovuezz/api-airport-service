from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from airport.models import Airport

User = get_user_model()


class AirportAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@admin.com", password="admin123"
        )
        self.regular_user = User.objects.create_user(
            username="user", email="user@user.com", password="user123"
        )

        self.airport1 = Airport.objects.create(
            name="Boryspil International", closest_big_city="Kyiv"
        )
        self.airport2 = Airport.objects.create(
            name="Lviv International", closest_big_city="Lviv"
        )
        self.airport3 = Airport.objects.create(
            name="Odesa International", closest_big_city="Odesa"
        )

        self.base_url = "/api/airport/airports/"

    def test_create_airport_admin_only(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "Kharkiv Airport", "closest_big_city": "Kharkiv"}
        response = self.client.post(self.base_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 4)

        self.client.force_authenticate(user=self.regular_user)
        data2 = {"name": "Dnipro Airport", "closest_big_city": "Dnipro"}
        response2 = self.client.post(self.base_url, data2)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_airports(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_list_airports_search_filter(self):
        self.client.force_authenticate(user=self.regular_user)

        response_name = self.client.get(self.base_url, {"search": "Boryspil"})
        self.assertEqual(len(response_name.data["results"]), 1)
        self.assertEqual(response_name.data["results"][0]["name"], "Boryspil International")

        response_city = self.client.get(self.base_url, {"search": "Lviv"})
        self.assertEqual(len(response_city.data["results"]), 1)
        self.assertEqual(response_city.data["results"][0]["closest_big_city"], "Lviv")

    def test_retrieve_airport_detail(self):
        self.client.force_authenticate(user=self.regular_user)
        url = f"{self.base_url}{self.airport1.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.airport1.name)
        self.assertEqual(response.data["closest_big_city"], self.airport1.closest_big_city)
