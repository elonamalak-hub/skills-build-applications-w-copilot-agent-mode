from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient
from django.conf import settings

# Models for direct MongoDB access (for index creation)
client = MongoClient('mongodb://localhost:27017')
db = client['octofit_db']

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Teams
        marvel_team = {'name': 'Team Marvel', 'members': []}
        dc_team = {'name': 'Team DC', 'members': []}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Users (super heroes)
        users = [
            {'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team_id': dc_team_id},
            {'name': 'Clark Kent', 'email': 'clark@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Update teams with members
        db.teams.update_one({'_id': marvel_team_id}, {'$set': {'members': user_ids[:2]}})
        db.teams.update_one({'_id': dc_team_id}, {'$set': {'members': user_ids[2:]}})

        # Activities
        activities = [
            {'user_id': user_ids[0], 'activity': 'Running', 'duration': 30},
            {'user_id': user_ids[1], 'activity': 'Cycling', 'duration': 45},
            {'user_id': user_ids[2], 'activity': 'Swimming', 'duration': 60},
            {'user_id': user_ids[3], 'activity': 'Yoga', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 110},
            {'user_id': user_ids[3], 'points': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user_id': user_ids[0], 'workout': 'Chest Day', 'reps': 50},
            {'user_id': user_ids[1], 'workout': 'Leg Day', 'reps': 60},
            {'user_id': user_ids[2], 'workout': 'Back Day', 'reps': 55},
            {'user_id': user_ids[3], 'workout': 'Arm Day', 'reps': 65},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
