from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(_('image'), upload_to="img_users")

    def image_(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150"/></a>'.format(self.image.url))
        else:
            return '(Нет аватарки)'

    image_.short_description = 'Аватарка'
    image_.allow_tags = True

