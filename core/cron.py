from django.contrib.auth import get_user_model
User = get_user_model()


def manage_stories():
    User.objects.get(username='hemang18').delete()
