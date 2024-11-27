from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from a_user_management.models import Owner, Manager, Employee, Teacher
from django.db import transaction


@receiver(post_save, sender=Owner)
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:  # Only assign the group when the user is first created
        def assign_group():
            group, _ = Group.objects.get_or_create(name='مالک')  # Ensure the group exists
            instance.groups.add(group)

        transaction.on_commit(assign_group)  # Delay assignment until the transaction is committed


@receiver(post_save, sender=Teacher)
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:  # Only assign the group when the user is first created
        def assign_group():
            group, _ = Group.objects.get_or_create(name='استاد')  # Ensure the group exists
            instance.groups.add(group)

        transaction.on_commit(assign_group)  # Delay assignment until the transaction is committed

@receiver(post_save, sender=Manager)
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:  # Only assign the group when the user is first created
        def assign_group():
            group, _ = Group.objects.get_or_create(name='مدیر')  # Ensure the group exists
            instance.groups.add(group)

        transaction.on_commit(assign_group)  # Delay assignment until the transaction is committed

@receiver(post_save, sender=Employee)
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:  # Only assign the group when the user is first created
        def assign_group():
            group, _ = Group.objects.get_or_create(name='کارمند')  # Ensure the group exists
            instance.groups.add(group)

        transaction.on_commit(assign_group)  # Delay assignment until the transaction is committed