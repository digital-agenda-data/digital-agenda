from django.urls import path, include
from rest_framework import routers

from .views import CreateShortURLViewSet

router = routers.DefaultRouter()
router.register("short-urls", CreateShortURLViewSet, basename="short-urls")


urlpatterns = [
    path("", include(router.urls)),
]
