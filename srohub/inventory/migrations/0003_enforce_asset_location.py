# Generated by Django 3.0.4 on 2020-03-05 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_add_root_assets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Asset'),
        ),
    ]