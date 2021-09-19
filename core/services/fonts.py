from core.models import Font, FontCategory

def font_downloaded(font_id):
    font = Font.objects.filter(id=font_id).first()
    font.downloads += 1
    font.save()