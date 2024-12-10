# Generated by Django 5.0.6 on 2024-08-15 09:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_city', models.CharField(max_length=100)),
                ('to_city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField(default=django.utils.timezone.now)),
                ('available_seats', models.PositiveIntegerField(default=0)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.bus')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.route')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('is_booked', models.BooleanField(default=False)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.schedule')),
            ],
        ),
    ]
