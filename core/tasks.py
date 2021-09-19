from tattoogen.celery import app
from core.services import font_downloaded
from core.services import set_activity
from core.models import Sketch
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date
import shutil
from tattoogen import settings

@app.task
def new_font_download(font_id):
    font_downloaded(font_id)

@app.task
def set_activity_to_sketch(sketch_id):
    set_activity(sketch_id)

@app.task
def delete_old_sketches():
    today = date.today()
    for sketch in Sketch.objects.filter(is_main=False, delete_date__contains=today):
        hash = sketch.hash
        sketch.delete()
        shutil.rmtree(settings.MEDIA_ROOT + '/sketches/' + hash)

