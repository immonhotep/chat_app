from django.urls import path
from .views import *

urlpatterns = [

    path('',Homeview.as_view(),name='home'),
    path('signup/',Signupview.as_view(),name='signup'),
    path('logout/',Mylogoutview.as_view(),name='logout'),
    path('login/',Myloginview.as_view(),name='login'),
    path('update_profile/',UpdateProfileView.as_view(),name='update_profile'),
    path('list_users/',UserListView.as_view(),name='list_users'),
    path('list_contacts/',ContactListView.as_view(),name='list_contacts'),
    path('remove_contact/<int:pk>/',RemoveContactView.as_view(),name='remove_contact'),
    path('list_requests/',ListRequestsView.as_view(),name='list_requests'),
    path('cancel_request/<int:pk>/',CancelRequestView.as_view(),name='cancel_request'),
    path('list_invitations/',ListInvitationsView.as_view(),name='list_invitations'),
    path('accept_invitations/<int:pk>/',AcceptInvitationView.as_view(),name='accept_invitations'),
    path('reject_invitations/<int:pk>/',RejectInvitationView.as_view(),name='reject_invitations'),
    path('connect_user/<int:pk>/',MakeFriendRequestView.as_view(),name='connect_user'),
    path('show_profile/<int:pk>/',UserProfileView.as_view(),name='show_profile'),
    path('change_password',CustomPassworchangeView.as_view(),name='change_password'),

]