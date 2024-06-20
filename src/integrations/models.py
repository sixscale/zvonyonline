from django.db import models


class CRMContact(models.Model):
    contact_id = models.IntegerField()
    phone = models.CharField(max_length=255)


class UsersKPI(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class ProjectInfo(models.Model):
    client = models.CharField(max_length=255)
    project_title = models.CharField(max_length=255, unique=True)
    scenario_title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class CallDataInfo(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)

    lead_id = models.CharField(max_length=255, null=True, blank=True)
    lead_name = models.CharField(max_length=255, null=True, blank=True)
    lead_comment = models.TextField(null=True, blank=True)
    lead_post = models.CharField(max_length=255, null=True, blank=True)
    lead_city = models.CharField(max_length=255, null=True, blank=True)
    lead_business = models.CharField(max_length=255, null=True, blank=True)
    lead_homepage = models.CharField(max_length=255, null=True, blank=True)
    lead_emails = models.JSONField(default=list, null=True, blank=True)
    lead_inn = models.CharField(max_length=255, null=True, blank=True)
    lead_kpp = models.CharField(max_length=255, null=True, blank=True)
    lead_created_at = models.CharField(max_length=255, null=True, blank=True)
    lead_updated_at = models.CharField(max_length=255, null=True, blank=True)
    lead_deleted_at = models.CharField(max_length=255, null=True, blank=True)
    lead_parent_lead_id = models.CharField(max_length=255, null=True, blank=True)
    lead_tags = models.JSONField(default=list, null=True, blank=True)
    lead_phones = models.CharField(max_length=255, null=True, blank=True)

    contact_id = models.CharField(max_length=255, blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_comment = models.TextField(null=True, blank=True)
    contact_post = models.CharField(max_length=255, null=True, blank=True)
    contact_city = models.CharField(max_length=255, null=True, blank=True)
    contact_business = models.CharField(max_length=255, null=True, blank=True)
    contact_homepage = models.CharField(max_length=255, null=True, blank=True)
    contact_emails = models.JSONField(default=list, null=True, blank=True)
    contact_inn = models.CharField(max_length=255, null=True, blank=True)
    contact_kpp = models.CharField(max_length=255, null=True, blank=True)
    contact_created_at = models.CharField(max_length=255, null=True, blank=True)
    contact_updated_at = models.CharField(max_length=255, null=True, blank=True)
    contact_deleted_at = models.CharField(max_length=255, null=True, blank=True)
    contact_parent_lead_id = models.CharField(max_length=255, blank=True, null=True)
    contact_tags = models.JSONField(default=list, null=True, blank=True)
    contact_address = models.CharField(max_length=255, null=True, blank=True)
    contact_phones = models.CharField(max_length=255, null=True, blank=True)

    call_id = models.CharField(max_length=255, null=True, blank=True)
    call_phone = models.CharField(max_length=255, null=True, blank=True)
    call_source = models.CharField(max_length=255, null=True, blank=True)
    call_direction = models.CharField(max_length=255, null=True, blank=True)
    call_params = models.JSONField(default=dict, null=True, blank=True)
    call_lead_id = models.CharField(max_length=255, null=True, blank=True)
    call_organization_id = models.CharField(max_length=255, null=True, blank=True)
    call_user_id = models.CharField(max_length=255, null=True, blank=True)
    call_started_at = models.CharField(max_length=255, null=True, blank=True)
    call_connected_at = models.CharField(max_length=255, null=True, blank=True)
    call_ended_at = models.CharField(max_length=255, null=True, blank=True)
    call_reason = models.CharField(max_length=255, null=True, blank=True)
    call_duration = models.IntegerField(null=True, blank=True)
    call_scenario_id = models.CharField(max_length=255, null=True, blank=True)
    call_result_id = models.CharField(max_length=255, null=True, blank=True)
    call_incoming_phone = models.CharField(max_length=255, null=True, blank=True)
    call_recording_url = models.URLField(null=True, blank=True)
    call_call_type = models.CharField(max_length=255, null=True, blank=True)
    call_region = models.CharField(max_length=255, null=True, blank=True)
    call_local_time = models.CharField(max_length=255, null=True, blank=True)
    call_call_project_id = models.CharField(max_length=255, null=True, blank=True)
    call_call_project_title = models.CharField(max_length=255, null=True, blank=True)
    call_scenario_result_group_id = models.CharField(max_length=255, null=True, blank=True)
    call_scenario_result_group_title = models.CharField(max_length=255, null=True, blank=True)

    call_result_result_id = models.CharField(max_length=255, null=True, blank=True)
    call_result_result_name = models.CharField(max_length=255, null=True, blank=True)
    call_result_comment = models.TextField(null=True, blank=True)

    save_date = models.DateTimeField(auto_now_add=True)


class Leads(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=255, blank=True)
    phoneNumber = models.CharField(max_length=255, blank=True)
    site = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    projectId = models.CharField(max_length=100, blank=True)
    addDate = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'Leads'


class WantResultContacts(models.Model):
    # The data that comes from Vontresalt
    vid = models.BigIntegerField(blank=True)
    site = models.CharField(max_length=255, blank=True)
    page = models.CharField(max_length=255, blank=True)
    ref = models.CharField(max_length=255, blank=True)
    time = models.BigIntegerField(blank=True)
    browser = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=255, blank=True)
    platform = models.CharField(max_length=255, blank=True)
    ip = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    roistat_visit = models.CharField(max_length=255, blank=True)
    phones_first = models.CharField(max_length=255, blank=True)
    phones_second = models.CharField(max_length=255, blank=True)
    phones_third = models.CharField(max_length=255, blank=True)
    mails_first = models.CharField(max_length=255, blank=True)
    mails_second = models.CharField(max_length=255, blank=True)
    utm_term = models.CharField(max_length=255, blank=True)
    utm_source = models.CharField(max_length=255, blank=True)
    utm_campaign = models.CharField(max_length=255, blank=True)
    utm_medium = models.CharField(max_length=255, blank=True)
    utm_content = models.CharField(max_length=255, blank=True)
    gclid = models.CharField(max_length=255, blank=True)

    # Additional fields for sending to Skorozvon
    project_id = models.BigIntegerField(blank=True)

    def __json_encode__(self):
        return self.__dict__


class RatioOfProjectsFromWRToSZ(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    project_id = models.BigIntegerField(blank=True)


class SkorozvonLeadWH(models.Model):
    pass
