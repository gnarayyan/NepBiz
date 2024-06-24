from django.shortcuts import render
from home.models import Product


def search(request):
    query = request.GET.get('q')

    if query:
        # Perform the search query using your model
        results = Product.objects.filter(name__icontains=query)
        context = {'food_items': results, 'query': query}
        return render(request, 'search/search.html', context)
    return render(request, 'search/search.html')
