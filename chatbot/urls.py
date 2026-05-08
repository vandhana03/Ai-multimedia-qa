from django.urls import path
from .views import ChatView, SummaryView, TimestampView

urlpatterns = [

    path('chat/',ChatView.as_view()),
    path('summary/', SummaryView.as_view()),
    path('timestamps/', TimestampView.as_view()),

]