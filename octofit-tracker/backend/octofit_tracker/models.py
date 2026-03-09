
from djongo import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team_id = models.ObjectIdField()
    class Meta:
        db_table = 'users'


# Embedded model for Team members
class Member(models.Model):
    user_id = models.ObjectIdField()
    class Meta:
        abstract = True

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ArrayField(model_container=Member, blank=True, null=True)
    class Meta:
        db_table = 'teams'

class Activity(models.Model):
    user_id = models.ObjectIdField()
    activity = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        db_table = 'activities'

class Leaderboard(models.Model):
    user_id = models.ObjectIdField()
    points = models.IntegerField()
    class Meta:
        db_table = 'leaderboard'

class Workout(models.Model):
    user_id = models.ObjectIdField()
    workout = models.CharField(max_length=100)
    reps = models.IntegerField()
    class Meta:
        db_table = 'workouts'
