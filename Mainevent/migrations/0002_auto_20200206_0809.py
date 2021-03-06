# Generated by Django 2.2.4 on 2020-02-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainevent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='comment',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='geo',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='i_level',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='keywords_dict',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='message_type',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='retweeted',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='root_mid',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='send_ip',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='source',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='text',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='information',
            name='timestamp',
            field=models.BigIntegerField(null=True),
        ),
    ]
