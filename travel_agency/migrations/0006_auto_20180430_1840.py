# Generated by Django 2.0.3 on 2018-04-30 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_agency', '0005_amenities_wifi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='location',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='number',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]