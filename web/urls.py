from django.urls import path

from .views import show_challenge, verify_challenge, show_challenge_jwtmode

app_name = "web"
urlpatterns = [
    path('', view=show_challenge, name="portal"),
    path('check/', view=verify_challenge, name="check"),
    path('jwt/', view=show_challenge_jwtmode, name="jwt"),
]
