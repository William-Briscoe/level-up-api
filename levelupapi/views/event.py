from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, GameType

class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all Events

        Returns:
            Response -- JSON serialized list of Events
        """

        game_query = request.query_params.get('game')

        if game_query:
            Events = Event.objects.filter(game=game_query)
        else:
            Events = Event.objects.all()
            
        serializer = EventSerializer(Events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        
        event = Event.objects.create(
            date=request.data["date"],
            game=game,
            organizer= gamer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.date = request.data["date"]
        
        #event.attendees = request.data["attendees"]
        organizer = Gamer.objects.get(pk=request.data["organizer"])
        event.organizer = organizer
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GamerSeralizer(serializers.ModelSerializer):
    class Meta:
        model= Gamer
        fields = ('id', 'user', 'bio', 'full_name')


class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= GameType
        fields = ('id', 'label', 'description')


class GameSerializer(serializers.ModelSerializer):
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model= Game
        fields = ('title', 'maker', 'num_of_players', 'skill_level', 'gamer', 'game_type')




class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for Events
    """

    organizer = GamerSeralizer(many=False)
    attendees = GamerSeralizer(many=True)
    game = GameSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'date', 'game', 'attendees', 'organizer')