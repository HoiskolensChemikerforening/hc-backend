from rest_framework import mixins, viewsets
from .serializers import SubmissionSerializer
from ..models import Submission
from rest_framework.permissions import IsAuthenticated


class CreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = Submission
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
