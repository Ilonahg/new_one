from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
    ]
