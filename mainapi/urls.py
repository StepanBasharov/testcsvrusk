from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('top_users/', views.TradeView.as_view()),
    path('upload/', views.UploadDetailsView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
