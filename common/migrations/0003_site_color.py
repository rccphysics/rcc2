# Generated by Django 2.0.6 on 2018-07-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20180712_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
