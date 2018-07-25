from django.db import models
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signal import object_viewed_signal
from .utils import get_clint_ip
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from account.signal import user_logged_in

User = settings.AUTH_USER_MODEL
# Create your models here.

FORCE_SESSION_TO_ONE = getattr(settings, "FORCE_SESSION_TO_ONE", False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, "FORCE_INACTIVE_USER_ENDSESSION", False)


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # User instance instance.id
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # product instance
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s viewed %s' % (self.content_object, self.timestamp)

    class Meta:
        get_latest_by = ['-analytic']
        verbose_name = "object viewed"
        verbose_name_plural = 'objects viewed'


def object_viewed_recevier(sender, instance, request, *args, **kwargs):
    # print("sender: ", sender)
    # print("instance: ", instance)
    # print("request: ", request)
    # print("request user: ", request.user)
    c_type = ContentType.objects.get_for_model(sender)  # instance.__class__  like it
    user = None
    if request.user.is_authenticated:
        user = request.user
    new_view_obj = ObjectViewed.objects.create(
        user=user,
        ip_address=get_clint_ip(request),
        content_type=c_type,
        object_id=instance.id
    )


object_viewed_signal.connect(object_viewed_recevier)


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    ip_address = models.CharField(max_length=200)
    session_key = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_reciver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_reciver, UserSession)


def post_save_user_changed_reciver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active is False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_reciver, sender=User)


def user_logged_in_reciver(sender, instance, request, *args, **kwargs):
    print(instance)
    user = instance
    ip_address = get_clint_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_reciver)




