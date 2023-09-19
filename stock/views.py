from django.shortcuts import render
import json
import pytz
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.views.decorators.http import require_POST

import random

from . import models
from . import serializers

# Create your views here.


def ProductCategory(category):
    if models.ProductCategory.objects.filter(category=category).count() != 0:
        category = models.ProductCategory.objects.get(category=category)
    else:
        category = models.ProductCategory.objects.create(category=category)

    return category


def shopCode():
    code = 'S'
    num = random.choices(range(10), k=10)

    for i in num:
        code += str(i)

    if models.ShopData.objects.filter(shop_code=code).count() != 0:
        shopCode()

    else:
        return code


def productCode():
    code = 'P'
    num = random.choices(range(10), k=10)

    for i in num:
        code += str(i)

    if models.ProductData.objects.filter(product_code=code).count() != 0:
        productCode()
    else:
        return code


def invoiceCode():
    code = 'I'
    num = random.choices(range(10), k=10)

    for i in num:
        code += str(i)

    if models.InputInvoice.objects.filter(invoice_no=code).count() != 0:
        invoiceCode()
    else:
        return code


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def userCheck(request):
    status = True
    message = ""

    username = request.data['username']
    email = request.data['email']
    try:

        if User.objects.filter(username=username).count() != 0:
            status = False
            message = "username"
        elif User.objects.filter(email=email).count() != 0:
            status = False
            message = "email"
    except Exception as err:
        print(err)

    return Response(
        {
            "status": status,
            "message": message
        }
    )


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def get_user(request):

    user_id = request.session['_auth_user_id']
    user_status = User.objects.get(id=user_id)

    return Response(
        {
            "status": True,
            "uid": user_id
        }
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getProvince(request):
    data = {}
    msg = 'already get thai province'

    result = finders.find('data/json/thai_province.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    data['province'] = province.keys()

    return Response(
        {
            'status': True,
            'message': msg,
            'data': data['province'],
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getDistrict(request):
    data = {}
    msg = 'already get thai district'
    print(request.data['province'])

    result = finders.find('data/json/thai_province.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    province_selected = request.data['province']
    data['district'] = province[province_selected].keys()

    return Response(
        {
            'status': True,
            'message': msg,
            'data': data['district'],
        }

    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def getTambon(request):
    data = {}
    msg = 'already get thai tambon'

    # get thai province file
    result = finders.find('data/json/thai_province.json')
    with open(result, encoding='utf-8') as f:
        province = json.load(f)

    province_selected = request.data['province']
    district_selected = request.data['district']

    data['tambon'] = province[province_selected][district_selected]

    return Response(
        {
            'status': True,
            'message': msg,
            'data': data['tambon']
        }
    )


@require_POST
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def createInputData(request):

    status = True
    user = User.objects.get(username=request.user.username)
    shop = models.ShopData.objects.get(user=user)

    obj_string = request.data['products'] # product list 
    remark = request.data['remark'] # remark
    total_cost = request.data['total_cost'] # total cost 
    total_price = request.data['total_price'] # total price
    total_discount = request.data['total_discount'] # total discount
    total = request.data['total'] #  total values 
    
    object_product = json.loads(obj_string)

    try:

        invoice = models.InputInvoice.objects.create(
            invoice_no=invoiceCode(),
            shop=shop,
            total_cost=total_cost,
            total_price=total,
            total_discount=total_discount,
            remark=remark
        )
        try:
            for products in object_product.values():
                product_code = productCode()
                product_name = products['product_name']
                product_desc = products['product_desc']
                product_price = products['price']
                product_unit = products['unit']
                product_cost = products['cost']
                product_category = ProductCategory(products['product_category'])

                product = models.ProductData.objects.create(
                    product_code=product_code,
                    product_name=product_name,
                    product_desc=product_desc,
                    product_price=product_price,
                    product_unit=product_unit,
                    product_cost=product_cost,
                    product_category=product_category,
                )
                models.InputData.objects.create(
                    invoice=invoice,
                    invoice_no=invoice.invoice_no,
                    product=product,
                    quantity=product_unit,
                    unit_price=product_price,
                    unit_cost=product_cost,
                    discount=products['discount']
                )
                models.ProductShop.objects.create(shop=shop, product=product)
                
        except Exception as err:
            print(err)

    except:
        models.InputInvoice.objects.filter(id=invoice.id).delete()

    return Response({
        "status": status
    })


@csrf_exempt
@api_view(["POST",])
@permission_classes((AllowAny,))
def createShop(request):
    data = request.data
    status = True
    fname = data['fname']
    lname = data['lname']
    username = data['username']
    password = data['password']
    email = data['email']
    shop_name = data['shop_name']
    shop_product_type = data['product_type']
    shop_contact = f"{fname} {lname}"
    shop_province = data['province']
    shop_district = data['district']
    shop_subdistrict = data['sub_district']
    shop_post_id = data['post_id']
    shop_address = data['detail_address']
    shop_tel = data['tel']
    shop_fax = data['fax']
    shop_email = email
    shop_remark = data['remark']
    shop_area = models.AreaData.objects.get(id=data['area'])

    if User.objects.filter(username=username).count() != 0:
        return Response({"status": False, "message": 'มีชื่อผู้ใช้นี้แล้ว'})

    try:
        # create user on main user >>>
        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=fname, last_name=lname)
        if user:
            # check shop product type >>>
            if models.ProductTypeData.objects.filter(type_name=shop_product_type).count() == 0:
                shop_product_type = models.ProductTypeData.objects.create(
                    type_name=shop_product_type)
            else:
                shop_product_type = models.ProductTypeData.objects.get(
                    type_name=shop_product_type)

            # create shop data
            shop_create = models.ShopData.objects.create(
                user=user,
                user_status=1,
                shop_code=shopCode(),
                shop_name=shop_name,
                shop_product_type=shop_product_type,
                shop_contact=shop_contact,
                shop_province=shop_province,
                shop_district=shop_district,
                shop_subdistrict=shop_subdistrict,
                shop_detail_address=shop_address,
                shop_tel=shop_tel,
                shop_post_code=shop_post_id,
                shop_fax=shop_fax,
                shop_email=shop_email,
                shop_remark=shop_remark,
                shop_area_code=shop_area,
            )
            if shop_create:
                status = True

    except Exception as err:
        status = False
        User.objects.get(id=user.id).delete()

    return Response(
        {
            "status": status,
            "message": "success"
        }
    )


@csrf_exempt
@api_view(["POST",])
@permission_classes((AllowAny,))
def login_api(request):

    username = request.data['username']
    password = request.data['password']

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:
        if user.is_active:
            status = True
            msg = 'user is logined'
            login(request, user)
        else:
            status = False
            msg = 'Currently, This user is not active'
    else:
        status = False
        msg = 'Error wrong username/password'

    return Response({'status': status, 'message': msg})


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getArea(request):
    data = serializers.AreaSerializer(
        models.AreaData.objects.all(), many=True).data

    return Response(
        {
            "status": True,
            "data": data
        }
    )


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getProductType(request):
    data = serializers.ProductTypeSerializer(
        models.ProductTypeData.objects.all(), many=True).data

    return Response(
        {
            "status": True,
            "data": data
        }
    )


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def getProductCategory(request):
    user = User.objects.get(username=request.user.username)
    shop = models.ShopData.objects.get(user=user)
    product_type = models.ProductTypeData.objects.get(id=shop.shop_product_type.id)
    
    
    
    data = serializers.ProductCategorySerializer(
        models.ProductCategory.objects.filter(product_type=product_type), many=True).data

    return Response(
        {
            "status":True,
            "data":data
        }
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def getAllProduct(request):
    product_data = models.ProductData.objects.all()
    products = serializers.ProductDataSerializer(product_data, many=True).data

    return Response(
        {
            "status": True,
            "data": products
        }
    )


@csrf_exempt
@api_view(["GET",])
@permission_classes((AllowAny,))
def getProductShop(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    print(username)
    user = models.User.objects.get(username=username)
    print(user)
    shop = models.ShopData.objects.get(user=user)
    # invoice = models.InputInvoice.objects.get(shop=shop)
    invoice_data = models.InputInvoice.objects.filter(shop=shop)
    invoiceSerializerData = serializers.InputInvoiceSerializer(
        invoice_data, many=True).data
    # inputData_data = models.InputData.objects.filter(invoice=invoice)
    # inputDataSerializerData = serializers.InputDataSerializer(inputData_data, many=True).data
    return Response(
        {
            "status": 200,
            "data": {
                "invoice": invoiceSerializerData,
                # "input_data":inputDataSerializerData

            }
        }
    )


# show shop data input
# @csrf_exempt
# @api_view(["GET",])
# @permission_classes((AllowAny,))
# def shopDataInput(request):
#     user = User.objects.get(username=request.user.username)
#     shop = models.ShopData.objects.get(user=user)
#     invoice = models.InputInvoice.objects.filter(shop=shop)
#     data_input = models.InputData.objects.filter(invoice=invoice[1])
#     data = serializers.ShopInputData(data_input, many=True).data
#     print(data_input)
#     return Response(
#         {
#             "status":True,
#             "data":data
#         }
#     )
    

# show all user input invoice data (Use)
@csrf_exempt
@api_view(["GET",])
@permission_classes((AllowAny,))
def getShopInputInvoices(request):
    user = User.objects.get(username=request.user.username)
    shop = models.ShopData.objects.get(user=user)

    invoice_data = serializers.InputInvoiceSerializer(
        models.InputInvoice.objects.filter(shop=shop).order_by('-id'), many=True).data
    invoices = []
    for invoice in invoice_data:
        input_data = serializers.InputDataSerializer(
            models.InputData.objects.filter(invoice=int(invoice['id'])), many=True).data

        invoice['shop'] = models.ShopData.objects.get(
            id=int(invoice['shop'])).shop_name
        input_information = []
        for data in input_data:
            data['product'] = serializers.ProductDataSerializer(
                models.ProductData.objects.filter(id=int(data['product'])), many=True).data[0]
            data['product']['product_category'] = models.ProductCategory.objects.get(
                id=int(data['product']['product_category'])).category
            input_information.append(data)

        invoice["data_input"] = input_information

        invoices.append(invoice)

    return Response(
        {
            "status":True,
            "data":invoices
        }
    )

# get all shop 
@csrf_exempt
@api_view(["GET",])
@permission_classes((AllowAny,))
def getAllShop(request):
    status = True

    shop_data = models.ShopData.objects.all()
    shop = serializers.ShopDataSerializer(shop_data, many=True).data
    shop_all = []
    for item in shop:
        item['user'] = User.objects.get(id=item['user']).username
        item['shop_product_type'] = models.ProductTypeData.objects.get(
            id=item["shop_product_type"]).type_name
        shop_all.append(item)

    return Response(
        {
            "status": status,
            "data": shop
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def editProduct(request):

    edit = request.data
    status = True
    product_id = edit['product_id']
    product_name = edit['product_name']
    product_desc = edit['product_desc']
    unit_cost = edit['unit_cost']

    print(product_name)

    try:
        models.ProductData.objects.filter(product_id=product_id).update(
            product_name=product_name,
            product_desc=product_desc,
            unit_cost=unit_cost
        )

    except TypeError as err:
        print(err)
        status = False

    return Response(
        {
            "status": status
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def deleteProduct(request):
    id = request.data['product_code']
    models.ProductData.objects.filter(product_code=id).delete()

    return Response(
        {
            "status": True
        }
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def editShop(request):

    status = True

    shop_id = request.data['shop_id']
    shop_name = request.data['shop_name']
    shop_product_type = request.data['shop_product_type']
    shop_contact = request.data['shop_contact']
    shop_province = request.data['shop_province']
    shop_district = request.data['shop_district']
    shop_subdistrict = request.data['shop_subdistrict']
    shop_detail_address = request.data['shop_detail_address']
    shop_post_code = request.data['shop_post_code']
    shop_tel = request.data['shop_tel']
    shop_fax = request.data['shop_fax']
    shop_email = request.data['shop_email']
    shop_remark = request.data['shop_remark']

    try:
        models.ShopData.objects.filter(shop_id=shop_id).update(
            shop_name=shop_name,
            shop_product_type=shop_product_type,
            shop_contact=shop_contact,
            shop_province=shop_province,
            shop_district=shop_district,
            shop_subdistrict=shop_subdistrict,
            shop_detail_address=shop_detail_address,
            shop_post_code=shop_post_code,
            shop_tel=shop_tel,
            shop_fax=shop_fax,
            shop_email=shop_email,
            shop_remark=shop_remark
        )

    except TypeError as err:
        print(err)
        status = False

    return Response({
        "status": status
    })


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def deleteShop(request):
    id = request.data['shop_id']
    print(models.ShopData.objects.get(shop_id=id).user)

    User.objects.filter(
        username=models.ShopData.objects.get(shop_id=id).user).delete()

    return Response(
        {
            "status": True
        }
    )
