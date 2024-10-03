from django.urls import path
from .views import *
from . import views

urlpatterns = [

    path('rooms/',Roomview.as_view(),name='rooms'),
    path('room/<slug:slug>/',RoomDetailView.as_view(),name='room_detail'),
    path('forums/',Forumview.as_view(),name='forums'),
    path('forum/<slug:slug>/',ForumDetailView.as_view(),name='forum_detail'),
    path('save_comment/<slug:slug>/',CreateForumMessageView.as_view(),name='save_comment'),
    path('delete_comment/<int:pk>/',DeleteMessageview.as_view(),name='delete_comment'),
    path('update_comment/<int:pk>/',EditForumMessageView.as_view(),name='update_comment'),
    path('report_comment/<int:pk>/',ReportCommentView.as_view(),name='report_comment'),
    path('reply_comment/<int:pk>/',ReplyCommentView.as_view(),name='reply_comment'),
    path('permission_denied',Permission_Deniedview.as_view(),name='permission_denied'),

    path('private_chat/<int:pk>/',OpenPrivateRoom.as_view(),name='private_chat'),
    path('mymessages/',SeeMyMessageview.as_view(),name='mymessages'),
    path('check_message/<int:pk>/',CheckMyMessageView.as_view(),name='check_message'),
    path('check_all/',CheckAllmessageView.as_view(),name='check_all'),

    path('create_forum/',CreateForumView.as_view(),name='create_forum'),
    path('update_forum/<slug:slug>/',ForumEditView.as_view(),name='update_forum'),
    path('delete_forum/<slug:slug>/',DeleteForumview.as_view(),name='delete_forum'),
    path('create_room/',CreateChatRoomView.as_view(),name='create_room'),
    path('update_room/<slug:slug>/',RoomEditView.as_view(),name='update_room'),
    path('delete_room/<slug:slug>/',DeleteRoomview.as_view(),name='delete_room'),
    path('show_reports/',ShowCommentReportView.as_view(),name='show_reports'),
    path('allow_comment/<int:pk>/',AllowReportedCommentView.as_view(),name='allow_comment'),
    path('hide_comment/<int:pk>/',HideCommentView.as_view(),name='hide_comment'),
    
    

]