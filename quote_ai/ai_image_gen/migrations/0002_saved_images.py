# Generated by Django 3.2.4 on 2023-05-11 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ai_image_gen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saved_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ai_image_url', models.URLField(max_length=500)),
                ('prompt', models.TextField(max_length=500)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_image', to='ai_image_gen.quotes')),
            ],
        ),
    ]