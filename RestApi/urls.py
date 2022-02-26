from django.urls import path

from .views import template_check

urlpatterns = [
    path('match', template_check.as_view())
]
