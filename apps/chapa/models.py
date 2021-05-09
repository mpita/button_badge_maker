import os

from django.db import models
from versatileimagefield.fields import PPOIField, VersatileImageField
from django.core.validators import MaxValueValidator, ValidationError


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path filename
    valid = ['.jpg', '.jpeg']
    if ext not in valid:
        raise ValidationError("Unsupported file extension.")


class Chapas(models.Model):
    name = models.CharField("Name", max_length=50)
    diameter = models.PositiveSmallIntegerField(
        "Diameter",
        validators=[
            MaxValueValidator(816),
        ],
        help_text='value in pixel, max. 816',
    )
    image = VersatileImageField(
        upload_to="img",
        ppoi_field="ppoi",
        blank=False,
        help_text='only image with extension .jpeg o .jpg',
        validators=[
            validate_extension,
        ],
    )
    ppoi = PPOIField()

    class Meta:
        verbose_name = "Button Badge"
        verbose_name_plural = "Buttons Badges"

    def __str__(self):
        return self.name
