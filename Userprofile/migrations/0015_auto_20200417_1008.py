# Generated by Django 2.2.4 on 2020-04-17 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userprofile', '0014_auto_20200222_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='geo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
