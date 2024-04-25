from rest_framework.serializers import ModelSerializer, SerializerMethodField

from management.models import Parking, ParkingSpace, Reservation, Ticket

class TicketSerializer(ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"

class ParkingSerializer(ModelSerializer):

    class Meta:
        model = Parking
        fields = "__all__"

    
class ParkingSpaceSerializer(ModelSerializer):

    class Meta:
        model = ParkingSpace
        fields = "__all__"

class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        exclude = ['ticket']