from django.db import models
from ..models import Font
from slugify import slugify
import hashlib
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from tattoogen import settings
from django.core.exceptions import ValidationError, FieldError
from django.utils.translation import gettext_lazy as _
import random
import re
from django.contrib.sites.models import Site


def sketch_image_upload_path(instance, filename):
    filename = '{0}'.format(instance.hash) + '.' + filename.split('.')[-1]
    return 'sketches/{0}/image/{1}'.format(instance.hash, filename)


def default_hash(text, color, font_id):
    return hashlib.md5((text + color + font_id.__str__()).encode('utf-8')).hexdigest()


def default_slug(text):
    return slugify(text)

def create_sketch(text, font_path, color):
    img = Image.new('RGB', (10, 10), ('#FFFFFF'))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=100)
    d.text((50, 50), text, font=font, fill=(color), align='center')
    text_width, text_height = d.textsize(text, font=font)
    tw = text_width + 100
    th = text_height + 100
    size = tw, th
    img = Image.new('RGB', (tw, th), ('#FFFFFF'))
    d = ImageDraw.Draw(img)
    d.text((50, 50), text, font=font, fill=(color), align='center')

    buffer = BytesIO()
    img.save(fp=buffer, format='JPEG', subsampling=0, quality=100)
    return ContentFile(buffer.getvalue())


class Sketch(models.Model):
    is_main = models.BooleanField(
        default=False,
    )
    delete_date = models.DateField(
        null=True,
        editable=False
    )
    font = models.ForeignKey(
        Font,
        on_delete=models.CASCADE,
    )
    hash = models.CharField(
        unique=True,
        max_length=100,
        editable=False
    )
    text = models.CharField(
        default='Undefined Sketch',
        max_length=1000,
    )
    color = models.CharField(
        default='#000000',
        max_length=7,
    )
    image = models.ImageField(
        blank=True,
        upload_to=sketch_image_upload_path,
        editable=False
    )
    link = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        editable=False
    )
    title_part = models.CharField(
        max_length=200,
        default='Tattoo',
    )
    keywords = models.CharField(
        max_length=2000,
        blank=True,
        editable=False,
    )

    def get_absolute_url(self):
        return f'/sketch/{self.hash}/'

    __original_image = None

    def __init__(self, *args, **kwargs):
        super(Sketch, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.pk:
            self.__original_image.storage.delete(self.__original_image.path)
        self.hash = default_hash(self.text, self.color, self.font.id)
        cs = create_sketch(self.text, self.font.file.path, self.color)
        self.image = InMemoryUploadedFile(
            cs,  # file
            None,  # field_name
            'jpg',  # file name
            'image/jpeg',  # content_type
            cs,  # size
            None)
        self.link = 'http://' + Site.objects.filter(pk=settings.SITE_ID).first().domain + '/sketch/' + self.hash + '/'
        if not self.id:
            self.delete_date = timezone.now() + timedelta(days=90)
            titles = ['Tattoo', 'Lettering tattoo', 'Script tattoo','Font tattoo', 'Tattoo designs', 'Letters font', 'Font style', 'Free tattoo font']
            self.title_part = random.choice(titles)
            kw = re.findall(r"[\w']+|[.,!?;_]", self.text)
            keywords = ''
            for k in kw:
                if k != '.' and k != ',' and k != '!' and k != '?' and k != ';' and k != '_':
                    keywords = keywords + k + ', '
            keywords = keywords + 'Tattoo, Lettering tattoo, Script tattoo, Font tattoo, Tattoo designs, Letters font, Font style, Free tattoo font'
            self.keywords = keywords
        if Sketch.objects.filter(hash=self.hash).exists() and not self.pk:
            raise ValidationError(_('The same sketch is already exists.'))
        else:
            super(Sketch, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.text

@receiver(pre_delete, sender=Sketch)
def delete_font_hook(sender, instance, using, **kwargs):
    try:
        instance.image.storage.delete(instance.image.path)
    except:
        pass

