from django.contrib.sitemaps import Sitemap
from core.models import *

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date

class SketchSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Sketch.objects.filter(is_main=False).all()

class SketchMainSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1

    def items(self):
        return Sketch.objects.filter(is_main=True).all()