
from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_queryset(self):
        teacher = self.request.user
        return Grade.objects.filter(teacher=teacher)
