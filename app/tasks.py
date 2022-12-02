# Celery
from celery.task import periodic_task
from celery.schedules import crontab 
# Email sender
from django.core.mail import EmailMessage
from newsapi import NewsApiClient
# Project
from .models import Email
from django.conf import settings

newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

@periodic_task(run_every=crontab(minute=0, hour=12))  # excute every day at 12 PM
def send_daily_news_to_subscribers():
    """Sends an email every day with latest news to all subscribers."""
    top_headlines = newsapi.get_top_headlines(country='eg', category= "general",language='ar', page_size=1)
    articles =top_headlines['articles']
    emails = Email.objects.filter(is_verified=True).values_list('email', flat=True)
    email = EmailMessage(
        subject = f'Daily News {articles[0]["title"]}',
        body = articles[0]['description'],
        from_email = 'sender.mail.rana@gmail.com',
        to = emails
    )
    email.send()

    