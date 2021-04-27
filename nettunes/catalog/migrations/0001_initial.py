# Generated by Django 3.2 on 2021-04-27 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('num_owned', models.IntegerField()),
                ('num_available', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('rented_at', models.DateTimeField(null=True)),
                ('order', models.IntegerField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to=settings.AUTH_USER_MODEL)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='catalog.record')),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rented_at', models.DateTimeField(auto_now_add=True)),
                ('returned_at', models.DateTimeField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental', to=settings.AUTH_USER_MODEL)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental', to='catalog.record')),
            ],
        ),
    ]
