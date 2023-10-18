from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from teams.models import Team, Person
from teams.serializers import (
    TeamSerializer,
    PersonSerializer,
    PersonListSerializer,
    PersonDetailSerializer,
    AssignPersonToTeamSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related("team")
    serializer_class = PersonSerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == "list":
            return PersonListSerializer

        if self.action == "retrieve":
            return PersonDetailSerializer

        if self.action == "assign_to_team":
            return AssignPersonToTeamSerializer

        return super().get_serializer_class()

    @action(
        detail=True,
        methods=["put"],
        url_path="assign-to-team",
    )
    def assign_to_team(self, request, pk):
        person = self.get_object()
        serializer = self.get_serializer(person, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
