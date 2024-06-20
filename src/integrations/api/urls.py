from django.urls import path

from .views import WriteDataToGoogleSheet, TestAPI, WantResultsAPI

urlpatterns = [
    path('write-call-to-google-sheet', WriteDataToGoogleSheet.as_view()),
    path('crm-whook/<slug:slug>', WantResultsAPI.as_view()),
    path('tests', TestAPI.as_view()),
]
