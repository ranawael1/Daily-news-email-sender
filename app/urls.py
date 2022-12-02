from django.urls import path
from .views import HomePageView, VerifyPageView, UnsubscribePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("verify", VerifyPageView.as_view(), name="verify"),
    path("unsubscribe", UnsubscribePageView.as_view(), name="unsubscribe"),


]