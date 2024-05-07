from django.db import models
from django.utils.timezone import now

class Dataset(models.Model):
    dt = models.DateTimeField(default = now)
    malayalam = models.TextField()
    english = models.TextField()
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    consencus_choices = {"g" : "Good", "b" : "Bad", "d" : "Draw"}
    consensus = models.CharField(max_length=1, choices=consencus_choices)
    again = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Calculate consensus based on good and bad counts
        if self.good > self.bad:
            self.consensus = "g"
        elif self.good == self.bad:
            self.consensus = "d"
        else:
            self.consensus = "b"
        
        # Set again to False if good or bad counts exceed 10
        if self.good >= 7 or self.bad >= 7:
            self.again = False
        else:
            self.again = True

        super().save(*args, **kwargs)
