import json

import redis
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from ..api import serializers
from ..services.skorozvon import skorozvon_api
from ..services.validation import WantResultContactsValidator
from ..services.db import get_project_id, get_or_create_or_update_contact

from ..services.logger import log_response_want_result


@shared_task(bind=True, max_retries=3, default_retry_delay=1)
def task_resending_a_contact_to_sz(self, slug: str, request_data: dict):
    validated_contact = get_validate_contact(slug, request_data)
    print(f"validated_contact---->{validated_contact}")
    response = skorozvon_api.add_contact(validated_contact)
    try:
        if response.status_code != 200:
            print(f"Re-trying task, attempt: {self.request.retries + 1}")
            self.retry(exc=MaxRetriesExceededError())
    except MaxRetriesExceededError:
        pass


def get_validate_contact(slug: str, request_data: dict):
    validated_contact = WantResultContactsValidator.model_validate(dict(request_data))
    validated_contact.project_id = get_project_id(slug)
    return validated_contact


@shared_task
def task_contact_check_and_sending_sz(request_data: dict, slug: str):
    validated_contact = WantResultContactsValidator.model_validate(request_data)
    validated_contact.project_id = get_project_id(slug)
    contact = get_or_create_or_update_contact(validated_contact, slug)
    check_contact = skorozvon_api.check_if_phone_was_called(contact)
    if not check_contact:
        response = skorozvon_api.add_contact(contact)
        log_response_want_result(response)
        if response.status_code != 200:
            task_resending_a_contact_to_sz.delay(slug, request_data)
