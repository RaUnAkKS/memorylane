from .models import Notification

def create_unlock_notifications(capsule):
    users = set()

    users.add(capsule.created_by)

    for user in capsule.recipients.all():
        users.add(user)

    for user in capsule.collaborators.all():
        users.add(user)

    for user in users:
        Notification.objects.create(
            user=user,
            capsule=capsule,
            message=f'🎉 Capsule "{capsule.title}" has unlocked!'
        )
