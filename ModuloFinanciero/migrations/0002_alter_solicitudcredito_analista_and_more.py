# Generated by Django 4.0.4 on 2022-04-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ModuloFinanciero', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcredito',
            name='analista',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitudcredito',
            name='estudiante',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]