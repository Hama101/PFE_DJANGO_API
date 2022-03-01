import string

import random 
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
    
    


import random

def create_new_ref_number():
      return str(random.randint(10000, 99999))
    
    
    
#    from django.db import models

# from django.db.models.signals import pre_save, post_save

# from admission.utils import unique_slug_generator
# STATUS_CHOICES = (
#     ('draft', 'Draft'),
#     ('published', 'Published'),
# )


# class Post(models.Model):
#     title = models.CharField(max_length=250)
#     slug = models.SlugField(max_length=250, null=True, blank=True)
#     #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
#     text = models.TextField()
#     published_at = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     status = models.CharField(
#         max_length=10, choices=STATUS_CHOICES, default='draft')

#     class Meta:
#         ordering = ('-published_at',)

#     def __str__(self):
#         return self.title


# def rl_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)


# pre_save.connect(rl_pre_save_receiver, sender=Post)


# def detail(request, slug):

#     q = Post.objects.filter(slug__iexact=slug)
#     if q.exists():
#         q = q.first()
#     else:
#         return HttpResponse('<h1>Post Not Found</h1>')
#     context = {

#         'post': q
#     }
#     return render(request, 'posts/details.html', context)
    
