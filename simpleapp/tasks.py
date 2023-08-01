from celery import shared_task
import datetime
from django.core.mail import EmailMultiAlternatives
import project
from project import settings
from project.settings import DEFAULT_FROM_EMAIL

from .models import Category, News
from django.template.loader import render_to_string


@shared_task
def mailing():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Category.objects.filter(datetime__gte=last_week)
    categories = set(posts.values_list('dopCategory__categories', flat=True))
    subscribers = set(Category.objects.filter(categories__in=categories).values_list('subscribers__email', flat=True))
    html_contex = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Лучшее',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_contex, 'news.html')
    msg.send()


@shared_task
def send_notifications(pk):
    post = Category.objects.get(pk=pk)
    categories = post.dopCategory.all()
    title = post.heading
    subscribers: list[str] = []
    for category in categories:
        subscribers_user = category.subscribers.all()
        for user in subscribers_user:
            subscribers.append(user.email)
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': News.models.Post.preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()