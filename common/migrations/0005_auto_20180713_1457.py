# Generated by Django 2.0.6 on 2018-07-13 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20180712_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
