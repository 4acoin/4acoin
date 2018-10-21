#-*- coding: utf-8 -*-
import uuid , json , string , random, urllib, base64, os, sys, time, pickle, collections, math, arrow
from django.utils.encoding import smart_str
from ecdsa import SigningKey, SECP256k1, NIST384p, BadSignatureError, VerifyingKey
from django.http import *
from django import template
from django.shortcuts import *
from django.http import HttpResponse
from django.contrib.auth import logout
import hashlib
from django.conf import settings
from core.models import transaction
from django.db.models import Avg, Sum, Count, Q
from cloudbank.utils import instantwallet, generate_wallet_from_pkey, generate_pubkey_from_prikey
import simplejson as json


def getwalletfrompkey(request, pkey):
    data = {}
    print(type(pkey))
    wallet = generate_wallet_from_pkey(pkey)
    data["public_key"] = pkey
    data["wallet"] = wallet
    return HttpResponse(json.dumps(data), content_type = "application/json")



def getbalancefromwallet(request, wallet):
    data = {}
    balance = gbfw(wallet)
    data["balance"] = balance
    data["wallet"] = wallet
    return HttpResponse(json.dumps(data), content_type = "application/json")

def gbfw(wallet_id):
    income = transaction.objects.filter(receiver=wallet_id).aggregate(Sum('amount'))['amount__sum']
    outgoing = transaction.objects.filter(senderwallet=wallet_id).aggregate(Sum('amount'))['amount__sum']

    if income and outgoing:
        # print("user have both")
        return(income - outgoing)
    elif outgoing is None:
        # print("user dont have  outgoing")
        return income
    elif income is None:
        return 0
    else:
        return 0



def getpublickeyfromprikey(request, private_key):
    data = {}
    public_key = generate_pubkey_from_prikey(private_key)
    data["private_key"] = private_key
    data["public_key"] = public_key
    return HttpResponse(json.dumps(data), content_type = "application/json")


def getwalletdetails(request, wallet):
    data = {}
    incomes = []

    income = transaction.objects.filter(Q(receiver=wallet) |  Q(senderwallet=wallet))
    #outgoing = transaction.objects.filter(senderwallet=wallet)
    for trr in income:
        incomes.append({"sender" : trr.sender,
                     "senderwallet": trr.senderwallet,
                     "receiver": trr.receiver,
                     "prevblockhash": trr.prevblockhash,
                     "blockhash": trr.blockhash,
                     "amount": trr.amount,
                     "nonce": trr.nonce,
                     "first_timestamp": trr.first_timestamp,
                     "saved_timestamp": trr.saved_timestamp.strftime("%Y-%m-%d"),
                     "P2PKH": trr.P2PKH,
                     "verification": trr.verification})


    data['timeline'] = incomes[::-1]
    data['wallet'] = wallet
    balance = gbfw(wallet)
    data['balance'] = balance


    return HttpResponse(json.dumps(data), content_type = "application/json")

def gettransaction(request, tid):
        data = {}
        trr = transaction.objects.get(id=int(tid))
        data = {"sender" : trr.sender,
                     "senderwallet": trr.senderwallet,
                     "receiver": trr.receiver,
                     "prevblockhash": trr.prevblockhash,
                     "blockhash": trr.blockhash,
                     "amount": trr.amount,
                     "nonce": trr.nonce,
                     "first_timestamp": trr.first_timestamp,
                     "saved_timestamp": trr.saved_timestamp.strftime("%Y-%m-%d"),
                     "P2PKH": trr.P2PKH,
                     "verification": trr.verification}
        return HttpResponse(json.dumps(data), content_type = "application/json")


def alltransactions(request):
    data = {}
    txs = []
    transactions = transaction.objects.all()
    for trr in transactions:
        gettrs = {"sender" : trr.sender,
                     "senderwallet" : trr.senderwallet,
                     "receiver": trr.receiver,
                     "prevblockhash": trr.prevblockhash,
                     "blockhash": trr.blockhash,
                     "amount": trr.amount,
                     "nonce": trr.nonce,
                     "first_timestamp": trr.first_timestamp,
                     "saved_timestamp": trr.saved_timestamp.strftime("%Y-%m-%d"),
                     "P2PKH": trr.P2PKH,
                     "verification": trr.verification,
                     "id":trr.id}
        txs.append(gettrs)

    data['alltestsarecomplated'] = txs
    return HttpResponse(json.dumps(data), content_type = "application/json")
