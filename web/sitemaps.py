from django.contrib.sitemaps import Sitemap
from core.models import *

class MainSitemap(Sitemap):

    location = "/"
    changefreq = "weekly"
    priority = 1

    def items(self):
      return [self]

class MainBlogSitemap(Sitemap):

    location = "blog/"
    changefreq = "weekly"
    priority = 1

    def items(self):
      return [self]

class PostCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return PostCategory.objects.all()

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date

class SketchSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.8

    def items(self):
        return Sketch.objects.filter(is_main=False).all()

class SketchMainSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.9

    def items(self):
        return Sketch.objects.filter(is_main=True).all()