from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile, User


@receiver(post_save, sender=User)
def create_and_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
