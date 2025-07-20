"""This module contains views for the Taskly API, including user registration, login, and task management."""

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes
from .serializers import RegisterSerializer, EmailLoginSerializer, TaskSerializer
from .models import Task
from .emails.utils import send_welcome_email, send_task_created_email
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    """View for user registration."""
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            try:
                username = getattr(user, 'username', None) or str(user.email).split('@')[0]
                send_welcome_email(
                    to_email=user.email,
                    username=username
                )
                logger.info(f"Welcome email sent to {user.email}")
            except Exception as e:
                logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
            
            return Response({
                "message": "User registered successfully.",
                "email_sent": True
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailLoginView(APIView):
    """View for user login using email."""
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User logged in successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    list=extend_schema(
        summary="List user tasks",
        description="Retrieve tasks for authenticated user with optional filtering",
        parameters=[
            OpenApiParameter('search', OpenApiTypes.STR, OpenApiParameter.QUERY, description='Search in title/description'),
            OpenApiParameter('completed', OpenApiTypes.BOOL, OpenApiParameter.QUERY, description='Filter by completion status'),
        ],
        tags=['Tasks']
    ),
    create=extend_schema(
        summary="Create new task",
        description="Create a new task and send email notification",
        tags=['Tasks']
    )
)
class TaskListCreateView(generics.ListCreateAPIView):
    """
    List all tasks for the authenticated user or create a new task.
    GET: Returns a list of tasks owned by the authenticated user
    POST: Creates a new task with the authenticated user as owner and sends email notification
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks only for the authenticated user."""
        queryset = Task.objects.filter(owner=self.request.user)
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            completed_bool = completed.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(completed=completed_bool)
            
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Automatically assign the authenticated user as the owner and send email notification."""
        task = serializer.save(owner=self.request.user)
        
        try:
            username = getattr(self.request.user, 'username', None) or str(self.request.user.email).split('@')[0]
            send_task_created_email(
                to_email=self.request.user.email,
                username=username,
                task_title=task.title,
                task_description=getattr(task, 'description', None),
                due_date=getattr(task, 'due_date', None)
            )
            logger.info(f"Task created email sent to {self.request.user.email} for task: {task.title}")
        except Exception as e:
            logger.error(f"Failed to send task created email to {self.request.user.email}: {str(e)}")

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific task for the authenticated user.
    GET: Returns task details if owned by authenticated user
    PUT/PATCH: Updates task if owned by authenticated user
    DELETE: Deletes task if owned by authenticated user
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks only for the authenticated user."""
        return Task.objects.filter(owner=self.request.user)

    def get_object(self):
        """Get task object ensuring it belongs to the authenticated user."""
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj

class TaskUpdateStatusView(generics.UpdateAPIView):
    """
    Update only the completion status of a task.
    PATCH: Toggle or set the completion status of a task
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return tasks only for the authenticated user."""
        return Task.objects.filter(owner=self.request.user)

    def patch(self, request, *args, **kwargs):
        """Update only the completed field."""
        task = self.get_object()
        completed = request.data.get('completed')
        
        if completed is not None:
            task.completed = completed
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        
        return Response(
            {'error': 'completed field is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class TaskCompletedListView(generics.ListAPIView):
    """
    List only completed tasks for the authenticated user.
    GET: Returns all completed tasks owned by the authenticated user
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only completed tasks for the authenticated user."""
        return Task.objects.filter(
            owner=self.request.user,
            completed=True
        ).order_by('-updated_at')

class TaskPendingListView(generics.ListAPIView):
    """
    List only pending (incomplete) tasks for the authenticated user.
    GET: Returns all pending tasks owned by the authenticated user
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only pending tasks for the authenticated user."""
        return Task.objects.filter(
            owner=self.request.user,
            completed=False
        ).order_by('due_date', '-created_at')

@extend_schema(
    summary="Toggle task status",
    description="Toggle completion status of a task",
    tags=['Tasks'],
    responses={200: TaskSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_task_status(request, pk):
    """
    Toggle the completion status of a task.
    POST: Toggles between completed and pending status
    """
    try:
        task = Task.objects.get(pk=pk, owner=request.user)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found or you do not have permission to access it.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    task.completed = not task.completed
    task.save()
    
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@extend_schema(
    summary="Get task statistics",
    description="Get task counts and completion rate",
    tags=['Statistics']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_stats(request):
    """
    Get task statistics for the authenticated user.
    GET: Returns counts of total, completed, and pending tasks
    """
    user_tasks = Task.objects.filter(owner=request.user)
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(completed=True).count()
    pending_tasks = user_tasks.filter(completed=False).count()
    
    overdue_tasks = user_tasks.filter(
        completed=False,
        due_date__lt=timezone.now()
    ).count() if user_tasks.exists() else 0
    
    stats = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
    }
    
    return Response(stats)