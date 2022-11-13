# Generated by Django 4.1.2 on 2022-11-02 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_order_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('SUBMITTED', 'Submitted'), ('PROCEED', 'Processed'), ('ISSUED TO THE CARRIER', 'Issued to the carrier'), ('Shipped', 'Shipped'), ('Finished', 'Finished')], default='SUBMITTED', max_length=255),
        ),
    ]