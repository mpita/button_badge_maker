import os

from django.contrib import admin
from .models import Chapas

from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.encoding import smart_str

from django.contrib.admin.options import (
    unquote,
    csrf_protect_m,
    HttpResponseRedirect,
)

from xhtml2pdf import pisa

from PIL import Image, ImageDraw
import numpy as np

def add_corners(path_img):
    # Open the input image as numpy array, convert to RGB
    img=Image.open(path_img).convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))
    rename, ext = path_img.split(".")
    new_name = f"{rename}__circle.png"

    # Save with alpha
    Image.fromarray(npImage).save(new_name)
    return new_name


@admin.register(Chapas)
class Admin(admin.ModelAdmin):
    change_form_template = 'chapa/admin_change_form_chapa.html'

    list_display = (
        "name",
        "diameter"
    )

    actions = ["download"]

    def download(self, request, queryset):
        height_pixel_max = 1054
        width_pixel_max = 816
        template = get_template("pdf.html")
        if isinstance(queryset, list):
            diameter = queryset[0].diameter
            image = os.path.join(settings.BASE_DIR.__str__(), queryset[0].image.crop[f"{diameter}x{diameter}"].url[1:])
        else:
            diameter = queryset.diameter
            image = os.path.join(settings.BASE_DIR.__str__(), queryset.image.crop[f"{diameter}x{diameter}"].url[1:])
        im = add_corners(image)
        html = template.render({
            "image": im,
            "range_y": range(int(height_pixel_max/diameter)),
            "range_x": range(int(width_pixel_max/diameter)),
        })
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=download.pdf"
            return response
        return None
    
    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == 'POST' and 'download' in request.POST:
            obj = self.get_object(request, unquote(object_id))
            return self.download(request, obj)

        return admin.ModelAdmin.changeform_view(
            self, request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context,
        )