# Generated by Django 3.2.16 on 2022-11-10 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Trooper', max_length=20, verbose_name='display name')),
                ('domain', models.URLField(help_text='The domain name associated with this website', verbose_name='domain name')),
                ('description', models.CharField(blank=True, help_text='A brief description of this Troop', max_length=255, verbose_name='description')),
                ('logo', models.ImageField(blank=True, help_text='A recognizable icon to visually identify your Troop', upload_to='img', verbose_name='logo')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configuration',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='website', verbose_name='file')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="The title of this page. Will be shown at the top of the page, in navigation, and in the browser's title bar.", max_length=100, verbose_name='title')),
                ('slug', models.SlugField(blank=True, help_text="The part of the page's URL that comes after the slash. Useful in providing meaningful links.", unique=True, verbose_name='slug')),
                ('is_builtin', models.CharField(blank=True, choices=[(None, 'custom webpage'), ('HOME', 'Home Page'), ('ABOUT', 'About Us'), ('CONTACT', 'Contact Form'), ('SIGNUP', 'Sign Up Form')], help_text='Some pages, such as the home page, require special treatment. If this is to be one of those special pages, you can specify it here.', max_length=7, null=True, unique=True, verbose_name='built-in page')),
                ('in_navbar', models.BooleanField(default=True, help_text="Determines whether this page should appear in the site's navigation bar.", verbose_name='include in navigation')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The date and time this page was first added to the database.', verbose_name='created')),
                ('last_modified', models.DateTimeField(auto_now=True, help_text='The date and time this page was last saved to the database.', verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.CharField(choices=[('ANONYMOUS', 'Anonymous/Guests'), ('PUBLIC', 'Everyone'), ('MEMBERS', 'Members Only')], default='MEMBERS', help_text='Controls who will be allowed to view this content.', max_length=9, verbose_name='visibility')),
                ('heading', models.CharField(blank=True, max_length=100, verbose_name='heading')),
                ('bookmark', models.SlugField(blank=True, help_text='Can be used to link directly to this content block on a webpage.', verbose_name='bookmark')),
                ('body', models.TextField(help_text='The main body of this content block', verbose_name='body')),
                ('images', models.ManyToManyField(blank=True, related_name='content', to='website.Image')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='website.page')),
            ],
            options={
                'verbose_name': 'Content Block',
                'verbose_name_plural': 'Content Blocks',
                'order_with_respect_to': 'page',
            },
        ),
    ]
