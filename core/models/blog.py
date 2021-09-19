from django.db import models
from slugify import slugify
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_delete

def post_img_path(instance, filename):
    return 'posts/{0}/img/{1}'.format(slugify(instance.title), filename)

class PostCategory(models.Model):
    name = models.CharField(
        default='Undefined Post Category',
        max_length=100,
    )
    slug = models.CharField(
        default='undefined-post-category',
        max_length=500,
        editable=False,
    )

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.name)
        if not PostCategory.objects.filter(slug=self.slug).exists():
            super(PostCategory, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(PostCategory,related_name='posts', on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name='Title', max_length=100)
    image = models.ImageField(verbose_name='Image',upload_to=post_img_path, default='posts/default.jpg')
    date = models.DateTimeField(verbose_name='Date',default=timezone.now, editable=False)
    description = models.TextField(verbose_name='Description')
    text = models.TextField(verbose_name='Post Content')
    keywords = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return str(self.title) + '(' + str(self.date.date()) + ')'

    def get_absolute_url(self):
        return f'/blog/p/{self.id}/'

    __original_image = None

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.__original_image != self.image:
            if self.pk:
                self.__original_image.storage.delete(self.__original_image.path)
        super(Post, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

@receiver(pre_delete, sender=Post)
def delete_font_hook(sender, instance, using, **kwargs):
    try:
        instance.image.storage.delete(instance.image.path)
    except:
        pass