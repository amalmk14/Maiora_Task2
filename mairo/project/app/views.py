from django.shortcuts import render
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Joke
from .serializers import JokeSerializer

# Create your views here.

def Fetch_Jokes():
    url = "https://v2.jokeapi.dev/joke/Any?amount=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("jokes", [])
    return []

class JokeViewSet(viewsets.ModelViewSet):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def create(self, request, *args, **kwargs):
        jokes = Fetch_Jokes()
        for i in jokes:
            Joke.objects.create(
                category=i["category"],
                type=i["type"],
                joke=i.get("joke", ""),
                setup=i.get("setup", ""),
                delivery=i.get("delivery", ""),
                nsfw=i["flags"]["nsfw"],
                political=i["flags"]["political"],
                sexist=i["flags"]["sexist"],
                safe=i["safe"],
                lang=i["lang"]
            )
        return Response({"message": "Jokes stored successfully"}, status=status.HTTP_201_CREATED)
