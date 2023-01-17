# Generated by Django 4.1.4 on 2023-01-14 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_remove_post_tags_tag_post"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tag",
            name="post",
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(to="blog.tag"),
        ),
    ]
