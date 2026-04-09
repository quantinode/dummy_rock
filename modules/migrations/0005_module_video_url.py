from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0004_learningresource'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='video_url',
            field=models.URLField(blank=True, help_text='YouTube embed URL or direct video URL for the module intro video', max_length=500),
        ),
    ]
