from django.shortcuts import render
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from .serializers import ChatMessageSerializer

# Create your views here.

class ChatbotAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data['message']

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:3000",  # Or your frontend URL
            "X-Title": "Ecart Chatbot",               # Or your site name
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-4o",  # You can change to any supported model
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 256
        }
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        try:
            data = response.json()
            bot_reply = data["choices"][0]["message"]["content"]
        except Exception:
            print("Error or unexpected response:", response.text)
            bot_reply = "Sorry, I couldn't generate a reply right now."

        return Response({"reply": bot_reply})
