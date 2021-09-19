import os
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
from django.db.models import DEFERRED


class FontCategory(models.Model):
    name = models.CharField(
        default='Undefined Category',
        max_length=100,
    )

    def __str__(self):
        return self.name


def font_upload_path(instance, filename):
    filename = slugify(filename.split('.')[0]) + '-{0}'.format(slugify(instance.name)) + '.' + filename.split('.')[-1]
    return 'fonts/{0}/font/{1}'.format(slugify(instance.name), filename)


def font_image_upload_path(instance, filename):
    filename = slugify(filename.split('.')[0]) + '-{0}'.format(slugify(instance.name)) + '.' + filename.split('.')[-1]
    return 'fonts/{0}/image/{1}'.format(slugify(instance.name), filename)


def create_font_image(text, font_path, color):
    img = Image.new('RGB', (10, 10), ('#FFFFFF'))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=50)
    d.text((1, 1), text, font=font, fill=(color), align='center')
    text_width, text_height = d.textsize(text, font=font)
    tw = text_width + 2
    th = text_height + 2
    size = tw, th
    img = Image.new('RGB', (tw, th), ('#FFFFFF'))
    d = ImageDraw.Draw(img)
    d.text((1, 1), text, font=font, fill=(color), align='center')

    buffer = BytesIO()
    img.save(fp=buffer, format='JPEG', subsampling=0, quality=90)
    return ContentFile(buffer.getvalue())


class Font(models.Model):
    class Languages(models.TextChoices):
        ENGLISH = 'En', _('En')
        ENGLISH_AND_RUSSIAN = 'En_Ru', _('En/Ru')

    category = models.ForeignKey(
        FontCategory,
        null=True,
        related_name='font_category',
        on_delete=models.SET_NULL,
    )
    name = models.CharField(
        default='Undefined Name',
        max_length=100,
    )
    language_type = models.CharField(
        max_length=10,
        choices=Languages.choices,
        default=Languages.ENGLISH,
    )
    image = models.ImageField(
        null=True,
        blank=True,
        editable=False,
        upload_to=font_image_upload_path,
    )
    file = models.FileField(
        upload_to=font_upload_path,
    )
    open = models.BooleanField(
        default=True
    )
    downloads = models.IntegerField(
        default=random.randint(15,50)
    )

    def __str__(self):
        return self.id.__str__() + ' : ' + self.name

    __original_file = None

    def __init__(self, *args, **kwargs):
        super(Font, self).__init__(*args, **kwargs)
        self.__original_file = self.file

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        cfont = Font.objects.filter(id=self.id).first()
        if self.pk:
            if self.__original_file != self.file:
                self.__original_file.storage.delete(self.__original_file.path)
            cfont.image.storage.delete(cfont.image.path)
            cs = create_font_image('Tattoo Generator', self.file, '#000000')
            self.image = InMemoryUploadedFile(
            cs,  # file
            None,  # field_name
            'jpg',  # file name
            'image/jpeg',  # content_type
            cs,  # size
            None)
        else:
            cs = create_font_image('Tattoo Generator', self.file, '#000000')
            self.image = InMemoryUploadedFile(
            cs,  # file
            None,  # field_name
            'jpg',  # file name
            'image/jpeg',  # content_type
            cs,  # size
            None)
        super(Font, self).save(force_insert, force_update, *args, **kwargs)

@receiver(pre_delete, sender=Font)
def delete_font_hook(sender, instance, using, **kwargs):
    try:
        instance.file.storage.delete(instance.file.path)
    except:
        try:
            instance.image.storage.delete(instance.image.path)
        except:
            pass

