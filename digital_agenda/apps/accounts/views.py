from constance import config
from django.contrib.auth import views as auth_views
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


class PasswordResetView(auth_views.PasswordResetView):
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        if not config.PASSWORD_LOGIN_ENABLED:
            raise Http404
        return super().dispatch(*args, **kwargs)
