from datetime import datetime, timezone
from management.models import Parking, ParkingSpace, Reservation, Ticket
from rest_framework import serializers

class ParkingService:

    def create(self, serializer, user):
        new_parking = Parking.objects.create(
                parking_name = serializer.validated_data['parking_name'],
                hour_price = serializer.validated_data['hour_price'],
                created_by = user,
            )
        num_spaces = serializer.validated_data['num_spaces']
        for i in range(1,num_spaces):
            temp_parking_space = ParkingSpace.objects.create(
                cod = "A"+str(i),
                status = False,
                parking = new_parking,
                created_by = user,
            )
        return new_parking

class ParkingSpaceService:

    def create(self, serializer, user):
        new_parking_space = ParkingSpace.objects.create(
                cod = serializer.validated_data['cod'],
                status = serializer.validated_data['status'],
                parking = serializer.validated_data['parking'],
                created_by = user,
            )
        return new_parking_space

class TicketService:

    def create(self, serializer, user):
        parking_space = serializer.validated_data['parking_space']
        checkin = serializer.validated_data['checkin']
        checkout = serializer.validated_data['checkout']
        
        if parking_space.vacancy_type == 'priority':
            raise serializers.ValidationError("Cannot create ticket: parking space is of type 'priority'.")
        
        new_ticket = Ticket.objects.create(
            model=serializer.validated_data['model'],
            license_plate=serializer.validated_data['license_plate'],
            checkin=checkin,
            checkout=checkout,
            parking_space=parking_space,
            value=serializer.validated_data['value'],
            created_by=user,
        )
        return new_ticket   
    
    def calc_ticket(self, ticket):
        reference_date = datetime.now().date()

        combined_checkin = datetime.combine(reference_date, ticket.checkin)
        combined_checkout = datetime.combine(reference_date, ticket.checkout)
            
        total_time = combined_checkout - combined_checkin
        ticket.value = total_time.total_seconds() / 3600 * ticket.parking_space.parking.hour_price
        ticket.save()
        return ticket


class ReservationService:

    def create(self, serializer, user):
        parking_space = serializer.validated_data['parking_space']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        ticket_data = serializer.validated_data.pop('ticket', None)  # Remover os dados do ticket
        
        overlapping_reservations = Reservation.objects.filter(
            parking_space=parking_space,
            start_time__lt=end_time, 
            end_time__gt=start_time  
        )
        
        if overlapping_reservations.exists():
            raise serializers.ValidationError("Another reservation already exists for this parking space within the specified time range.")
        
        new_reservation = Reservation.objects.create(
            parking_space=parking_space,
            start_time=start_time,
            end_time=end_time,
            created_by=user
        )
        
        if ticket_data:
            # Criar o ticket associado à reserva, se houver dados do ticket
            ticket = Ticket.objects.create(reservation=new_reservation, **ticket_data)
            new_reservation.ticket = ticket  # Associar o ticket à reserva
            new_reservation.save()  # Salvar a reserva com o ticket associado
        
        return new_reservation
