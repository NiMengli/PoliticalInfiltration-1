# Generated by Django 2.2.4 on 2020-04-10 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainevent', '0018_event_count_max'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_analyze',
            name='figure_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event_analyze',
            name='info_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='figure',
            name='event_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='figure',
            name='figure_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]