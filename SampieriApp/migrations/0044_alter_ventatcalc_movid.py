# Generated by Django 5.0.6 on 2024-08-08 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SampieriApp', '0043_alter_ventatcalc_empresa_alter_ventatcalc_sucursal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventatcalc',
            name='MovID',
            field=models.CharField(default=1, max_length=20),
        ),
    ]