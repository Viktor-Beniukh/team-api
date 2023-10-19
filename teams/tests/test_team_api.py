from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from teams.models import Team
from teams.pagination import ApiPagination
from teams.serializers import TeamSerializer, TeamDetailSerializer


TEAM_URL = reverse("teams:team-list")


def sample_team(**params):
    defaults = {
        "name": "Team 1",
    }
    defaults.update(params)

    return Team.objects.create(**defaults)


def detail_url(team_id):
    return reverse("teams:team-detail", args=[team_id])


class UnauthenticatedTeamApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_teams(self):
        sample_team()
        pagination = ApiPagination

        response = self.client.get(TEAM_URL)

        teams = Team.objects.all()
        serializer = TeamSerializer(pagination, teams, many=True)

        if serializer.is_valid():
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)

    def test_filter_teams_by_name(self):
        team1 = sample_team()
        team2 = sample_team(name="Team 2")
        team3 = sample_team(name="Another")

        response = self.client.get(TEAM_URL, {"name": "team"})

        self.assertContains(response, team1.name)
        self.assertContains(response, team2.name)
        self.assertNotContains(response, team3.name)

    def test_retrieve_team_detail(self):
        team = sample_team()

        url = detail_url(team.id)
        response = self.client.get(url)

        serializer = TeamDetailSerializer(team)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AuthenticatedTeamApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_create_team_forbidden(self):
        payload = {
            "name": "Team 1",
        }

        response = self.client.post(TEAM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTeamApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "adminpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_team(self):

        payload = {
            "name": "Team 1",
        }

        response = self.client.post(TEAM_URL, payload)

        team = Team.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(team, key))

    def test_update_team(self):
        team = sample_team()

        payload = {
            "name": "Updated Team 1",
        }

        url = detail_url(team.id)
        response = self.client.patch(url, payload)

        team.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(team.name, payload["name"])

    def test_delete_team(self):
        team = sample_team(name="Team 1")

        url = detail_url(team.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(id=team.id).exists())
