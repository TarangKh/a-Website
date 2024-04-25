from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bio = models.TextField()
    score = models.IntegerField(default=0)
    image = models.ImageField(default="pictures/image001.jpg", upload_to="pictures")

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return self.fullname
    

class UserSeen(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    user_seen_id = models.IntegerField()

    class Meta:
        ordering = ['user_seen_id']


class DBPointer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    db_pointer = models.IntegerField()
    preference = models.CharField(max_length=1)

