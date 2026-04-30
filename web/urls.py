from django.urls import path

from .views import show_challenge, verify_challenge

app_name = "web"
urlpatterns = [
    path('', view=show_challenge, name="portal"),
    path('check/', view=verify_challenge, name="check"),
]
