from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator, Field, AliasPath, validator


def get_current_date():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class LeadCreationData(BaseModel):
    comment: str = Field(validation_alias=AliasPath("call_result_comment"), default="")
    contact_name: str = Field(validation_alias=AliasPath("lead_name"), default="")
    scenario_id: str = Field(validation_alias=AliasPath("call_scenario_id"), default="")
    result_id: str = Field(validation_alias=AliasPath("call_result_result_id"), default="")
    tag: str = Field(default="")


class ContactCreationData(BaseModel):
    phone: str = Field(validation_alias=AliasPath("lead_phones"), default="")
    name: str = Field(validation_alias=AliasPath("lead_name"), default="")

    @field_validator("phone")
    def phone_validator(cls, value):
        remove_symbols = "+_-() "
        for symbol in remove_symbols:
            value = value.replace(symbol, "")
        if value[0] == 8:
            value[0] = 7
        return value


def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


class WantResultContactsValidator(BaseModel):
    vid: int = Field(validation_alias=AliasPath("vid"), default=0)
    site: str = Field(validation_alias=AliasPath("site"), default="")
    page: str = Field(validation_alias=AliasPath("page"), default="")
    ref: str = Field(validation_alias=AliasPath("ref"), default="")
    time: int = Field(validation_alias=AliasPath("time"), default=0)
    browser: str = Field(validation_alias=AliasPath("browser"), default="")
    device: str = Field(validation_alias=AliasPath("device"), default="")
    platform: str = Field(validation_alias=AliasPath("platform"), default="")
    ip: str = Field(validation_alias=AliasPath("ip"), default="")
    comment: str = Field(validation_alias=AliasPath("comment"), default="", allow_none=True)
    roistat_visit: str = Field(validation_alias=AliasPath("roistat_visit"), default="")
    phones_first: str = Field(validation_alias=AliasPath("phones", 0), default="")
    phones_second: str = Field(validation_alias=AliasPath("phones", 1), default="")
    phones_third: str = Field(validation_alias=AliasPath("phones", 2), default="")
    mails_first: str = Field(validation_alias=AliasPath("mails", 0), default="")
    mails_second: str = Field(validation_alias=AliasPath("mails", 1), default="")
    utm_term: str = Field(validation_alias=AliasPath("utm", "utm_term"), default="")
    utm_source: str = Field(validation_alias=AliasPath("utm", "utm_source"), default="")
    utm_campaign: str = Field(validation_alias=AliasPath("utm", "utm_campaign"), default="")
    utm_medium: str = Field(validation_alias=AliasPath("utm", "utm_medium"), default="")
    utm_content: str = Field(validation_alias=AliasPath("utm", "utm_content"), default="")
    gclid: str = Field(validation_alias=AliasPath("utm", "gclid"), default="")
    project_id: int = Field(default=0)

    @validator('*', pre=True, always=True)
    def replace_none_with_empty_str(cls, v):
        if v is None:
            return ""
        return v
