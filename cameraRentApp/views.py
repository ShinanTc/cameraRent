from errno import ESTALE
from telnetlib import STATUS
from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from cameraRentApp.models import *
from django.contrib.auth.models import User

# Create your views here.


def indexPage(request):
    if request.session.has_key('admin_id'):
        return HttpResponseRedirect('/admin-view-users/')
    else:
        product_details = product_tb.objects.all()
        return render(request, 'index.html', {'product_details': product_details})


def userLogin(request):
    if request.method == "POST":
        name = request.POST['user_name']
        pwd = request.POST['user_pwd']
        u_tb = user_tb.objects.filter(user_name=name, user_password=pwd)
        if u_tb:
            for x in u_tb:
                request.session['user_id'] = x.id
            return HttpResponseRedirect('/')
        else:
            return render(request, 'user/user_login.html')
    else:
        return render(request, 'user/user_login.html')


def userSignup(request):
    if request.method == 'POST':
        buyerName = request.POST['buyer_name']
        name = request.POST['user_name']
        email = request.POST['user_email']
        phone = request.POST['user_phone']
        pwd = request.POST['user_pwd']
        u_tb = user_tb(buyer_name=buyerName, user_name=name,
                       user_email=email, user_phone=phone, user_password=pwd)
        u_tb.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'user/user_reg.html')


def userViewProduct(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            pid = request.POST['product_id']
            # creating an instance for product_id using product_tb 'id'
            product_id = product_tb.objects.get(id=pid)
            fromDate = request.POST['booking-from']
            toDate = request.POST['booking-to']
            user_id = request.session['user_id']
            user_id = user_tb.objects.get(id=user_id)
            query = product_tb.objects.filter(id=pid)

            for x in query:
                seller_id = x.seller_id
                b_tb = book_tb(user_id=user_id, product_id=product_id, seller_id=seller_id,
                               book_from=fromDate, book_to=toDate)
                b_tb.save()
            return HttpResponseRedirect('/')
        else:
            id = request.GET['product_id']
            product_details = product_tb.objects.filter(id=id)
            return render(request, 'user/user_view_product.html', {'product_details': product_details})
    else:
        return HttpResponseRedirect('/')


def userViewBookings(request):
    if request.session.has_key('user_id'):
        userId = request.session['user_id']
        bookDetails = book_tb.objects.filter(user_id=userId)
        return render(request, 'user/user_view_bookings.html', {'bookDetails': bookDetails})
    else:
        return HttpResponseRedirect('/')


def checkDateAvailability(request):
    if request.session.has_key('user_id'):
        fromDate = request.GET['booking_from']
        toDate = request.GET['booking_to']
        product_id = request.GET['product_id']
        print("Inside function")
        productAvailable = book_tb.objects.filter(product_id=product_id)
        if productAvailable.exists():
            if productAvailable.raw('SELECT a.* FROM (SELECT * FROM camerarentapp_book_tb WHERE product_id_id=%s)a WHERE %s BETWEEN book_from AND book_to', [product_id, fromDate]):
                dateAvailability = {'dateExist': 'false'}
                return JsonResponse(dateAvailability)
            elif productAvailable.raw('SELECT a.* FROM (SELECT * FROM camerarent_app_book_tb WHERE product_id_id=%s)a WHERE %s BETWEEN book_from AND book_to', [product_id, toDate]):
                dateAvailability = {'dateExist': 'false'}
                return JsonResponse(dateAvailability)
            else:
                dateAvailability = {'dateExist': 'false'}
                return JsonResponse(dateAvailability)
        else:
            dateAvailability = {'dateExist': 'false'}
            return JsonResponse(dateAvailability)
    else:
        return HttpResponseRedirect('/')


def userUpdateTable(request):
    if request.method == 'POST':
        id = request.POST['user_id']
        buyerName = request.POST['buyer_name']
        name = request.POST['user_name']
        email = request.POST['user_email']
        phone = request.POST['user_phone']
        pwd = request.POST['user_pwd']
        u_tb = user_tb.objects.filter(id=id).update(
            buyer_name=buyerName, user_name=name, user_email=email, user_phone=phone, user_password=pwd)
        return HttpResponseRedirect('/user-table/')
    else:
        user_id = request.GET['user_id']
        user_details = user_tb.objects.filter(id=user_id)
        return render(request, 'admin/user_update.html', {"user_details": user_details})


def userUpdateProfile(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            id = request.POST['user_id']
            buyerName = request.POST['buyer_name']
            name = request.POST['user_name']
            email = request.POST['user_email']
            phone = request.POST['user_phone']
            u_tb = user_tb.objects.filter(id=id).update(
                buyer_name=buyerName, user_name=name, user_email=email, user_phone=phone)
            return HttpResponseRedirect('/')
        else:
            id = request.session['user_id']
            user_details = user_tb.objects.filter(id=id)
            return render(request, 'user/user_update_profile.html', {'user_details': user_details})


def userUpdateBooking(request):
    if request.session.has_key('user_id'):
        if request.method == "POST":
            pid = request.POST['product_id']
            # creating an instance for product_id using product_tb 'id'
            fromDate = request.POST['booking-from']
            toDate = request.POST['booking-to']
            user_id = request.session['user_id']
            book_tb.objects.filter(user_id=user_id).update(
                book_from=fromDate, book_to=toDate)
            return HttpResponseRedirect('/')
        else:
            book_id = request.GET['booking_id']
            query = book_tb.objects.filter(id=book_id)
            return render(request, 'user/user_update_booking.html', {'product_details': query})
    else:
        HttpResponseRedirect('/user-login/')


def userCancelBooking(request):
    if request.session.has_key('user_id'):
        bookId = request.GET['booking_id']
        book_tb.objects.filter(id=bookId).delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('user-login/')


def userDelete(request):
    user_id = request.GET['user_id']
    user_tb.objects.filter(id=user_id).delete()
    return HttpResponseRedirect('/user-table/')


def userLogout(request):
    if request.session.has_key('user_id'):
        del request.session['user_id']
    return HttpResponseRedirect('/')


def sellerLogin(request):
    if request.method == 'POST':
        name = request.POST['seller_name']
        pwd = request.POST['seller_pwd']
        s_tb = seller_tb.objects.filter(
            user_name=name, user_password=pwd, status='approved')
        if s_tb:
            for x in s_tb:
                request.session['seller_id'] = x.id
        return HttpResponseRedirect('/')
    else:
        return render(request, 'seller/seller_login.html')


def sellerSignup(request):
    if request.method == 'POST':
        sellerName = request.POST['seller_name']
        name = request.POST['user_name']
        email = request.POST['user_email']
        pwd = request.POST['user_pwd']
        s_tb = seller_tb(seller_name=sellerName, user_name=name,
                         user_email=email, user_password=pwd)
        s_tb.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'seller/seller_reg.html')


def sellerAddProduct(request):
    if request.method == 'POST':
        name = request.POST['product-name']
        price = request.POST['product-price']
        description = request.POST['product-description']
        image = request.FILES['product-img']
        sid = request.session['seller_id']
        sellerId = seller_tb.objects.get(id=sid)
        p_tb = product_tb(product_name=name, product_price=price, product_img=image,
                          product_description=description, seller_id=sellerId)
        p_tb.save()
    return render(request, 'seller/seller_addproduct.html')


def sellerViewProduct(request):
    product_details = product_tb.objects.all()
    return render(request, 'seller/seller_viewproduct.html', {'product_details': product_details})


def sellerViewBookings(request):
    if request.session.has_key('seller_id'):
        sellerId = request.session['seller_id']
        bookDetails = book_tb.objects.filter(id=sellerId)
        return render(request, 'seller/seller_view_bookings.html', {'bookDetails': bookDetails})
    else:
        return HttpResponseRedirect('/')


def sellerUpdateProduct(request):
    if request.session.has_key('seller_id'):
        if request.method == 'POST':
            id = request.POST['product_id']
            name = request.POST['product_name']
            image = request.POST['product_img']
            price = request.POST['product_price']
            description = request.POST['product_description']
            p_tb = product_tb.objects.filter(id=id).update(
                product_name=name, product_img=image, product_price=price, product_description=description)
            return HttpResponseRedirect('/seller-view-product/')
        else:
            id = request.GET['product_id']
            product_details = product_tb.objects.filter(id=id)
            return render(request, 'seller/seller_update_product.html', {"product_details": product_details})


def sellerDeleteProduct(request):
    if request.session.has_key('seller_id'):
        id = request.GET['pid']
        product_tb.objects.filter(id=id).delete()
        return HttpResponseRedirect('/seller-view-product/')
    else:
        return HttpResponseRedirect('/seller-view-product/')


def sellerUpdateTable(request):
    if request.method == 'POST':
        id = request.POST['seller_id']
        sellerName = request.POST['seller_name']
        name = request.POST['user_name']
        email = request.POST['user_email']
        pwd = request.POST['user_pwd']
        s_tb = seller_tb.objects.filter(id=id).update(
            seller_name=sellerName, user_name=name, user_email=email, user_password=pwd)
        return HttpResponseRedirect('/seller-table/')
    else:
        id = request.GET['seller_id']
        seller_details = seller_tb.objects.filter(id=id)
        return render(request, 'admin/seller_update.html', {'seller_details': seller_details})


def sellerUpdateProfile(request):
    if request.session.has_key('seller_id'):
        if request.method == 'POST':
            id = request.POST['seller_id']
            sellerName = request.POST['seller_name']
            name = request.POST['user_name']
            email = request.POST['user_email']
            s_tb = seller_tb.objects.filter(id=id).update(
                seller_name=sellerName, user_name=name, user_email=email)
            return HttpResponseRedirect('/')
        else:
            id = request.session['seller_id']
            seller_details = seller_tb.objects.filter(id=id)
            return render(request, 'seller/seller_update_profile.html', {'seller_details': seller_details})


def sellerDelete(request):
    id = request.GET['seller_id']
    slr = seller_tb.objects.filter(id=id).delete()
    return HttpResponseRedirect('/seller-table/')


def sellerLogout(request):
    if request.session.has_key('seller_id'):
        del request.session['seller_id']
    return HttpResponseRedirect('/')


def adminLogin(request):
    if request.method == 'POST':
        name = request.POST['admin-name']
        pwd = request.POST['admin-pwd']
        a_tb = User.objects.filter(username=name, password=pwd)
        if a_tb:
            for x in a_tb:
                request.session['admin_id'] = x.id
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return render(request, 'admin/admin_login.html')


def adminViewProducts(request):
    if request.session.has_key('admin_id'):
        products = product_tb.objects.all()
        return render(request, 'admin/admin_view_products.html', {'products': products})
    else:
        return HttpResponseRedirect('/')


def adminViewSellers(request):
    if request.session.has_key('admin_id'):
        adminId = request.session['admin_id']
        adminDetails = User.objects.filter(id=adminId)
        sellersList = seller_tb.objects.all()
        return render(request, 'admin/admin_view_sellers.html', {'sellers': sellersList, 'adminDetails': adminDetails})
    else:
        return HttpResponseRedirect('/')


def adminApprovedSeller(request):
    if request.session.has_key('admin_id'):
        sellerId = request.GET['seller_id']
        seller_tb.objects.filter(
            id=sellerId).update(status="approved")
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def adminDisapprovedSeller(request):
    if request.session.has_key('admin_id'):
        sellerId = request.GET['seller_id']
        seller_tb.objects.filter(
            id=sellerId).delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def adminApprovedBooking(request):
    if request.session.has_key('admin_id'):
        bookingId = request.GET['booking_id']
        seller_tb.objects.filter(
            id=bookingId).update(status="appproved")
    else:
        return HttpResponseRedirect('/')


def adminDisapprovedBooking(request):
    if request.session.has_key('admin_id'):
        bookingId = request.GET['booking_id']
        seller_tb.objects.filter(
            id=bookingId).delete()
    else:
        return HttpResponseRedirect('/')


def adminViewUsers(request):
    if request.session.has_key('admin_id'):
        adminId = request.session['admin_id']
        adminDetails = User.objects.filter(id=adminId)
        userList = user_tb.objects.all()
        return render(request, 'admin/admin_view_users.html', {'users': userList, 'adminDetails': adminDetails})
    else:
        return HttpResponseRedirect('/')


def adminViewProducts(request):
    if request.session.has_key('admin_id'):
        adminId = request.session['admin_id']
        adminDetails = User.objects.filter(id=adminId)
        productList = product_tb.objects.all()
        return render(request, 'admin/admin_view_products.html', {'products': productList, 'adminDetails': adminDetails})
    else:
        return HttpResponseRedirect('/')


def adminViewBookings(request):
    if request.session.has_key('admin_id'):
        adminId = request.session['admin_id']
        adminDetails = User.objects.filter(id=adminId)
        bookingList = book_tb.objects.all()
        return render(request, 'admin/admin_view_bookings.html', {'bookings': bookingList, 'adminDetails': adminDetails})
    else:
        HttpResponseRedirect('/')


def adminLogout(request):
    if request.session.has_key('admin_id'):
        del request.session['admin_id']
    return HttpResponseRedirect('/')
