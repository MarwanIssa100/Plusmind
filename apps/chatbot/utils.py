from accounts.models import CustomUser


def get_guest_user():

    user, created = CustomUser.objects.get_or_create(
        username="guest_user",
        defaults={
            "email": "guest@local.test"
        }
    )

    return user
