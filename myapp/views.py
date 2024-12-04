import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Incorrect JSON, please write in another format!')

        required_fields = {'name', 'price', 'available'}
        if not required_fields.issubset(data.keys()):
            return HttpResponseBadRequest('Missing fields: name, price, or available!!!')

        try:
            name = data.get('name')
            price = Decimal(str(data.get('price')))
            available = data.get('available')

            if price < 0:
                return HttpResponseBadRequest('Price only can be positive or 0!')

            product = Product(name=name, price=price, available=available)
            product.full_clean()
            product.save()
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            }, status=201)
        except Exception as e:
            return HttpResponseBadRequest(f'Invalid data: {str(e)}')

    else:
        return HttpResponseBadRequest('Method is incorrect, please use another!')

@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound({
            "error": f"Product with ID {product_id} does not exist."
        })

    if request.method == 'GET':
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'available': product.available
        })
    else:
        return HttpResponseBadRequest('Method is incorrect, please use another!')
