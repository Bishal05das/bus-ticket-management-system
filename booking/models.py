from django.db import models
from django.utils import timezone

class Bus(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Route(models.Model):
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.from_city} to {self.to_city}"

class Schedule(models.Model):
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_date = models.DateField()
    departure_time=models.TimeField(default=timezone.now)
    available_seats=models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)
        if not Seat.objects.filter(schedule=self).exists():
            for i in range(1, self.bus.capacity + 1):
                Seat.objects.create(schedule=self, seat_number=i)
    

    

    def __str__(self):
        return f"{self.bus} on {self.route} at {self.departure_date}--{self.departure_time}"
    

class Seat(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.schedule}"
    
class booking_history(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)  # New field to track creation time

    def __str__(self):
        return f"{self.name} - {self.seat} - {self.created_at}"