import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "TRITRACK.html")


@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)

        # Build messages for Groq
        messages = []

        if body.get("system"):
            messages.append({
                "role": "system",
                "content": body["system"]
            })

        messages.extend(body.get("messages", []))

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": body.get("max_tokens", 1000),
            },
            timeout=30,
        )

        # Print response in Render logs
        print("Groq Response:", response.json())

        return JsonResponse(response.json(), safe=False)

    except Exception as e:
        print("ERROR:", str(e))
        return JsonResponse(
            {"error": str(e)},
            status=500
        )