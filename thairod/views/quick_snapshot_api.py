from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from thairod.services.quick_snapshot.quick_snapshot_service import QuickSnapshotResponse, QuickSnapshotService
from thairod.utils.auto_serialize import swagger_auto_serialize_get_schema


class QuickSnapshotView(APIView):

    @swagger_auto_serialize_get_schema(
        query_type=None,
        response_type=QuickSnapshotResponse
    )
    def get(self, request: Request) -> Response:
        qsr = QuickSnapshotService.build_quick_snapshot_response()
        return qsr.to_response()
