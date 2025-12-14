from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='users/profile_photo/',blank=True,null=True)
    DOB = models.DateField(null=True,blank=True)

class Theme(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Capsule(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)
    unlock_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(User, related_name='received_capsules')
    collaborators = models.ManyToManyField(User, related_name='collab_capsules', blank=True)
    privacy = models.CharField(max_length=20, choices=[
        ('private','Private'),
        ('family','Family'),
        ('public','Public')
    ],
    default = 'private'
    )
    image = models.ImageField(
        upload_to='capsules/images/',
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to='capsules/videos/',
        blank=True,
        null=True
    )
    audio = models.FileField(
        upload_to='capsules/audio/',
        blank=True,
        null=True
    )
    EVENT_CHOICES = [
    ('graduation', 'Graduation'),
    ('wedding', 'Wedding'),
    ('birthday', 'Birthday'),
    ('anniversary', 'Anniversary'),
    ('custom', 'Custom Event'),
    ]

    unlock_type = models.CharField(max_length=20,
        choices=[('date', 'Date'),('event', 'Life Event'),],
        default='date'
    )

    unlock_event = models.CharField(max_length=30,choices=EVENT_CHOICES,blank=True,null=True)

    event_triggered = models.BooleanField(default=False)
    notification_sent = models.BooleanField(default=False)

    def is_unlocked(self):
        if self.unlock_type == 'date':
            return timezone.now() >= self.unlock_date

        if self.unlock_type == 'event':
            return self.event_triggered

        return False

    def __str__(self):
        return self.title
    

class CapsuleComment(models.Model):
    capsule = models.ForeignKey(
        Capsule,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    REACTION_CHOICES = [
    ('❤️', '❤️'),
    ('👍', '👍'),
    ('😢', '😢'),
    ]

    reaction = models.CharField(
    max_length=2,
    choices=REACTION_CHOICES,
    blank=True
    )


    def __str__(self):
        return f'Comment by {self.user} on {self.capsule}'
    
class CapsuleEntry(models.Model):
    capsule = models.ForeignKey(Capsule,on_delete=models.CASCADE,related_name='entries')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    text = models.TextField(blank=True)

    image = models.ImageField(upload_to='capsules/entries/images/',blank=True,null=True)
    video = models.FileField(upload_to='capsules/entries/videos/',blank=True,null=True)
    audio = models.FileField(upload_to='capsules/entries/audio/',blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Entry by {self.created_by} in {self.capsule}'


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    capsule = models.ForeignKey(Capsule,on_delete=models.CASCADE,null=True,blank=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user}'
