import hashlib
from datetime import datetime, timedelta
from django.core import serializers

from ..models.sketches import Sketch
from core.models import Font
from django.utils import timezone

def set_activity(sketch_id):
    sketch = Sketch.objects.filter(id=sketch_id).first()
    sketch.delete_date = timezone.now() + timedelta(days=90)
    sketch.save()

def default_hash(text, color, font_id):
    return hashlib.md5((text + color + font_id.__str__()).encode('utf-8')).hexdigest()

def check_sketch(text, color, font_id):
    hash = default_hash(text, color, font_id)
    if Sketch.objects.filter(hash=hash).exists():
        return True
    else:
        return False

def get_sketch(text, color, font_id):
    if check_sketch(text, color, font_id) == True:
        hash = default_hash(text, color, font_id)
        sketch = Sketch.objects.filter(hash=hash).first()
        set_activity(sketch.id)
        return serializers.serialize("json", [Sketch.objects.filter(hash=hash).first()])
    else:
        font = Font.objects.filter(id=font_id).first()
        sketch = Sketch.objects.create(text=text, color=color,font=font)
        hash = default_hash(text, color, font_id)
        return serializers.serialize("json", [Sketch.objects.filter(hash=hash).first()])