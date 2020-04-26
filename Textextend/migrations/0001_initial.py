# Generated by Django 2.2.4 on 2020-04-24 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventPositive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_id', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=400)),
                ('vector', models.BinaryField(null=True)),
                ('store_timestamp', models.BigIntegerField(null=True)),
                ('store_type', models.IntegerField(default=0)),
                ('process_status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'EventPositive',
            },
        ),
    ]