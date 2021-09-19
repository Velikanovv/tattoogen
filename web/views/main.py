from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from core.services import *
from core.tasks import new_font_download, set_activity_to_sketch


def index(request):
    if request.method == 'GET':
        categories = FontCategory.objects.all()
        af = request.session.get('af', '0')
        return render(
            request,
            'main/index.html',
            {
                'categories': categories,
                'af': af
            }
        )
    if request.method == 'POST':
        if request.POST['action'] == 'getfonts':
            af = request.session.get('af', '0')
            try:
                fonts = serializers.serialize("json", Font.objects.all())
                count = Font.objects.all().count()
                return JsonResponse({'font_count': count, 'fonts': fonts, 'af': af}, status=200)
            except Exception as e:
                return JsonResponse({'errors': e.args[0]}, status=400)
        if request.POST['action'] == 'getfonts_cats':
            af = request.session.get('af', '0')
            try:
                all_fonts = None
                cats = FontCategory.objects.all()
                on_cats = []
                all = True
                for cat in cats:
                    if request.POST['cats[' + cat.id.__str__() + ']'] == 'on':
                        all = False
                        on_cats.append(cat.id)
                if all == False:
                    fonts = serializers.serialize("json", Font.objects.filter(category__id__in=on_cats))
                    count = Font.objects.filter(category__id__in=on_cats).count()
                else:
                    fonts = serializers.serialize("json", Font.objects.all())
                    count = Font.objects.all().count()
                return JsonResponse({'font_count': count, 'fonts': fonts,'af': af}, status=200)
            except Exception as e:
                return JsonResponse({'errors': e.args[0]}, status=400)
        if request.POST['action'] == 'get_img':
            af = request.session.get('af', '0')
            try:
                text = request.POST['text']
                if request.POST['text'].replace(' ', '') == '':
                    text = 'empty'
                color = request.POST['color']
                font_id = request.POST['font_id']
                sketch = get_sketch(text, color, font_id)
                if not Font.objects.get(id=font_id).open and af == '0':
                    return JsonResponse({'errors': 'You have no Permissions'}, status=400)
                return JsonResponse({'sketch': sketch, 'af': af}, status=200)
            except Exception as e:
                return JsonResponse({'errors': e.args[0]}, status=400)
        if request.POST['action'] == 'dwnld':
            try:
                new_font_download.delay(request.POST['font_id'])
                return JsonResponse({}, status=200)
            except Exception as e:
                return JsonResponse({'errors': e.args[0]}, status=400)
        if request.POST['action'] == 'acceptFonts':
            try:
                request.session['af'] = '1'
                request.session.modified = True
                return JsonResponse({}, status=200)
            except Exception as e:
                return JsonResponse({'errors': e.args[0]}, status=400)


def sketch(request, hash):
    if request.method == 'GET':
        af = request.session.get('af', '0')
        categories = FontCategory.objects.all()
        sketch = Sketch.objects.filter(hash=hash)
        if sketch.exists():
            sketch = sketch.first()
            set_activity_to_sketch.delay(sketch.id)
            return render(
                request,
                'main/sketch.html',
                {
                    'sketch': sketch,
                    'af': af
                }
            )
        else:
            return redirect(index)
    if request.method == 'POST':
        af = request.session.get('af', '0')
        if request.POST['action'] == 'get_img':
            try:
                text = request.POST['text']
                if request.POST['text'].replace(' ', '') == '':
                    text = 'empty'
                color = request.POST['color']
                font_id = request.POST['font_id']
                sketch = get_sketch(text, color, font_id)
                return JsonResponse({'sketch': sketch, 'af': af}, status=200)
            except Exception as e:
                return JsonResponse({'errors': e.args[0]}, status=400)
