from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import CVDoc


@receiver(post_save, sender=CVDoc)
def create_avatar_thumbnail_on_save(sender, instance, **kwargs):
    if instance.avatar:
        instance.make_thumbnail()


@receiver(post_delete, sender=CVDoc)
def delete_avatar_files_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        instance.delete_avatar_files()


@receiver(pre_save, sender=CVDoc)
def delete_old_avatar_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip for new instances

    try:
        old = CVDoc.objects.get(pk=instance.pk)
    except CVDoc.DoesNotExist:
        return

    # If avatar is changed, delete old avatar
    if old.avatar and old.avatar != instance.avatar:
        old.delete_avatar_files()
