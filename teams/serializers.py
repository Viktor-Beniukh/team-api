from rest_framework import serializers

from teams.models import Team, Person


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "members")


class TeamListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "name")


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "email")


class PersonListSerializer(serializers.ModelSerializer):

    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "email", "team_name")


class PersonDetailSerializer(serializers.ModelSerializer):
    team = TeamListSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "email", "team")


class AssignPersonToTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "team")
