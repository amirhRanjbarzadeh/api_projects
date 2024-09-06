from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer


class TaskListView(APIView):
    """
    View to list all tasks for the authenticated user and create a new task.

    - GET: Returns a list of tasks that belong to the authenticated user.
    - POST: Allows the authenticated user to create a new task.

    Permissions:
    - Requires the user to be authenticated (IsAuthenticated).
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Retrieve all tasks belonging to the authenticated user.

        Returns a list of tasks ordered by the 'updated_at' field.

        Responses:
        - 200: List of tasks serialized in JSON format.
        """
        tasks = Task.objects.all().filter(owner=request.user).order_by('updated_at')
        ser_data = TaskSerializer(tasks, many=True)
        return Response(ser_data.data)

    def post(self, request, format=None):
        """
        Create a new task for the authenticated user.

        The owner of the task is automatically set to the current user.

        Request body:
        - Task data in JSON format.

        Responses:
        - 201: Task created successfully.
        - 400: Invalid data, task creation failed.
        """
        ser_data = TaskSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save(owner=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """
    View to retrieve, update, or delete a specific task for the authenticated user.

    - GET: Returns details of a specific task that belongs to the authenticated user.
    - PUT: Updates a specific task that belongs to the authenticated user.
    - DELETE: Deletes a specific task that belongs to the authenticated user.

    Permissions:
    - Requires the user to be authenticated (IsAuthenticated).
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, user):
        """
        Helper method to retrieve a task by its primary key and owner.

        Raises:
        - Http404: If the task does not exist or does not belong to the user.
        """
        return Task.objects.get(pk=pk, owner=user)

    def get(self, request, pk, format=None):
        """
        Retrieve details of a specific task by its primary key (pk).

        Returns the task if it belongs to the authenticated user.

        Responses:
        - 200: Task details serialized in JSON format.
        - 404: Task not found.
        """
        task = self.get_object(pk, request.user)
        ser_data = TaskSerializer(task)
        return Response(ser_data.data)

    def put(self, request, pk, format=None):
        """
        Update a specific task by its primary key (pk).

        Only the task's owner can update the task.

        Request body:
        - Partial or full task data in JSON format.

        Responses:
        - 200: Task updated successfully.
        - 400: Invalid data, task update failed.
        - 404: Task not found.
        """
        task = self.get_object(pk, request.user)
        ser_data = TaskSerializer(task, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete a specific task by its primary key (pk).

        Only the task's owner can delete the task.

        Responses:
        - 204: Task deleted successfully.
        - 404: Task not found.
        """
        task = self.get_object(pk, request.user)
        task.delete()
        return Response({"detail": f"{task.title} has been deleted"}, status=status.HTTP_204_NO_CONTENT)
