# Django libraries
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
# Email sender
from .models import Email
from django.core.mail import EmailMessage
from newsapi import NewsApiClient
# Math libraries
from random import randint
# Redis
import redis

newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)
r = redis.StrictRedis()

def random_with_digits(n):
    """Create six random integer digits to make verification code."""
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class HomePageView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        if Email.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return render(request, self.template_name)
        random = random_with_digits(6)
        email_sender = EmailMessage(
        subject = 'Verify Email',
        body = f'Your verification code is: {random}',
        from_email = 'sender.mail.rana@gmail.com',
        to = [email]
        )
        email_sender.send()
        r.set(email, random)
        r.expire(email, 900) # expire after 15 min.
        request.session['email'] = email
        return HttpResponseRedirect('verify')

class VerifyPageView(TemplateView):
    template_name = "verify.html"
    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER')
        if not referer:
            raise Http404
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        code = int(request.POST['code'])
        if r.exists(email):
            pin = int(r.get(email))
            if pin == code:
                if not Email.objects.filter(email=email).exists():
                    user = Email.objects.create(email=email)
                    user.is_verified = True
                    user.save()
                    del request.session['email']
                    messages.add_message(request, messages.INFO, 'Your email has been successfully subscribed.')
                    return HttpResponseRedirect(reverse("home"))
                else:
                    user = Email.objects.get(email=email)
                    user.is_verified = False
                    user.save()
                    del request.session['email']
                    messages.add_message(request, messages.INFO, 'Your email has been unsubscribed.')
                    return HttpResponseRedirect(reverse("home"))
            else: 
                messages.warning(request, 'Invalid code!')
        else:
            messages.warning(request, 'Verification code has been expired! Try to subscribe again.')
        return render(request, self.template_name)

class UnsubscribePageView(View):
    template_name = "unsubscribe.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        if not Email.objects.filter(email=email).exists():
            messages.warning(request, 'Email not exists!')
            return render(request, self.template_name)
        user = Email.objects.get(email=email)
        if not user.is_verified:
            messages.warning(request, 'Email already has been unsbuscribed!')
            return render(request, self.template_name)
        random = random_with_digits(6)
        email_sender = EmailMessage(
        subject = 'Unsbuscribe us',
        body = f'Your verification code is: {random}',
        from_email = 'sender.mail.rana@gmail.com',
        to = [email]
        )
        email_sender.send()
        r.set(email, random)
        r.expire(email, 900) # expire after 15 min.
        request.session['email'] = email
        return HttpResponseRedirect('verify')


def error_404(request, exception):
    return render(request, '404.html')

    

