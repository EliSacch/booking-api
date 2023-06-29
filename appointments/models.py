from django.db import models
from django.contrib.auth.models import User

from treatments.models import Treatment


class Appointment(models.Model):
    class Slot(models.IntegerChoices):
        NINE = 900, '9:00'
        HALFNINE = 950, '9:30'
        TEN = 1000, '10:00'
        HALFTEN = 1050, '10:30'
        ELEVEN = 1100, '11:00'
        HALFELEVEN = 1150, '11:30'
        TWELVE = 1200, '12:00'
        HALFTWELVE = 1250, '12:30'
        THIRTEEN = 1300, '13:00'
        HALFTHIRTEEN = 1350, '13:30'
        FOURTEEN = 1400, '14:00'
        HALFFOURTEEN = 1450, '14:30'
        FIFTEEN = 1500, '15:00'
        HALFFIFTEEN = 1550, '15:30'
        SIXTEEN = 1600, '16:00'
        HALFSIXTEEN = 1650, '16:30'

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
        )
    client_name = models.CharField(max_length=255, null=True, blank=True)
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.PROTECT,
        null=True
        )
    date = models.DateField()
    time = models.IntegerField(choices=Slot.choices, default=Slot.NINE)
    end_time = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s appointment on {self.date}"
