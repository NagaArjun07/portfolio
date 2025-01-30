from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Contact
from .celery_task import send_feedback_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
class ContactSet(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True, max_length=100)
        email = serializers.EmailField(required=True)
        content = serializers.CharField(required=True)

    def post(self, request):
        """
        Create a new contact entry.
        """
        # Deserialize and validate incoming data
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Call the function to create a contact entry
        return self.create_contact(**serializer.validated_data)

    def create_contact(self, **data):
        try:
            # Create the Contact instance
            contact = Contact(
                name=data.get('name'),
                email=data.get('email'),
                content=data.get('content')
            )
            contact.save()

            # Send email using the renamed function
            send_feedback_mail(contact.email)

            # Return response with the created contact's details
            return JsonResponse({
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'content': contact.content,
                'message': "Contact created successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle exceptions and return an error response
            return JsonResponse({'error': f"Error creating contact: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class ContactGet(APIView):
    def get(self, request):
        """
        Retrieve all contact entries.
        """
        try:
            # Fetch all contacts from the database
            contact_data = Contact.objects.all().values()

            # Return the response with the contact data
            return JsonResponse({
                'data': list(contact_data),
                'message': "Contacts retrieved successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle exceptions and return an error response
            return JsonResponse({'error': f"Error retrieving contacts: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)