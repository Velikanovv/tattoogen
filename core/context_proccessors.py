from core.models import *
from django.utils import timezone
from django.contrib.sites.models import Site
from tattoogen import settings

def load_settings(request):
    try:
        year = timezone.now().year
        cs = ContentSettings.objects.first()
        socials = SocialMediaSetting.objects.all()
        domain = Site.objects.filter(pk=settings.SITE_ID).first().domain
        return {'cs': cs, 'socials': socials, 'domain': domain}
    except:
        return {'ok': 'ok'}
