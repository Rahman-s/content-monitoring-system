from django.urls import path
from .views import (
    KeywordCreateView,
    ScanTriggerView,
    FlagListView,
    FlagStatusUpdateView,
)

urlpatterns = [
    path('keywords/', KeywordCreateView.as_view(), name='keyword-create'),
    path('scan/', ScanTriggerView.as_view(), name='scan-trigger'),
    path('flags/', FlagListView.as_view(), name='flag-list'),
    path('flags/<int:pk>/', FlagStatusUpdateView.as_view(), name='flag-update'),
]