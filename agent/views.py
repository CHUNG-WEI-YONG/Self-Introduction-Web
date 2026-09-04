import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .rag_service import query_agent


@csrf_exempt
@require_POST
def chat_api_view(request):
  try:
    if not request.body:
      return JsonResponse(
          {'error': 'Request body is completely empty.'}, status=400
      )

    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    # 兼容 message、text 或 query
    user_message = (
        data.get('message') or data.get('text') or data.get('query') or ''
    )
    user_message = str(user_message).strip()

    if not user_message:
      return JsonResponse(
          {'error': 'Message content cannot be empty.'}, status=400
      )

    reply = query_agent(user_message)
    return JsonResponse({'reply': reply})

  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
  except Exception as e:
    return JsonResponse({'error': f'Agent Server Error: {str(e)}'}, status=500)


