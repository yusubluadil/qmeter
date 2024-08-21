from django.urls import path

from feedback import views as feedback_views


urlpatterns = [
    path('', feedback_views.MainDataView.as_view()),
]
