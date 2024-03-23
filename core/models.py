from django.db import models

class City(models.Model):
    name = models.CharField(max_length=225)
    country = models.CharField(max_length=4)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

    