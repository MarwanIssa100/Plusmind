from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save
)
from django.utils.text import slugify
from .models import Post


@receiver(pre_save, sender=Post)
def blog_post_pre_save(sender, instance, *args, **kwargs):
    """Generate slug from title if not provided"""
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)
        print(f"Signal: Generated slug '{instance.slug}' for title '{instance.title}'")
    elif instance.slug and instance.title:
        print(f"Signal: Using existing slug '{instance.slug}' for title '{instance.title}'")
    else:
        print(f"Signal: No slug generated. Slug: '{instance.slug}', Title: '{instance.title}'")


@receiver(post_save, sender=Post)
def blog_post_post_save(sender, instance, created, *args, **kwargs):
    """Debug post-save signal"""
    if created:
        print(f"Post created: '{instance.title}' with slug: '{instance.slug}'")
    else:
        print(f"Post updated: '{instance.title}' with slug: '{instance.slug}'")
