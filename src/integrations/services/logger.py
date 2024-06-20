from datetime import datetime
import logging

request_logger_write_data_to_google_sheet = logging.getLogger("request_logger_write_data_to_google_sheet")
lead_logger_write_data_to_google_sheet = logging.getLogger("lead_logger_write_data_to_google_sheet")
request_logger_want_result_webhook = logging.getLogger("request_logger_want_result_webhook")
contact_logger_want_result_webhook = logging.getLogger("contact_logger_want_result_webhook")
contact_logger_sz_body = logging.getLogger("contact_logger_sz_body")
amo_usi_body_logger = logging.getLogger("amo_usi_body_logger")


def log_request(request):
    request_logger_write_data_to_google_sheet.info(request)


def log_request_wantresult(request):
    request_logger_want_result_webhook.info(request)


def log_response_want_result(respone):
    contact_logger_want_result_webhook.info(f"response status SZ: {respone}")


def log_sz_body(body):
    contact_logger_sz_body.info(f"data sent to the SZ: {body}")


def log_request_lead(validated_contact, validated_lead):
    lead_logger_write_data_to_google_sheet.info(f"request time: {datetime.now()}\n"
                                                f"validated contact: {validated_contact}\n"
                                                f"validated lead: {validated_lead}\n")


def log_amo_usi_body(body):
    amo_usi_body_logger.info(f"body sent to the AMO USI: {body}")