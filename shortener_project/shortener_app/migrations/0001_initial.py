# Generated by Django 4.0 on 2022-01-03 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_url', models.URLField(max_length=500)),
                ('created_by_id', models.PositiveIntegerField(default=0)),
                ('short_url', models.SlugField(max_length=6, unique=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('used_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['creation_date'],
            },
        ),
    ]
