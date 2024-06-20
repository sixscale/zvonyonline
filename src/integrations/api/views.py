import json

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import CallDataInfoSerializer
from ..services import exceptions
from ..services.logger import log_request, log_request_lead
from ..services.validation import ContactCreationData, LeadCreationData, flatten_data
from ..services.webhook_handler import webhook_handler, webhook_handler_and_send_to_amocrm


# logger = logging.getLogger(__name__)


class TestAPI(APIView):
    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class WriteDataToGoogleSheet(CreateAPIView):
    serializer_class = CallDataInfoSerializer

    def post(self, request, *args, **kwargs):
        log_request(json.dumps(request.data))
        serializer = self.serializer_class(data=flatten_data(request.data))
        webhook_handler_and_send_to_amocrm(request, serializer)
        return Response(status=status.HTTP_201_CREATED)


class WantResultsAPI(CreateAPIView):

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        webhook_handler(request.data, slug)
        response = Response(status=status.HTTP_200_OK)
        return response
