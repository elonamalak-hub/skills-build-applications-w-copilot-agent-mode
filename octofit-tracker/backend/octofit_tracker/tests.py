from django.test import TestCase
from .models import User, Team, Activity, Leaderboard, Workout

class ModelSmokeTest(TestCase):
    def test_user_model(self):
        User.objects.create(name='Test User', email='test@example.com', team_id='507f1f77bcf86cd799439011')
        self.assertEqual(User.objects.count(), 1)
    def test_team_model(self):
        Team.objects.create(name='Test Team', members=[])
        self.assertEqual(Team.objects.count(), 1)
    def test_activity_model(self):
        Activity.objects.create(user_id='507f1f77bcf86cd799439011', activity='Test', duration=10)
        self.assertEqual(Activity.objects.count(), 1)
    def test_leaderboard_model(self):
        Leaderboard.objects.create(user_id='507f1f77bcf86cd799439011', points=5)
        self.assertEqual(Leaderboard.objects.count(), 1)
    def test_workout_model(self):
        Workout.objects.create(user_id='507f1f77bcf86cd799439011', workout='Test', reps=10)
        self.assertEqual(Workout.objects.count(), 1)
