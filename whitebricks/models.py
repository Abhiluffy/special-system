from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class PG(models.Model):

    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    email = models.EmailField(default=None)
    phone = models.IntegerField(default=None)
    address = models.CharField(max_length=255, default=None)
    highlights = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    bedroom = models.IntegerField()
    city = models.CharField(max_length=50)
    image = models.FileField(upload_to='media/uploads', null=True)
    created_by = models.CharField(max_length=100, default=None)



class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()





