# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from simplecrypt import encrypt, decrypt


# Create your views here.
def register(request):
    return HttpResponse("register service")

def auth():
    headers = {'content-type':'application/json'}
    api_data = '{"jsonrpc":"2.0","method":"personal_unlockAccount",\
        "params":["0x76e13c978f42bfd01e5241a0bbf09110db4952f6","techsummit"],"id":"2"}'
    unlock_response = requests.post("http://13.127.33.43", api_data, headers=headers, verify=False)
    return jsonify({'status': "OK"}), 201

def create_bc_address():
    auth()
    headers = {'content-type':'application/json'}
    api_data = '{"jsonrpc":"2.0","method":"personal_newAccount","params":["techsummit"],"id":"1"}' 
    created = requests.post("http://13.127.33.43", api_data, headers=headers, verify=False)
    print created
    return created

@authentication_classes((JSONWebTokenAuthentication,))
def set_user():
    if request.method == 'POST':
        auth()
        
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

        user_details = '{"first_name":"'+first_name+'",\
            "last_name":"'+last_name+'",\
            "father_name":"'+father_name+'",\
            "dob":"'+dob+'",\
            "gender":"'+gender+'",\
            "address":'+address+'",\
            "mobile":'+mobile+'",\
            "email":"'+email+'",\
            "bc_address":"'+bc_address+'",\
            "finger_print":'+finger_print+'"}'
        
        ciphertext = encrypt(finger_print, user_details)

        eth_connection = EthJsonRpc("13.127.33.43","80")
        transaction = eth_connection.call_with_transaction(
            eth_connection.eth_coinbase(),
            "0x3aed98631ABb156fF525b4CaE202E6bDe3402bF0",
            'set_s(string)',
            [ciphertext]
        )
        print transaction
        return Response(transaction, status=200)

@authentication_classes((JSONWebTokenAuthentication,))
def get_user():
    auth()
    hash = request.POST.get("hash", None)
    eth_connection = EthJsonRpc("13.127.33.43","80")
    get_transaction_details = eth_connection.eth_getTransactionByHash(hash)
    get_input_hex = get_transaction_details['input']
    get_readable_detail = get_input_hex[138:].decode('hex').split('\x00')[0]
    print "get_readable_detail"
    print get_readable_detail
    plaintext = decrypt(password, get_readable_detail)
    print "plaintext"
    print plaintext
    return Response(transaction, status=200)