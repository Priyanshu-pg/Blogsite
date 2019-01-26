from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models
from django.core.validators import RegexValidator
# Create your models here.

# TODO: Add tags views upvotes downvotes stars author edited by

class Tag(models.Model):
    tag_name = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9a-zA-Z ]+$',
                message='Can contain only alphabets, numerals or -',
                code='invalid_tagname'
            ),
        ]
    )

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse('tag-archive', args=[self.tag_name])


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, unique=True, default="slug")
    subtitle = models.TextField()
    content = tinymce_models.HTMLField('Content')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.create_time.year, '{:02d}'.format(self.create_time.month), self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['create_time']

