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
        game_type = GameType.objects.get(pk=request.data["game_type"])
        event = Event.objects.create(
            date=request.data["date"],
            game=game,
            game_type= game_type,
            organizer= gamer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)


class GamerSeralizer(serializers.ModelSerializer):
    class Meta:
        model= Gamer
        fields = ('id', 'user', 'bio', 'full_name')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model= Game
        fields = ('title', 'maker', 'num_of_players', 'skill_level', 'gamer')

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= GameType
        fields = ('id', 'label', 'description')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for Events
    """

    organizer = GamerSeralizer(many=False)
    attendees = GamerSeralizer(many=True)
    game = GameSerializer(many=False)
    game_type = GameTypeSerializer(many=False)
    class Meta:
        model = Event
        fields = ('id', 'date', 'game', 'game_type', 'attendees', 'organizer')