from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Keyword, Flag
from .serializers import (
    KeywordSerializer,
    FlagSerializer,
    FlagStatusUpdateSerializer,
)
from .services import run_scan


class KeywordCreateView(generics.CreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class ScanTriggerView(APIView):
    def post(self, request):
        flags = run_scan()
        serializer = FlagSerializer(flags, many=True)
        return Response(
            {
                "message": "Scan completed successfully",
                "flags": serializer.data
            },
            status=status.HTTP_200_OK
        )


class FlagListView(generics.ListAPIView):
    queryset = Flag.objects.select_related('keyword', 'content_item').all()
    serializer_class = FlagSerializer


class FlagStatusUpdateView(generics.UpdateAPIView):
    queryset = Flag.objects.select_related('content_item').all()
    serializer_class = FlagStatusUpdateSerializer

    def patch(self, request, *args, **kwargs):
        flag = self.get_object()
        serializer = self.get_serializer(flag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if flag.status == 'irrelevant':
            flag.suppressed_at_content_update = flag.content_item.last_updated
            flag.save()
        else:
            flag.suppressed_at_content_update = None
            flag.save()

        output_serializer = FlagSerializer(flag)
        return Response(output_serializer.data, status=status.HTTP_200_OK)