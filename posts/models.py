from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from tinymce import models as tinymce_models
from django.core.validators import RegexValidator
import uuid
import hashlib
# Create your models here.
# TODO: Add tags views upvotes downvotes stars author edited by
# TODO: Add suggestion for clubbing similar tags


class CaseInsensitiveFieldMixin:
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }

    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass


class Tag(models.Model):
    tag_name = CICharField(
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


def generate_hash(mail):
    salt = uuid.uuid4().hex
    hashed_mail = hashlib.sha3_256(mail.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_mail


class UserMailIdMap(models.Model):
    email = models.EmailField(max_length=100,
                              blank=False,
                              unique=True)
    email_hash = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        self.email_hash = generate_hash(self.email)
        super(UserMailIdMap, self).save(*args, **kwargs)


class SubscribedUsers(models.Model):
    DAILY = 'D'
    WEEKLY = 'W'
    MONTHLY = 'M'
    YEARLY = 'Y'
    FREQUENCY_CHOICES = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    )
    email = models.EmailField(max_length=100,
                              blank=False,
                              unique=True,
                              error_messages={'unique': "You are already subscribed"})
    frequency = models.CharField(
                                max_length=2,
                                choices=FREQUENCY_CHOICES,
                                default=DAILY,
                                )
    tags_followed = models.ManyToManyField(Tag)
