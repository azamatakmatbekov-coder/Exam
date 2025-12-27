from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer

class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['is_completed']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(owner=user)
        status = self.request.query_params.get('is_completed')
        if status is not None:
            if status.lower() in ['true', '1']:
                queryset = queryset.filter(is_completed=True)
            elif status.lower() in ['false', '0']:
                queryset = queryset.filter(is_completed=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



