# Generated by Django 2.0.3 on 2018-03-14 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0007_auto_20180314_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Area'),
        ),
    ]