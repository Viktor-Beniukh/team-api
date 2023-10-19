from django.test import TestCase

from teams.models import Team, Person


class ModelsTest(TestCase):

    def test_team_str(self) -> None:
        team = Team.objects.create(
            name="Team 1",
        )
        self.assertEqual(str(team), team.name)

    def test_person_str(self) -> None:
        person = Person.objects.create(
            first_name="John", last_name="Doe"
        )
        self.assertEqual(str(person), f"{person.first_name} {person.last_name}")
