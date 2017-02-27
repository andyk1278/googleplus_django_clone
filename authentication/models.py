from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')

    tagline = models.CharField(max_length=140, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    # whenever a User model created, UserProfile is notified and creates a corresponding
    # instance of itself. This ensures we never hav any 'orphan' Users.
    # Known as singal dispatching.
    @receiver(post_save, sender=User)
    def create_profile_for_user(sender, instance=None, created=False, **kwargs):
        if created:
            UserProfile.objects.get_or_create(user=instance)

    # whenever a Uder model is deleted, the corresponding UserProfile is also deleted
    @receiver(pre_delete, sender=User)
    def delete_profile_for_user(selfsender, instance=None, **kwargs):
        if instance:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()
