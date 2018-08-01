# Generated by Django 2.0.5 on 2018-06-03 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0003_merge_20180604_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicalPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(verbose_name='slug name')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='style_music',
            field=models.ManyToManyField(to='userauth.MusicalPreference'),
        ),
    ]