from django.shortcuts import render
import json
import pytz
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.views.decorators.http import require_POST

from . import models
from . import serializers

# Create your views here.

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
@api_view(["GET", ])
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
    obj_string = request.POST['products']
    user_id = request.data['user']
    remark = request.data['remark']
    user = User.objects.get(id=user_id)
    object_product = json.loads(obj_string)
    products = []

    total_price = 0
    discount = 0

    status = True
    
    for i, o in dict(object_product).items():
        pro = {}
        for x, y in o.items():
            pro[x] = y
            if x == 'total_price':
                total_price += y
            if x == 'discount':
                discount += y
        products.append(pro)

    print(products)
    print(total_price, discount)

    try:
        shop = models.ShopData.objects.get(user=user)

        if models.InputInvoice.objects.all().count() == 0:

            inv_id = 100001
            invoice = models.InputInvoice.objects.create(
                invoice_id=inv_id,
                shop=shop,
                remark=remark,
                total_price=total_price,
                discount=discount,
            )

        else:

            invoice = models.InputInvoice.objects.create(
                shop=shop,
                remark=remark,
                total_price=total_price,
                discount=discount,
            )

        models.InputInvoice.objects.filter(invoice_id=invoice.invoice_id).update(
            invoice_no=f"I{shop.shop_code}{invoice.invoice_id}"
        )

        for product in products:
            product_name = product['product_name']
            product_desc = product['product_detail']
            product_cost = product['price']
            product_unit = product['unit']
            product_disc = product['discount']

            _product = models.ProductData.objects

            if models.ProductData.objects.all().count() == 0:

                _product = models.ProductData.objects.create(
                    product_id=100000,
                    product_name=product_name,
                    unit_cost=product_cost,
                    product_desc=product_desc
                )
            else:
                _product = models.ProductData.objects.create(
                    product_name=product_name,
                    unit_cost=product_cost,
                    product_desc=product_desc
                )

            models.ProductData.objects.filter(product_id=_product.product_id).update(
                product_code=f"P{_product.product_id}")

            print(
                f"No. {models.InputInvoice.objects.get(invoice_id=invoice.invoice_id).invoice_no}"
            )

            models.InputData.objects.create(
                invoice=invoice,
                invoice_no=models.InputInvoice.objects.get(
                    invoice_id=invoice.invoice_id).invoice_no,
                product=_product,
                quantity=product_unit,
                discount=product_disc,
                unit_price=product_cost

            )

            models.TempInputDB.objects.create(
                invoice=invoice.invoice_id,
                invoice_no=models.InputInvoice.objects.get(
                    invoice_id=invoice.invoice_id).invoice_no,
                product=models.ProductData.objects.get(
                    product_id=_product.product_id).product_code,
                quantity=product_unit,
                discount=product_disc,
                unit_price=product_cost
            )
            
    except TypeError as err:
        print(err)
        status = False

    return Response({
        "status": status
    })


@csrf_exempt
@api_view(["POST",])
@permission_classes((AllowAny,))
def createShop(request):
    data = request.data

    status = True
    _username = data['username']
    _password = data['password']
    _shop_name = data['shop_name']
    _product_type = data['product_type']
    _contact = data['contact']
    _province = data['province']
    _district = data['district']
    _subDistrict = data['sub_district']
    _post_id = data['post_id']
    _detail_address = data['detail_address']
    _tel = data['tel']
    _fax = data['fax']
    _email = data['email']
    _remark = data['remark']

    if User.objects.filter(username=_username).count() != 0:
        return Response({"status": False, "message": 'มีชื่อผู้ใช้นี้แล้ว'})

    try:
        _user = User.objects.create_user(
            email=_email,
            username=_username,
            password=_password
        )
        if _user:

            if models.ShopData.objects.all().count() == 0:
                shop_id = 10000

                shop = models.ShopData.objects.create(
                    user=_user,
                    user_status=1,
                    shop_id=shop_id,
                    shop_name=_shop_name,
                    shop_product_type=_product_type,
                    shop_contact=_contact,
                    shop_post_code=_post_id,
                    shop_province=_province,
                    shop_district=_district,
                    shop_subdistrict=_subDistrict,
                    shop_detail_address=_detail_address,
                    shop_tel=_tel,
                    shop_fax=_fax,
                    shop_email=_email,
                    shop_remark=_remark
                )

            else:

                shop = models.ShopData.objects.create(
                    user=_user,
                    user_status=1,
                    shop_name=_shop_name,
                    shop_product_type=_product_type,
                    shop_contact=_contact,
                    shop_post_code=_post_id,
                    shop_province=_province,
                    shop_district=_district,
                    shop_subdistrict=_subDistrict,
                    shop_detail_address=_detail_address,
                    shop_tel=_tel,
                    shop_fax=_fax,
                    shop_email=_email,
                    # shop_remark = _remark
                )

            models.ShopData.objects.filter(shop_id=shop.shop_id).update(
                shop_code=f"S{shop.shop_id}")

    except TypeError as err:

        status = False
        print(err)

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
@api_view(["GET"])
@permission_classes((AllowAny,))
def getAllShop(request):
    status = True

    shop_data = models.ShopData.objects.all()
    shop = serializers.ShopDataSerializer(shop_data, many=True).data

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
