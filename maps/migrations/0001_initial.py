# Generated by Django 5.0.7 on 2024-07-21 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=20, max_digits=23)),
                ('longitude', models.DecimalField(decimal_places=20, max_digits=24)),
                ('place_type', models.CharField(max_length=10)),
            ],
        ),
    ]