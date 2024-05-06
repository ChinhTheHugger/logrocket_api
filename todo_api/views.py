# from django.shortcuts import render

# # Create your views here.

# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        print(serializer)
        print("\n-----\n")
        print(serializer.data)
        print(status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(Response(serializer.data, status=status.HTTP_201_CREATED))
            if "201" in str(Response(serializer.data, status=status.HTTP_201_CREATED)):
                print("checked")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# use this to create api for the car shop