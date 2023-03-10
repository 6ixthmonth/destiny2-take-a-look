# Generated by Django 4.1.5 on 2023-02-21 08:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_hash', models.BigIntegerField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=255)),
                ('icon_url', models.CharField(max_length=2083)),
                ('character_class', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('vendor_hash', models.BigIntegerField(primary_key=True, serialize=False)),
                ('vendor_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SalesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('mobility', models.PositiveSmallIntegerField(default=0)),
                ('resilience', models.PositiveSmallIntegerField(default=0)),
                ('recovery', models.PositiveSmallIntegerField(default=0)),
                ('discipline', models.PositiveSmallIntegerField(default=0)),
                ('intellect', models.PositiveSmallIntegerField(default=0)),
                ('strength', models.PositiveSmallIntegerField(default=0)),
                ('item_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='d2api.item')),
                ('vendor_hash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='d2api.vendor')),
            ],
        ),
    ]
