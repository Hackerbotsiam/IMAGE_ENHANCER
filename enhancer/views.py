import os
import uuid

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render
from PIL import Image, ImageFilter

from .forms import ImageUploadForm

PROCESSED_DIR = os.path.join(settings.MEDIA_ROOT, 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

SHARPEN_SETTINGS = {
    'none': None,
    'light': {'radius': 2, 'percent': 100, 'threshold': 3},
    'strong': {'radius': 2, 'percent': 180, 'threshold': 2},
}


def enhance_image(input_path, scale, sharpen_level):
    img = Image.open(input_path)

    if img.mode not in ('RGB', 'RGBA', 'L'):
        img = img.convert('RGB')

    new_size = (img.width * scale, img.height * scale)
    upscaled = img.resize(new_size, resample=Image.LANCZOS)

    sharpen_params = SHARPEN_SETTINGS.get(sharpen_level)
    if sharpen_params:
        upscaled = upscaled.filter(ImageFilter.UnsharpMask(**sharpen_params))

    output_filename = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join(PROCESSED_DIR, output_filename)
    upscaled.save(output_path, format='PNG')

    return output_filename, img.size, new_size

def upload_view(request):
    result = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            scale = int(form.cleaned_data['scale'])
            sharpen_level = form.cleaned_data['sharpen']

            temp_name = f"{uuid.uuid4().hex}_{uploaded_image.name}"
            temp_path = os.path.join(PROCESSED_DIR, temp_name)
            with open(temp_path, 'wb+') as dest:
                for chunk in uploaded_image.chunks():
                    dest.write(chunk)

            try:
                output_filename, original_size, new_size = enhance_image(temp_path, scale, sharpen_level)
                result = {
                    'processed_url': settings.MEDIA_URL + 'processed/' + output_filename,
                    'download_name': output_filename,
                    'original_size': original_size,
                    'new_size': new_size,
                }
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    else:
        form = ImageUploadForm()

    return render(request, 'enhancer/upload.html', {'form': form, 'result': result})


def download_view(request, filename):
    file_path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(file_path):
        raise Http404('File paoa jayni')
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)