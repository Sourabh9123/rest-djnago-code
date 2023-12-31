# Generated by Django 4.2.5 on 2023-10-26 13:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0003_order_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('payment_id', models.CharField(max_length=254)),
                ('order_id', models.CharField(max_length=254)),
                ('signature', models.CharField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
