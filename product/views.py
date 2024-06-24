# Django
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from home.models import Product
from .models import ReviewModel

# Awesome Product !!


@csrf_exempt
@login_required
@require_POST
def add_review(request):
    data = json.loads(request.body)
    review = ReviewModel(
        user=request.user,
        rating=data['rating'],
        review=data['review'],
        product_id=int(data['productId']),
    )
    review.save()
    return JsonResponse({'message': 'Review added successfully'})
