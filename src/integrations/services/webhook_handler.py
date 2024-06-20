import json

from requests import Request
from rest_framework.response import Response
from rest_framework import status

from . import exceptions
from .amocrm import is_lead, send_usi_lead_to_amocrm
from .validation import ContactCreationData, LeadCreationData
from ..api.serializers import CallDataInfoSerializer
from ..services.logger import log_request_wantresult, log_response_want_result, log_request_lead
from ..services.tasks import task_contact_check_and_sending_sz


def webhook_handler(request_data: dict, slug: str):
    log_request_wantresult(json.dumps(request_data))
    task_contact_check_and_sending_sz.delay(request_data, slug)


def webhook_handler_and_send_to_amocrm(request: Request, serializer: CallDataInfoSerializer):
    if not serializer.is_valid():
        raise exceptions.SerializerNotValidError(f"Данные не валидны: {serializer.data}")
    serializer.save()
    if is_lead(serializer.data.get("call_scenario_id", ""), serializer.data.get("call_result_result_id", "")):
        validated_contact = ContactCreationData.model_validate(serializer.data)
        validated_lead = LeadCreationData.model_validate(serializer.data)
        log_request_lead(validated_contact, validated_lead)
        # send_lead_to_amocrm(validated_contact, validated_lead)
        print("Отправил в амо самолет")
        return Response(status=status.HTTP_201_CREATED)
    send_usi_lead_to_amocrm(serializer.data, request.data)
