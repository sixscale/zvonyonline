import json
import requests
import time

from django.conf import settings

from .logger import log_amo_usi_body
from .validation import ContactCreationData, LeadCreationData
from . import amo_db

LEAD_FIELDS_IDS = {
    1444017: "comment",
    1432107: "contact_name",
}

CONTACT_FIELDS_IDS = {
}

AMO_WORKING_SCENARIOS = {
    "50000014598": "Авито ЗО",
    "50000014725": "Сайты ЗО",
}

AMO_WORKING_RESULT_USI_IDS = {
    50000080830: "ЮСИ ГЦК Ств",
    50000227298: "ЮСИ ГКЦ Крд",
    50000208244: "ЮСИ Сайты ЖК РнД",
    50000226822: "ЮСИ Сайты ЖК Крд",
    50000011952: "ЮСИ Сайты ЖК Крд",
    50000208236: "ЮСИ Сайт ЖК Ств",
    50000208248: "ЮСИ ГКЦ РнД",
    50000208240: "ЮСИ Авито Ств",
    50000237106: "ЮСИ ГЦК Ств",
    50000208252: "ЮСИ Авито РнД",
    50000233411: "АН ГЦК РнД",
    50000013183: "АН ГКЦ Рнд",
    50000014134: "ЮСИ РнД ЖК Персон",
    50000003654: "ЮСИ Ставрополь ЖК Печорин",
}

AMO_WORKING_CUSTOM_FIELD_USI = {
    # Проект ЮСИ ГКЦ РнД - FIELD_50000007635
    50000001821: "ЖК Персона",
    50000001822: "ЖК Полет",
    50000001823: "ЖК Левобережье",
    50000003095: "ЖК Сияние",
    # ЮСИ ГКЦ Крд - FIELD_50000007637
    50000001827: "ЖК Губернский",
    50000001828: "ЖК Достояние",
    50000001829: "ЖК Архитектор",
    50000003182: "ЖК Эрмитаж",
    # ЮСИ ГЦК Ств - FIELD_50000007636
    50000001824: "ЖК 1777",
    50000001825: "ЖК Высота",
    50000001826: "ЖК Основа",
    50000003654: "ЮСИ Ставрополь ЖК Печорин",
}

AMO_WORKING_RESULTS_IDS = [
    "50000014598",
    "50000261928",
    "50000264262",
]


def save_token_data(data: dict):
    url = f"https://{settings.AMO_INTEGRATION_SUBDOMAIN}.amocrm.ru/oauth2/access_token"
    response = requests.post(url, json=data).json()
    data = {
        "access_token": response['access_token'],
        "refresh_token": response['refresh_token'],
        "token_type": response['token_type'],
        "expires_in": response['expires_in'],
        "end_token_time": response['expires_in'] + time.time(),
    }
    with open(settings.BASE_DIR / 'refresh_token.txt', 'w') as outfile:
        json.dump(data, outfile)
    return data["access_token"]


def auth():
    data = {
        'client_id': settings.AMO_INTEGRATION_CLIENT_ID,
        'client_secret': settings.AMO_INTEGRATION_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': settings.AMO_INTEGRATION_CODE,
        'redirect_uri': settings.AMO_INTEGRATION_REDIRECT_URI,
    }
    return save_token_data(data)


def get_fields(postfix: str):
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    link = f"/api/v4/{postfix}/custom_fields"
    url = f"https://{settings.AMO_INTEGRATION_SUBDOMAIN}.amocrm.ru{link}"
    return requests.get(url, headers=headers).json()


def update_access_token(refresh_token: str):
    data = {
        "client_id": settings.AMO_INTEGRATION_CLIENT_ID,
        "client_secret": settings.AMO_INTEGRATION_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": settings.AMO_INTEGRATION_REDIRECT_URI,
    }
    return save_token_data(data)


def get_access_token():
    with open(settings.BASE_DIR / 'refresh_token.txt') as json_file:
        token_info = json.load(json_file)
        if token_info["end_token_time"] - 60 < time.time():
            return update_access_token(token_info["refresh_token"])
        else:
            return dict(token_info)["access_token"]


def get_custom_fields_values(field_ids: dict, data):
    custom_fields_values = []
    data = data.dict()
    for field_id, field_name in field_ids.items():
        custom_fields_values.append({
            "field_id": field_id,
            "values": [{"value": data[field_name]}]
        })
    return custom_fields_values


def get_or_create_contact(validated_data):
    if amo_db.contact_exists(validated_data.phone):
        contact_id = amo_db.get_contact_id_by_phone(validated_data.phone)
    else:
        contact_id = create_contact(validated_data)
        amo_db.create_contact(contact_id=contact_id, phone=validated_data.phone)
    return contact_id


def create_contact(contact: ContactCreationData):
    custom_fields = get_custom_fields_values(CONTACT_FIELDS_IDS, contact)
    custom_fields.append({
        "field_id": 104057,
        "values": [
            {
                "value": contact.phone,
                "enum_code": "WORK"
            }
        ]
    })
    body = [{
        "name": contact.name,
        "responsible_user_id": 10892178,
        "custom_fields_values": custom_fields,
    }]
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    url = f"https://{settings.AMO_INTEGRATION_SUBDOMAIN}.amocrm.ru/api/v4/contacts"
    return requests.post(url, json=body, headers=headers).json()['_embedded']['contacts'][0]['id']


def create_lead(contact_id, lead: LeadCreationData, contact: ContactCreationData):
    lead.tag = AMO_WORKING_SCENARIOS[lead.scenario_id]
    custom_fields = get_custom_fields_values(LEAD_FIELDS_IDS, lead)
    body = [{
        "name": f"Звони онлайн {contact.phone}",
        "pipeline_id": settings.AMO_LEAD_PIPELINE_ID,
        "status_id": settings.AMO_LEAD_STATUS_ID,
        "Компания": contact.phone,
        "_embedded": {
            "contacts": [{"id": contact_id}],
            "tags": [{"name": lead.tag}],
        },
        "responsible_user_id": 10892178,
        "custom_fields_values": custom_fields
    }]
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    url = f"https://{settings.AMO_INTEGRATION_SUBDOMAIN}.amocrm.ru/api/v4/leads"
    requests.post(url, json=body, headers=headers).json()


def send_lead_to_amocrm(contact: ContactCreationData, lead: LeadCreationData):
    contact_id = get_or_create_contact(contact)
    create_lead(contact_id, lead, contact)


def is_lead(scenario_id: str, result_id: str):
    return is_working_scenario_id(scenario_id) and is_working_result_id(result_id)


def is_working_result_id(result_id: str):
    return result_id in AMO_WORKING_RESULTS_IDS


def is_working_scenario_id(scenario_id: str):
    return scenario_id in AMO_WORKING_SCENARIOS.keys()


def send_usi_lead_to_amocrm(serializer_data, request_data):
    url = 'https://usi-col.int3grat.ru/usi_ZO.php'
    headers = {
        'Content-Type': 'application/json'
    }

    custom_fields = request_data["lead"]["custom_fields"]
    value_field = next(((key, value) for key, value in custom_fields.items() if value is not None), None)

    # data = serializer_data
    data = request_data
    data["0"] = {"teg": AMO_WORKING_RESULT_USI_IDS[request_data["call"]["result_id"]]}
    try:
        data["1"] = {"teg": AMO_WORKING_CUSTOM_FIELD_USI[value_field[1]]}
    except TypeError or KeyError:
        pass
    data["call"]["recording_url"] = "0"
    updated_data = json.dumps(data, indent=2, ensure_ascii=False)
    log_amo_usi_body(updated_data)

    response = requests.post(url, headers=headers, data=updated_data)
    print(f"RESPONSE ----->{response}")
    return response


