from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Category
from django.db.models.signals import post_save

def send_notifications(preview, pk, article_title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'Text': preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=article_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=Category)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.news_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.article_title, subscribers)

# Приветственное сообщение новому пользователю
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать!'
        message = f"Добро пожаловать, {instance.username}!\n\nВсем спасибо! " \
                  f"i am glad!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])


User = get_user_model()


@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(sender, instance, created, **kwargs)