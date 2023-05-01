from django.http import Http404
from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Product
from .serializers import ProductSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def product_api(request):
    if request.method =='GET':
        json_data=request.body   # data
        stream = io.BytesIO(json_data)    # stream data 
        pythondata = JSONParser().parse(stream)  # conver python data
        id = pythondata.get('id',None)
        if id is not None:
            stu = Product.objects.get(id=id)
            serializer = ProductSerializer(stu)
            json_data=JSONRenderer().render(serializer.data)
            return HttpResponse(json_data,content_type='application/json')
        pro = Product.objects.all()
        serializer = ProductSerializer(pro,many=True)
        json_data=JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type='application/json')
    
    if request.method =='POST':
        json_data=request.body  
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = ProductSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)  # error are come in serializer.errors
        return HttpResponse(json_data,content_type='application/json')
    
    if request.method == 'PUT':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id=pythondata.get('id')
        pro= Product.objects.get(id=id)
        serializer = ProductSerializer(pro,data=pythondata,partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Data Updated !!'}
            json_data =JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data =JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')
        

    if request.method =='DELETE':
        json_data = request.body
        stream=io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id=pythondata.get('id')
        pro =Product.objects.get(id=id)
        pro.delete()
        res = {'msg':'Deleted Product !!'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json')
    