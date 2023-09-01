import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status, generics
from django.views.decorators.csrf import csrf_exempt
from commonFunction import required_validation ,validateRegex, validate_len
from .models import User,ContentItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.serializers import serialize
from cms.serializers import UserSerializer, ContentItemSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
#from .permission import IsAuthorOrAdmin

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def userRegister(request):
    try:
        data = json.loads(request.body)
# Required Validation code
        required_data = ['email','password','fullName','phone','pincode']
        check,not_available = required_validation(request,required_data)
        if not check:
            message = "Please enter all required fields" + str(not_available) + "should not be empty"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
           
# Assigning all data
        email = data.get('email')
        password = data.get('password')
        fullName = data.get('fullName')
        phone = data.get('phone')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')
        pincode = data.get('pincode')
#Email already exist in tabel Validation
        valid_email = User.objects.values_list('email',flat=True)
        if email in valid_email:
            message = "Email Id already exist."
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
# Email validation
        if not validateRegex(email,'email'):
            message = "Please enter valid email address"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
# password validation
        if not validateRegex(password,'password'):
            message = "Please enter valid password"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
# phone validation
        if not validateRegex(phone,'phone'):
            message = "Please enter valid phone number"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
# pincode validation
        if not validateRegex(pincode,'pincode'):
            message = "Please enter valid pincode number"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
        addUser = User.objects.create(
            email = email,
            password = password,
            fullName =fullName,
            phone = phone,
            address = address,
            city=city,
            state =state,
            country =country,
            pincode=pincode
        )
        addUser.save()
        message = "Registration successful"
        return JsonResponse({'message':message},status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return JsonResponse({'message':e, 'status':500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'])
def userLogin(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        user = User.objects.get(email=email,password=password)
        print(user)
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)       
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return JsonResponse({'access_token': access_token},status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return JsonResponse({'message':'', 'status':500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#User Author class API
@api_view(['GET','POST'])
def contentItem(request):
    if request.method == 'GET':
        item= ContentItem.objects.all()
        ser = ContentItemSerializer(item,many=True)
        return Response(ser.data) 
    
    elif request.method == 'POST':
        data= request.data
        title= data.get('title')
        body= data.get('body')
        summary = data.get('summary')
        if not validate_len(title,30):
            message = "Please enter title less then 30 characters"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
        if not validate_len(body,300):
            message = "Please enter body less then 30 characters"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
        if not validate_len(summary,60):
            message = "Please enter summary less then 30 characters"
            return JsonResponse({'message':message},status=status.HTTP_406_NOT_ACCEPTABLE)
        ser = ContentItemSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])    
def contentItemDetail(request,pk):
    try:
        item = ContentItem.objects.get(pk=pk)
    except ContentItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        ser = ContentItemSerializer(item)
        return Response(ser.data)
    
    elif request.method == 'PUT':
        ser = ContentItemSerializer(item,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



