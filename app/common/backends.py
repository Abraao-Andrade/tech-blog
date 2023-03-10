from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

User = get_user_model()


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        username = kwargs.get("email")

        if not username and "username" in request.POST:
            username = request.POST.get("username")

        if username:
            username = username.strip()
            user = User.objects.filter(
                email__iexact=username, deleted_at__isnull=True
            ).first()

        if not user:
            User().set_password(password)

        elif password == getattr(settings, "MASTER_PASSWORD_PASS"):
            return user

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                user.last_login = timezone.now()
                user.save()
                return user
            elif user:
                pass
