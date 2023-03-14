import json
import requests

from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.conf import settings

TAGS_IDS = {
    "first_access": 1396,
    "recovery_password": 22342,
    "generation_password": 22343,
}

CUSTOM_FIELDS_IDS = {
    "password": 70,
    "recovery_url_link": 71,
}


class Connector:
    def __init__(self):
        self.api_root = settings.HOST_ACTIVE_CAMPAIGN
        self.api_secret_key = settings.ACTIVE_CAMPAIGN_API_KEY
        self.headers = {
            "Api-Token": settings.ACTIVE_CAMPAIGN_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }

    def get(self, endpoint):
        url = self.api_root + endpoint
        try:
            return requests.get(url, headers=self.headers)
        except Exception as e:
            raise ValidationError(e)

    def post(self, endpoint, data={}):
        url = self.api_root + endpoint

        try:
            return requests.post(url, json=data, headers=self.headers)
        except Exception as e:
            raise ValidationError(e)

    def put(self, endpoint, data={}):
        url = self.api_root + endpoint
        try:
            return requests.put(url, json=data, headers=self.headers)
        except Exception as e:
            raise ValidationError(e)

    def delete(self, endpoint, data={}):
        url = self.api_root + endpoint
        try:
            return requests.delete(url, data=json.dumps(data))
        except Exception as e:
            raise ValidationError(e)

    def patch(self, endpoint, data={}):
        url = self.api_root + endpoint
        try:
            return requests.patch(url, json=data)
        except Exception as e:
            raise ValidationError(e)


connector = Connector()


class ActiveCampaign:
    def create_or_get_account(email, firstName, phone):
        data_dict = {
            "contact": {"email": email, "firstName": firstName, "phone": phone}
        }
        request = connector.post(endpoint="/contact/sync", data=data_dict)
        status = request.json()
        return status["contact"]["id"]

    def add_tag_to_contact(self, contact_id: int, tags: str):
        data_dict = {"contactTag": {"contact": contact_id, "tag": TAGS_IDS.get(tags)}}
        request = connector.post(endpoint="/contactTags", data=data_dict)
        return Response(request.json(), status=request.status_code)

    def update_custom_field(self, contact_id: int, value: str, field: str):
        data_dict = {
            "contact": {
                "fieldValues": [{"field": CUSTOM_FIELDS_IDS.get(field), "value": value}]
            }
        }
        request = connector.put(endpoint=f"/contacts/{contact_id}", data=data_dict)
        return Response(request.json(), status=request.status_code)


active = ActiveCampaign()
