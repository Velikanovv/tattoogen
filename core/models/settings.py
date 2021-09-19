from django.db import models
from slugify import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import random


def logo_header_path(instance, filename):
    return 'settings/logo_header/{0}'.format(filename)


def logo_footer_path(instance, filename):
    return 'settings/logo_footer/{0}'.format(filename)


class ContentSettings(models.Model):
    main_title = models.CharField(
        default='TATTOO GENERATOR',
        max_length=100,
    )
    instruction = models.TextField(
        blank=True,
    )
    logo_header = models.FileField(
        upload_to=logo_header_path,
    )
    logo_footer = models.FileField(
        upload_to=logo_footer_path,
    )

    def __str__(self):
        return 'Content Settings'

    __original_logo_header = None
    __original_logo_footer = None

    def __init__(self, *args, **kwargs):
        super(ContentSettings, self).__init__(*args, **kwargs)
        self.__original_logo_header = self.logo_header
        self.__original_logo_footer = self.logo_footer

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        cContentSettings = ContentSettings.objects.filter(id=self.id).first()
        if self.logo_header != self.__original_logo_header:
            if self.pk:
                self.__original_logo_header.storage.delete(self.__original_logo_header.path)
        if self.logo_footer != self.__original_logo_footer:
            if self.pk:
                self.__original_logo_footer.storage.delete(self.__original_logo_footer.path)
        super(ContentSettings, self).save(force_insert, force_update, *args, **kwargs)


@receiver(pre_delete, sender=ContentSettings)
def delete_font_hook(sender, instance, using, **kwargs):
    try:
        instance.logo_footer.storage.delete(instance.logo_footer.path)
    except:
        try:
            instance.logo_header.storage.delete(instance.logo_header.path)
        except:
            pass


def sms_file_path(instance, filename):
    return 'social_media_settings/icons/%s' % (filename)


class SocialMediaSetting(models.Model):
    file = models.FileField(verbose_name='Icon', help_text="Format: .svg | FlatIcon", upload_to=sms_file_path)
    url = models.URLField(verbose_name='Link', blank=True, null=True, help_text="URL")

    def __str__(self):
        return str(self.url)

    __original_file = None

    def __init__(self, *args, **kwargs):
        super(SocialMediaSetting, self).__init__(*args, **kwargs)
        self.__original_file = self.file

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        cSocialMediaSetting = SocialMediaSetting.objects.filter(id=self.id).first()
        if self.__original_file != self.file:
            if self.pk:
                self.__original_file.storage.delete(self.__original_file.path)
        super(SocialMediaSetting, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = 'Social'
        verbose_name_plural = 'Socials'


@receiver(pre_delete, sender=SocialMediaSetting)
def delete_font_hook(sender, instance, using, **kwargs):
    try:
        instance.file.storage.delete(instance.file.path)
    except:
        pass
