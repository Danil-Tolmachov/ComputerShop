# Generated by Django 4.1.2 on 2022-10-31 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=45)),
                ('category_slug', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('characteristics', models.JSONField(blank=True, null=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('is_available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=70)),
                ('address', models.CharField(max_length=255)),
                ('products', models.ManyToManyField(blank=True, to='cart.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='available_count',
            field=models.ManyToManyField(blank=True, to='cart.storage'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='cart.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.productimage'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('processed', 'Processed'), ('issued to the carrier', 'Issued to the carrier'), ('shipped', 'Shipped'), ('Finished', 'Finished')], default=('submitted', 'Submitted'), max_length=255)),
                ('status_comment', models.CharField(blank=True, max_length=255)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(to='cart.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='cart.product')),
            ],
        ),
    ]
