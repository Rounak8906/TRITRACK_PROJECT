import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def index(request):
    return render(request, 'tritrack.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': settings.ANTHROPIC_API_KEY,
                    'anthropic-version': '2023-06-01'
                },
                json=body,
                timeout=30
            )
            data = response.json()
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)