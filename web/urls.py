from django.urls import path

from . import views

urlpatterns = [
    path('', views.main.index, name='index'),
    path('sketch/<slug:hash>/', views.main.sketch, name='sketch'),
    path('blog/', views.blog.index, name='blog-index'),
    path('blog/c/<slug:slug>/', views.blog.index_cat, name='blog-index-cat'),
    path('blog/p/<int:pk>/', views.blog.post, name='blog-post'),
]