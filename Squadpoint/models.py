from django.contrib.auth.models import AbstractUser
from django.db import models
from Capstone.settings import AUTH_USER_MODEL
import json
class User(AbstractUser):
    friends = models.ManyToManyField(
        AUTH_USER_MODEL, blank=True, symmetrical=False, default=None)
    pass

    def __str__(self):
        return f'User @{self.username}'


class Photo(models.Model):
    altText = models.CharField(max_length=255)
    image = models.ImageField()

    def __str__(self):
        return self.altText


class Location(models.Model):
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    subcity = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    houseNumber = models.IntegerField()

    def __str__(self):
        return f'{self.country}, {self.city}, {self.subcity}, {self.landmark}, {self.houseNumber}'


class SportZone(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        User, blank=True, related_name="user_favorites")
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    photos = models.ManyToManyField(Photo, blank=True, default=None)
    available_time_from = models.DateTimeField()
    available_time_to = models.DateTimeField()
    available_day_from = models.CharField(max_length=12)
    available_day_to = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.name}, Location: {self.location}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.location.city,
            'area': self.location.subcity
        }


class Sport_court(models.Model):
    name = models.CharField(max_length=24)
    max_num_people = models.PositiveIntegerField(default=4)
    payment_rate_per_hour = models.FloatField()
    is_booked = models.BooleanField(default=False)
    photos = models.ManyToManyField(Photo, blank=True)
    sport_zone = models.ForeignKey(
        SportZone, on_delete=models.CASCADE, related_name="sport_courts")

    def __str__(self):
        return f'{self.name}, from {self.sport_zone.name}'

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "max_num_people": self.max_num_people,
                "payment_rate_per_hour": self.payment_rate_per_hour,
                "is_booked": self.is_booked}


class Booking(models.Model):
    creater = models.ForeignKey(
        User, related_name='user_bookings', on_delete=models.CASCADE)
    sport_zone = models.ForeignKey(
        SportZone, related_name='bookings', on_delete=models.CASCADE)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    sport_court = models.ForeignKey(
        Sport_court, related_name='bookings', on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        User, blank=True, related_name='participated_bookings')
    is_held = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    length_time = models.DurationField(default=0)

    def __str__(self):

        return f'Booking of {self.sport_court.name} court booked from {self.starts} to {self.ends} on  {self.ends.strftime("%b %d %Y")} '

    def serialize(self):
        formatted_datetime = self.starts.isoformat()
        json_datetime = json.dumps(formatted_datetime)
        return {
            "id": self.id,
            "creater": self.creater.username,
            "sport_zone": self.sport_zone.name,
            "starts": json_datetime,
            "sport_court": self.sport_court.name,
            "is_held": self.is_held,
            "is_canceled": self.is_canceled,
            "length_time": self.length_time,
            "date": self.ends.strftime("%b %d %Y")
        }


class Match(models.Model):
    booking = models.ForeignKey(
        Booking, related_name='matches', on_delete=models.CASCADE)
    numberParticipants = models.PositiveIntegerField()
    teamA_members = models.ManyToManyField(
        User, related_name="matches_where_user_is_in_A")
    teamB_members = models.ManyToManyField(
        User, related_name="matches_where_user_is_in_B")
    winner_team = models.CharField(max_length=255, blank=True)
    is_draw = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    is_held = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    duration = models.DurationField()

    def __str__(self):
        return f'Match in {self.booking.sport_zone.name} starts at {self.starts.strftime("%H:%M %p")} and ends at {self.ends.strftime("%H:%M %p %b %d %Y")} on {self.ends.strftime("%b %d %Y")}'

    def serialize(self):
        formatted_datetime = self.starts.isoformat()
        json_datetime = json.dumps(formatted_datetime)
        return {
            "id": self.id,
            "creater": self.booking.creater.username,
            "sport_zone": self.booking.sport_zone.name,
            "starts": json_datetime,
            "sport_court": self.booking.sport_court.name,
            "is_held": self.is_held,
            "is_canceled": self.is_canceled,
            "duration": self.duration,
            "date": self.ends.strftime("%b %d %Y")
        }


class Notifications(models.Model):
    to_user = models.ForeignKey(
        User, related_name="user_notifications", on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    def serialize(self):
        return {"id": self.id, "to": self.to_user.username, "message": self.message, "is_read": self.is_read}
