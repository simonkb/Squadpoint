import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import User, Sport_court, SportZone, Booking, Match
import datetime
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "squadpoint/index.html")
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "squadpoint/login.html", {
                "message": "Invalid username and/or password."
            })
    elif request.method == "PUT" or request.method == "GET":
        return render(request, "squadpoint/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "squadpoint/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
        except IntegrityError:
            return render(request, "squadpoint/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "squadpoint/register.html")
def search(request, query):
    if request.method == "GET":
        query = query.lower()
        sportZones = []
        for sportZone in SportZone.objects.all():
            #Case 1 search by game name
            for sport in sportZone.sport_courts.all():
                if(sport.name == query or sport.name.__contains__(query) or sport.name.startswith(query) or sport.name.lower() == query.lower()):
                    if(sportZone not in sportZones):
                        sportZones.append(sportZone)
                    break
            #Case 2 search by sport zone name 
            if(sportZone.name == query or sportZone.name.__contains__(query) or sportZone.name.startswith(query) or sportZone.name.lower() == query.lower() or query.lower().__contains__(sportZone.name)):
                if(sportZone not in sportZones):
                    sportZones.append(sportZone)
            #Case 3 search by landmark
            if(sportZone.location.landmark == query or sportZone.location.landmark.__contains__(query) or sportZone.location.landmark.startswith(query) or sportZone.location.landmark.lower() == query.lower() or query.lower().__contains__(sportZone.location.landmark)):
                if(sportZone not in sportZones ):
                    sportZones.append(sportZone)
            #case 4 search by area
            if(sportZone.location.subcity == query or sportZone.location.subcity.__contains__(query) or sportZone.location.subcity.startswith(query) or sportZone.location.subcity.lower() == query.lower() or query.lower().__contains__(sportZone.location.subcity)):
                if(sportZone not in sportZones):
                    sportZones.append(sportZone)
            #case 5 search by city
            if(sportZone.location.city == query or sportZone.location.city.__contains__(query) or sportZone.location.city.startswith(query) or sportZone.location.city.lower() == query.lower() or query.lower().__contains__(sportZone.location.city)):
                if(sportZone not in sportZones):
                    sportZones.append(sportZone)
            #case 6 search by country
            if(sportZone.location.country == query or sportZone.location.country.__contains__(query) or sportZone.location.country.startswith(query) or sportZone.location.country.lower() == query.lower() or query.lower().__contains__(sportZone.location.country)):
                if(sportZone not in sportZones):
                    sportZones.append(sportZone)
            #case 7 search for all
            if(query.lower() == "all"):
                all_sportZones = SportZone.objects.all()
                sportZones = all_sportZones
        if(len(sportZones) == 0):
            return render(request, "squadpoint/search.html", {'sport_zones': sportZones, 'query': query, "empty":True, 'error':f"Empty result for '{query}', please try again with a different keyword"})         
        return render(request, "squadpoint/search.html", {'sport_zones': sportZones, 'query': query, "empty": False, 'error':""})    
def sport_zone(request, id):
    if(request.method == "GET"):
        sportZone =SportZone.objects.get(id = id)
        return render(request, 'squadpoint/sport_zone.html', {'sportZone': sportZone})
def page(request, name):
    name = name.lower()
    if (name == ''):
        return render(request, "squadpoint/index.html")
    elif (name == 'matches'):
        return render(request, "squadpoint/matches.html")
    elif(name == 'bookings' and request.user.is_authenticated):
        user = request.user
        bookings = user.user_bookings.all()
        return render(request, "squadpoint/bookings.html",{'bookings': bookings})
    elif(name == 'notifications' and request.user.is_authenticated):
        user = request.user
        allNotifications = user.user_notifications.all()
        return render(request, "squadpoint/notifications.html", {'notifications': allNotifications})
    elif(name == 'about'):
        return render(request, "squadpoint/about.html")
    elif(name == 'profile'and request.user.is_authenticated):
        return render(request, "squadpoint/profile.html", {'user': request.user})
def sport_court(request, id):
    if request.method == 'GET':
        sport = Sport_court.objects.get(id=id)
        return render(request, "squadpoint/sport_court.html", {'sport_court' : sport})
@login_required
@csrf_exempt
def book(request, court_id):
    sport_court = Sport_court.objects.get(id=court_id)
    if request.method == 'PUT':
        creater = request.user
        data = json.loads(request.body)
        starts = data['starts']
        ends = data['ends']
        #X and y are just used to get the default duartion of 3O minutes. 
        x = datetime.datetime.strptime("2/3/2022, 9:30:00 PM", '%m/%d/%Y, %I:%M:%S %p')
        y = datetime.datetime.strptime("2/3/2022, 10:00:00 PM", '%m/%d/%Y, %I:%M:%S %p')
        length_time = y-x

        sport_zone = sport_court.sport_zone
        for booking in sport_court.bookings.all():
            formatted_datetime = booking.starts.isoformat()
            json_datetime = json.dumps(formatted_datetime)
            if (json_datetime[1:17] == starts[0:16]):
                return JsonResponse({"error" : "The court is already booked for the selected time, \nplease select different time."})
        booking = Booking(creater=creater, sport_court = sport_court, starts=starts, ends=ends, sport_zone=sport_zone, length_time=length_time)
        booking.save()
        return HttpResponse("Success")
    elif request.method == "GET":
        return JsonResponse([booking.serialize() for booking in sport_court.bookings.all()], safe=False)
@login_required
@csrf_exempt
def create_match(request, booking_id):
    if request.method == 'PUT':
        booking = Booking.objects.get(id= booking_id)
        if booking.matches.all().count() == 0 and booking.is_canceled == False:
            data = json.loads(request.body)     
            numberParticipants = data['numberParticipants']
            if(int(numberParticipants) != 2):
                numberParticipants = 4
            starts = data['m_starts']
            ends = data['m_ends']
            x = datetime.datetime.strptime("2/3/2022, 9:30:00 PM", '%m/%d/%Y, %I:%M:%S %p')
            y = datetime.datetime.strptime("2/3/2022, 10:00:00 PM", '%m/%d/%Y, %I:%M:%S %p')
            duration = y-x
            match = Match(booking = booking, numberParticipants = numberParticipants, starts = starts, ends = ends, duration = duration)
            match.save()

            if data['join']:
                match.teamA_members.add(booking.creater)
            return HttpResponse("success")
        else:
            return HttpResponse("error")
@login_required
@csrf_exempt
def bookings(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        user_bookings = user.user_bookings.all()
        user_bookings_ordered = user_bookings.order_by("starts").all()
        return JsonResponse([booking.serialize() for booking in user_bookings_ordered], safe=False)
def matches(request):
    if request.method == 'GET':
        matches = Match.objects.all()
        ordered = matches.order_by("starts").all()
        return JsonResponse([matches.serialize() for matches in ordered], safe=False)
@login_required
@csrf_exempt
def join_match(request, match_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            match = Match.objects.get(id=match_id)
            data = json.loads(request.body)
            if data["selected_team"]=="A":
                if match.teamA_members.all().count() < match.numberParticipants/2 and request.user in match.teamA_members.all()==False:
                    match.teamA_members.add(request.user)
                    match.save()
                    return HttpResponse("Success")
                else:
                    return HttpResponse("error")
            elif data["selected_team"]=="B":
                if match.teamB_members.all().count() < match.numberParticipants/2 and request.user in match.teamB_members.all()==False:
                    match.teamB_members.add(request.user)
                    match.save()
                    return HttpResponse("Success")
                else:
                    return HttpResponse("error")            
    else:
        return render(request, "squadpoint/login.html")


