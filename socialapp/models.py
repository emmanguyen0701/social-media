from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance) #user field of Profile is the instance of the signal Sender
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"{self.created_at}"
            f"{self.body[:20]}"
        )


class Image(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    image = models.ImageField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

        