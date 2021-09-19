from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

@admin.register(FontCategory)
class FontCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ('name', 'open', 'category', 'language_type', 'downloads')
    list_filter = ('open', 'category', 'language_type')

@admin.register(Sketch)
class SketchAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_main', 'font', 'color','link')
    list_filter = ('is_main', 'font')

@admin.register(ContentSettings)
class ContentSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(SocialMediaSetting)
class SocialMediaSettingAdmin(admin.ModelAdmin):
    pass

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    pass

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Post Content', widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    readonly_fields = ('date',)
    form = PostAdminForm