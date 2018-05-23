# Generated by Django 2.0.5 on 2018-05-22 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(0, '------'), (1, 'Male'), (2, 'Female'), (3, 'Other')], default=0, verbose_name='gender'),
        ),
    ]
