from django.db import models

# Create your models here.


class UserProfile(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.IntegerField()
    bio = models.TextField()
    score = models.IntegerField(default=0)
    image = models.ImageField(default="image001.jpg")

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return self.fullname