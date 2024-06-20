import datetime
import time

from .validation import WantResultContactsValidator
from ..models import RatioOfProjectsFromWRToSZ, WantResultContacts

from ..services import exceptions


def get_or_create_or_update_contact(validated_contact: WantResultContactsValidator, slug):
    project_id = get_project_id(slug)
    contact, created = WantResultContacts.objects.get_or_create(
        project_id=project_id,
        phones_first=validated_contact.phones_first,
        phones_second=validated_contact.phones_second,
        phones_third=validated_contact.phones_third,
        defaults=validated_contact.dict(),
    )
    if created:
        return contact
    if not was_contact_added_in_a_week(contact):
        contact.time = int(time.time())
        contact.save()
        return contact
    raise exceptions.ContactIsDoubleError(
        f"Контакт {validated_contact.phones_first} уже добавлен в проект {project_id} {datetime.datetime.fromtimestamp(contact.time).strftime('%d.%m.%Y %H:%M:%S')}"
    )


def was_contact_added_in_a_week(contact: WantResultContacts) -> bool:
    seconds_per_week = 60 * 60 * 24 * 7
    return int(time.time()) - contact.time < seconds_per_week


def get_project_id(slug: str):
    project_id = RatioOfProjectsFromWRToSZ.objects.get(slug=slug).project_id
    return project_id
