# Generated by Django 5.0.5 on 2024-05-09 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_fooditem_image2_fooditem_image3'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeatureProduct',
        ),
    ]