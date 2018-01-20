# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from simplecrypt import encrypt, decrypt
from rest_framework_jwt.settings import api_settings
from rest_framework.parsers import JSONParser
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, serializers
from pyethmobisir import EthJsonRpc
from serializers import UserLoginSerializer
from datacenter.models import User, UserProfile
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login, logout, authenticate


# Create your views here.
def register(request):
    return HttpResponse("register service")


def auth_bc():
    headers = {'content-type':'application/json'}
    api_data = '{"jsonrpc":"2.0","method":"personal_unlockAccount",\
        "params":["0x76e13c978f42bfd01e5241a0bbf09110db4952f6","techsummit"],"id":"2"}'
    unlock_response = requests.post("http://13.127.33.43", api_data, headers=headers, verify=False)
    return unlock_response

def create_bc_address():
    auth_bc()
    headers = {'content-type':'application/json'}
    api_data = '{"jsonrpc":"2.0","method":"personal_newAccount","params":["techsummit"],"id":"1"}' 
    created = requests.post("http://13.127.33.43", api_data, headers=headers, verify=False)
    print created
    return created

@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def set_user(request):
    if request.method == 'POST':
        auth_bc()

        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        dob = request.POST.get('dob', None)
        gender = request.POST.get('gender', None)
        father_name = request.POST.get('father_name', None)
        address = request.POST.get('address', None)
        mobile = request.POST.get('mobile', None)
        email = request.POST.get('email', None)
        finger_print = request.POST.get('finger_print', None)
        bc_address = create_bc_address()
        
        user_details = {}
        user_details['first_name'] = first_name
        user_details['last_name'] = last_name
        user_details['father_name'] = father_name
        user_details['dob'] = dob
        user_details['gender'] = gender
        user_details['address'] = address
        user_details['mobile'] = mobile
        user_details['email'] = email
        user_details['bc_address'] = json.loads(bc_address.content)['result']
        user_details['finger_print'] = finger_print
        
        eth_connection = EthJsonRpc("13.127.33.43","80")
        transaction = eth_connection.call_with_transaction(
            eth_connection.eth_coinbase(),
            "0x3aed98631ABb156fF525b4CaE202E6bDe3402bF0",
            'set_s(string)',
            [str(json.dumps(user_details))]
        )
        print transaction
        res = {}
        res['transaction'] = transaction
        return Response(res, status=200)


@api_view(['POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_user(request):
    res = {}
    auth_bc()
    hash = request.POST.get("hash", None)
    eth_connection = EthJsonRpc("13.127.33.43","80")
    get_transaction_details = eth_connection.eth_getTransactionByHash(hash)
    get_input_hex = get_transaction_details['input']
    get_readable_detail = get_input_hex[138:].decode('hex').split('\x00')[0]
    res['data'] = get_readable_detail
    return Response(res, status=200)

# ---------------------------------------------------------------
# User Login: JWT and Session Login
# ---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((AllowAny, ))
def auth_login(request):
    """
    User Login and Creating a new jwt token
    """
    if request.method == 'POST':
        # loading jwt payload handlers
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        serializer = UserLoginSerializer(data=request.data)
        user = None
        if serializer.is_valid():
            user_name = serializer.data.get('username')
            user_pass = serializer.data.get('password')
            user_exists = User.objects.filter(username=user_name)
            user = authenticate(username=user_name,password=user_pass)
            if user:
                if user.is_active and user.is_staff:
                    '''
                    set username and token in response
                    object if the user need to continue
                    '''
                    login(request, user)
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response_object = {
                        'username': user.username,
                        'token': token,
                        'status': 'success'
                    }
                    return Response(response_object, status=status.HTTP_200_OK)
                else:
                    response_object = {
                        'username': user_name,
                        'status': 'false',
                        'message': 'Your Account is Locked Please call customer care',
                    }
                    return Response(response_object,status=status.HTTP_401_UNAUTHORIZED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
# ---------------------------------------------------------------