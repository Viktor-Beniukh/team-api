from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from teams.models import Team, Person
from teams.pagination import ApiPagination
from teams.serializers import PersonListSerializer, PersonDetailSerializer


PERSON_URL = reverse("teams:person-list")


def sample_person(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@gmail.com"
    }
    defaults.update(params)

    return Person.objects.create(**defaults)


def sample_team(**params):
    defaults = {
        "name": "Team 1",
    }
    defaults.update(params)

    return Team.objects.create(**defaults)


def detail_url(person_id):
    return reverse("teams:person-detail", args=[person_id])


def assign_url(person_id):
    return reverse("teams:person-assign-to-team", args=[person_id])


class UnauthenticatedPersonApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_people(self):
        sample_person()
        pagination = ApiPagination

        response = self.client.get(PERSON_URL)

        people = Person.objects.all()
        serializer = PersonListSerializer(pagination, people, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_filter_people_by_last_name(self):
        person1 = sample_person()
        person2 = sample_person(
            first_name="User 1", last_name="Last Name 1", email="user1.lastname1@gmail.com"
        )
        person3 = sample_person(
            first_name="User 2", last_name="Last Name 2", email="user2.lastname2@gmail.com"
        )

        response = self.client.get(PERSON_URL, {"last_name": "doe"})

        self.assertContains(response, person1.last_name)
        self.assertNotContains(response, person2.last_name)
        self.assertNotContains(response, person3.last_name)

    def test_retrieve_person_detail(self):
        person = sample_person()

        url = detail_url(person.id)
        response = self.client.get(url)

        serializer = PersonDetailSerializer(person)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AuthenticatedPersonApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_person_forbidden(self):
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com"
        }

        response = self.client.post(PERSON_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminPersonApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_person(self):

        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com"
        }

        response = self.client.post(PERSON_URL, payload)

        person = Person.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(person, key))

    def test_update_person(self):
        person = sample_person()

        payload = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@gmail.com"
        }

        url = detail_url(person.id)
        response = self.client.patch(url, payload)

        person.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(person.first_name, payload["first_name"])
        self.assertEqual(person.last_name, payload["last_name"])
        self.assertEqual(person.email, payload["email"])

    def test_delete_person(self):
        person = sample_person()

        url = detail_url(person.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Person.objects.filter(id=person.id).exists())

    def test_assign_person_to_team(self):
        person = sample_person()
        team = sample_team()

        url = assign_url(person.id)

        payload = {
            "team": team.id
        }

        response = self.client.put(url, payload)

        person.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(person.team.id, team.id)
