from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from teams.models import Team, Person
from teams.pagination import ApiPagination
from teams.permissions import IsAdminOrReadOnly
from teams.serializers import (
    TeamSerializer,
    TeamDetailSerializer,
    PersonSerializer,
    PersonListSerializer,
    PersonDetailSerializer,
    AssignPersonToTeamSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ApiPagination

    def get_queryset(self):
        """Retrieve the team with filter"""
        name = self.request.query_params.get("name")

        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        """Distribution of serializers by actions"""
        if self.action == "retrieve":
            return TeamDetailSerializer

        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by team name (ex. ?name=Team 1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """List teams with filter by name"""
        return super().list(request, *args, **kwargs)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related("team")
    serializer_class = PersonSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ApiPagination

    def get_queryset(self):
        """Retrieve the person with filter"""
        last_name = self.request.query_params.get("last_name")

        queryset = super().get_queryset()

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    def get_serializer_class(self):
        """Distribution of serializers by actions"""
        if self.action == "list":
            return PersonListSerializer

        if self.action == "retrieve":
            return PersonDetailSerializer

        if self.action == "assign_to_team":
            return AssignPersonToTeamSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=["put"], url_path="assign-to-team")
    def assign_to_team(self, request, pk):
        """Endpoint for assigning the specific person to a team"""
        person = self.get_object()
        serializer = self.get_serializer(person, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filter by last name of person (ex. ?last_name=Smith)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """List people with filter by last name"""
        return super().list(request, *args, **kwargs)
