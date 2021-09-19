from core.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import random
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime as DT
from decimal import Decimal
from django.core import serializers

def index(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('date')
        categories = PostCategory.objects.all()
        return render(
            request,
            'main/blog.html',
            {
                'posts': posts,
                'categories': categories,
            }
        )

def index_cat(request, slug):
    if request.method == 'GET':
        cat = PostCategory.objects.filter(slug=slug).first()
        posts = Post.objects.filter(category=cat).order_by('date')
        categories = PostCategory.objects.all()
        return render(
            request,
            'main/blog-cat.html',
            {
                'posts': posts,
                'categories': categories,
                'cc': cat,
            }
        )

def post(request, pk):
    if request.method == 'GET':
        post = Post.objects.filter(pk=pk).first()
        return render(
            request,
            'main/article.html',
            {
                'post': post,
            }
        )