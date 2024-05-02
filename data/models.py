from django.db import models
from django.utils.timezone import now

class Dataset(models.Model):
    dt = models.DateTimeField(default = now)
    malayalam = models.TextField()
    english = models.TextField()
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    consensus = models.BooleanField()
    again = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Calculate consensus based on good and bad counts
        self.consensus = self.good > self.bad
        
        # Set again to False if good or bad counts exceed 10
        if self.good >= 2 or self.bad >= 2:
            self.again = False
        else:
            self.again = True

        super().save(*args, **kwargs)
