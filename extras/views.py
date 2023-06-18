from rest_framework.generics import GenericAPIView
from .models import ExpectedCalories
from .serializer import ExpectedSerializer
from django.http import JsonResponse
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.utils import timezone

class CreateView(GenericAPIView):
    serializer_class = ExpectedSerializer
    permission_classes = []

    @swagger_auto_schema(
        tags=['expected'],
        operation_summary='Create a expected calories setting',
        operation_description='This endpoint is for creating a setting of expected calories value',
    )
    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse({
                "status": "success",
                "code": 200,
                "data": serialized_data.data
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            "status": "error",
            "code": 400,
            "errors": serialized_data.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class FilterView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        tags=['expected'],
        operation_summary='Filter the expected calorie setting using user id',
        operation_description='Filter user expected calories',
    )
    def get(self, request, id):
        instance = ExpectedCalories.objects.filter(user_id=id).first()
        if instance is not None:
            return JsonResponse({
                "status": "success",
                "code": 200,
                "data": {
                    "user_id": instance.user_id.id,
                    "expected": instance.expected
                }
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            "status": "error",
            "code": 404,
            "errors": "Not Found"
        }, status=status.HTTP_404_NOT_FOUND)


class UpdateView(GenericAPIView):
    serializer_class = ExpectedSerializer

    @swagger_auto_schema(
        tags=['expected'],
        operation_summary='Update a expected calories setting',
        operation_description='This endpoint is for updating a setting of expected calories value',
    )
    def put(self, request):
        data = ExpectedCalories.objects.filter(user_id=request.data.get("user_id")).first()
        if data is not None:
            data.expected = request.data.get("expected")
            data.updated_at = timezone.now()
            data.save()
            return JsonResponse({
                "status": "success",
                "code": 200,
                "message": "Updated Successfully!"
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            "status": "error",
            "code": 400,
            "errors": "Something went wrong!"
        }, status=status.HTTP_400_BAD_REQUEST)


class DeleteView(APIView):
    @swagger_auto_schema(
        tags=['expected'],
        operation_summary='Delete the expected calorie setting using user id',
        operation_description='Delete user expected calories',
    )
    def delete(self, request, id):
        instance = ExpectedCalories.objects.filter(user_id=id).first()
        if instance is not None:
            temp = instance
            instance.delete()
            return JsonResponse({
                "status": "success",
                "code": 200,
                "data": {
                    "user_id": temp.user_id.id,
                    "expected": temp.expected
                }
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            "status": "error",
            "code": 404,
            "errors": "Not Found"
        }, status=status.HTTP_404_NOT_FOUND)