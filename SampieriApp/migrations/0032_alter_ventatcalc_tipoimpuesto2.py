# Generated by Django 5.0.6 on 2024-08-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SampieriApp', '0031_alter_ventatcalc_renglontipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventatcalc',
            name='TipoImpuesto2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]