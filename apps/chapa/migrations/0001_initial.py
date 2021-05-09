# Generated by Django 3.2.2 on 2021-05-09 15:07

import django.core.validators
from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('diameter', models.PositiveSmallIntegerField(help_text='value in pixel, max. 816', validators=[django.core.validators.MaxValueValidator(816)], verbose_name='Diameter')),
                ('image', versatileimagefield.fields.VersatileImageField(height_field='height', upload_to='img', width_field='width')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
            ],
            options={
                'verbose_name': 'Button Badge',
                'verbose_name_plural': 'Buttons Badges',
            },
        ),
    ]
