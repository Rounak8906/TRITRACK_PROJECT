import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def index(request):
    return render(request, 'TRITRACK.html')

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": body.get("messages", []),
                    "temperature": 0.7,
                    "max_tokens": body.get("max_tokens", 1000),
                },
                timeout=30,
            )

            return JsonResponse(response.json(), safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)