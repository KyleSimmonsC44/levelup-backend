import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Game_Type, Game, Event
from django.contrib.auth.models import User

class EventTests(APITestCase):
    def setUp(self):

        url="/register"
        data= {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"            
        }

        response= self.client.post(url, data, format="json")

                # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        gametype = Game_Type()
        gametype.label = "Board game"
        gametype.save()

        game=Game()
        game.title="title"
        game.number_of_players= 3
        game.description="gud game"
        game.game_type_id= 1
        game.gamer_id= 1
        game.save()



    def test_create_event(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/events"
        data = {
            "event_time": "2021-02-12 12:47:00",
            "location": "your moms house",
            "gameId": 1,
            "gamerId": 1
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["event_time"], "2021-02-12 12:47:00")
        self.assertEqual(json_response["location"], "your moms house")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["scheduler"]['id'], 1)

    def test_get_event(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        event = Event()
        event.event_time = "2021-02-12 12:47:00"
        event.location = "Monopoly"
        event.scheduler_id = 1
        event.game_id = 1

        event.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["location"], "Monopoly")
        self.assertEqual(json_response["event_time"], "2021-02-12T12:47:00Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["scheduler"]["id"], 1)

    def test_change_event(self):
        """
        Ensure we can change an existing game.
        """
        event = Event()
        event.event_time = "2021-02-12 12:47:00"
        event.location = "Sorry"
        event.scheduler_id = 1
        event.game_id = 1
        event.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "event_time": "2021-03-12 12:47:00",
            "location": "your moms house",
            "gameId": 1,
            "gamerId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["location"], "your moms house")
        self.assertEqual(json_response["event_time"], "2021-03-12T12:47:00Z")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["scheduler"]["id"], 1)

    def test_delete_event(self):
        """
        Ensure we can delete an existing game.
        """
        event = Event()
        event.event_time = "2021-02-12 12:47:00"
        event.location = "Sorry"
        event.scheduler_id = 1
        event.game_id = 1
        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event AGAIN TO VERIFY 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)