from django.urls import path
from cameraRentApp import views

urlpatterns = [

    # BUYER

    path('', views.indexPage),
    path('user-signup/', views.userSignup),
    path('user-login/', views.userLogin),
    path('user-view-product/', views.userViewProduct),
    path('user-view-bookings/', views.userViewBookings),
    path('check-date-availability/', views.checkDateAvailability),
    path('user-update-profile/', views.userUpdateProfile),
    path('user-update-booking/', views.userUpdateBooking),
    path('user-cancel-booking/', views.userCancelBooking),
    path('user-delete/', views.userDelete),
    path('user-logout/', views.userLogout),

    # SELLER

    path('seller-login/', views.sellerLogin),
    path('seller-signup/', views.sellerSignup),
    path('seller-add-product/', views.sellerAddProduct),
    path('seller-update-product/', views.sellerUpdateProduct),
    path('seller-delete-product/', views.sellerDeleteProduct),
    path('seller-view-product/', views.sellerViewProduct),
    path('seller-view-bookings/', views.sellerViewBookings),
    path('seller-update-profile/', views.sellerUpdateProfile),
    path('seller-delete/', views.sellerDelete),
    path('seller-logout/', views.sellerLogout),

    # ADMIN

    path('admin-login/', views.adminLogin),
    path('admin-logout/', views.adminLogout),
    path('admin-view-products/', views.adminViewProducts),
    path('admin-view-sellers/', views.adminViewSellers),
    path('admin-approved-booking/', views.adminApprovedBooking),
    path('admin-disapproved-booking/', views.adminDisapprovedBooking),
    path('admin-approved-seller/', views.adminApprovedSeller),
    path('admin-disapproved-seller/', views.adminDisapprovedSeller),
    path('admin-view-users/', views.adminViewUsers),
    path('admin-view-bookings/', views.adminViewBookings),
    path('seller-update/', views.sellerUpdateTable),
    path('user-update/', views.userUpdateTable),
]