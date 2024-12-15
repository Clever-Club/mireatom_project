from django.urls import path

from .views import DocsCreationView

urlpatterns = [
    path(
        "",
        DocsCreationView.as_view(),
        name="auth",
    ),

]