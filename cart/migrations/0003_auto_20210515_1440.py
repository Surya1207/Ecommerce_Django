# Generated by Django 3.1.1 on 2021-05-15 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20210513_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_name', models.CharField(help_text='Required', max_length=255, verbose_name='delivery_name')),
                ('delivery_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 999.99', max_digits=5, verbose_name='delivery price')),
                ('delivery_method', models.CharField(choices=[('IS', 'In Store'), ('HD', 'Home Delivery'), ('DD', 'Digital Delivery')], help_text='Required', max_length=255, verbose_name='delivery_method')),
                ('delivery_timeframe', models.CharField(help_text='Required', max_length=255, verbose_name='delivery timeframe')),
                ('delivery_window', models.CharField(help_text='Required', max_length=255, verbose_name='delivery window')),
                ('order', models.IntegerField(default=0, help_text='Required', verbose_name='list order')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Delivery Option',
                'verbose_name_plural': 'Delivery Options',
            },
        ),
        migrations.CreateModel(
            name='PaymentSelections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='name')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Payment Selection',
                'verbose_name_plural': 'Payment Selections',
            },
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.order'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='state',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='zipcode',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
