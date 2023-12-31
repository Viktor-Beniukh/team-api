from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, related_name="members", null=True, blank=True
    )

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
