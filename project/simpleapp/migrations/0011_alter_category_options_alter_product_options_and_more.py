# Generated by Django 4.2 on 2023-06-01 17:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simpleapp', '0010_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Subscription', 'verbose_name_plural': 'Subscriptions'},
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(help_text='Price should be >= 0.0', validators=[django.core.validators.MinValueValidator(0.0, 'Price should be >= 0.0')], verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(help_text='Quantity should be >= 0', validators=[django.core.validators.MinValueValidator(0, 'Quantity should be >= 0')], verbose_name='Quantity'),
        ),
    ]
