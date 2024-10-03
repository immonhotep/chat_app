from typing import Any
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from django.views.generic.list import MultipleObjectMixin
from .models import Room,Message,ForumCategory,ForumMessage,ForumMessageReport,Connected
from .forms import EditForumMessageForm,ReportMessageForm,CreateForumCategoryForm,RoomCreateForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .mixins import SuperUserRequiredMixin
import time

import uuid


class Roomview(LoginRequiredMixin,ListView):

    queryset = Room.objects.filter(private=False)
    template_name = 'rooms/rooms.html'
    ordering = ['-name']
    paginate_by = 6

    
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class Forumview(ListView):

    queryset = ForumCategory.objects.all()
    template_name = 'rooms/forums.html'
    ordering = ['-name']
    paginate_by = 6




class RoomDetailView(LoginRequiredMixin,View):

    def get(self,request,slug):

        user = self.request.user

        room = get_object_or_404(Room,slug=slug)
        messages = Message.objects.filter(room=room)[0:25]


       

        if room.private:

            if user not in room.participant.all():

                return redirect('permission_denied')
        
        
        context={'room':room,'messages':messages}
        return render(self.request,'rooms/room.html',context)



    login_url = "/login/"
    redirect_field_name = "redirect_to"




class ForumDetailView(DetailView):

    model = ForumCategory
    template_name='rooms/forum.html'
      

 
    def get_context_data(self, *args, **kwargs):

        context = super(ForumDetailView,self).get_context_data(*args, **kwargs)
        category = get_object_or_404(ForumCategory,slug=self.kwargs['slug'])
        comments = ForumMessage.objects.filter(category=category).order_by('-date_added')
        
        
        context['category'] = category
        context['comments'] = comments
        
    
        
        return context




class CreateForumMessageView(LoginRequiredMixin,View):

    def post(self,request,slug):

        category = get_object_or_404(ForumCategory,slug=slug)


        comment = self.request.POST.get('comment')
        ForumMessage.objects.create(category=category,user=request.user,message=comment)
        messages.success(self.request,'You posted new comment')
        return  redirect('forum_detail',category.slug)
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"
        
        

class DeleteMessageview(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = ForumMessage

    template_name = 'rooms/delete_confirmation.html'
    
    def get_success_message(self,cleaned_data):
            return('Comment deleted' )
    
    def get_success_url(self,**kwargs):

        return reverse_lazy('forum_detail',kwargs={'slug': self.object.category.slug})
    
    def test_func(self):

        object = self.get_object()
        if object.user == self.request.user:
            return True
        else:
            messages.error(self.request,'This is not your comment')
            return False
            
    def handle_no_permission(self):

        return redirect('permission_denied')    

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class EditForumMessageView(LoginRequiredMixin,View):

    def get(self,request,pk):

        message = get_object_or_404(ForumMessage,pk=pk)

        if message.user == self.request.user:
            form = EditForumMessageForm(instance=message)
            context = {'form':form,'page_name':'update_comment'}
            return render(self.request,'rooms/universal_form.html',context)
        
        else:
            return redirect('permission_denied')
        

    def post(self,request,pk):

        message = get_object_or_404(ForumMessage,pk=pk)

        if message.user == self.request.user:
            form = EditForumMessageForm(request.POST,instance=message)
            if form.is_valid():
                form.save()
                messages.success(self.request,'Your post updated')
                return redirect('forum_detail',message.category.slug)

            else:
                for error in list(form.errors.values()):
                    messages.error(self.request,error)
        else:

            return redirect('permission_denied')

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ReportCommentView(LoginRequiredMixin,View):

    def get(self,request,pk):
        
        form = ReportMessageForm()
        context={'form':form,'page_name':'report_comment'}
        return render(self.request,'rooms/universal_form.html',context)


    def post(self,request,pk):
        
        form = ReportMessageForm(self.request.POST)

        message = get_object_or_404(ForumMessage,pk=pk)

        if form.is_valid():
            report = form.save(commit=False)
            report.message = message
            report.user = self.request.user
            form.save()
            messages.success(self.request,'Your report has been saved')

            return redirect('forum_detail',message.category.slug)
        
        else:
            for error in list(form.errors.values()):
                messages.error(self.request,error)

                return redirect('forum_detail',message.category.slug)
            
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ReplyCommentView(LoginRequiredMixin,View):

    def get(self,request,pk):
        
        form = EditForumMessageForm()
        context={'form':form,'page_name':'reply_comment'}
        return render(self.request,'rooms/universal_form.html',context)

    def post(self,request,pk):

        message = get_object_or_404(ForumMessage,pk=pk)
        category = message.category

        form = EditForumMessageForm(self.request.POST)
 

        if form.is_valid():
            comment = form.save(commit=False)
            comment.category = category
            comment.user = self.request.user
            comment.reply = message
            comment.save()
            messages.success(self.request,'You replied to the comment')
            return redirect('forum_detail',message.category.slug)

        else:
            for error in list(form.errors.values()):
                messages.error(self.request,error)
                return redirect('forum_detail',message.category.slug)

        login_url = "/login/"
        redirect_field_name = "redirect_to"

   


    
class OpenPrivateRoom(LoginRequiredMixin,View):


    def get(self,request,pk):

        user = self.request.user
        partner = get_object_or_404(User,pk=pk)
       
    
        private_room = Room.objects.filter(participant=user).filter(participant=partner).distinct().first()
        
        if private_room:
            
            return redirect('room_detail',private_room.slug)

        else:
            name = uuid.uuid4().hex
            room = Room.objects.create(name=name,private=True)
         
            room.participant.add(user)
            room.participant.add(partner)
            room.save()
            return redirect('room_detail',room.slug)


    login_url = "/login/"
    redirect_field_name = "redirect_to"




class SeeMyMessageview(LoginRequiredMixin,View):

    def get(self,request):

        mymessages = Message.objects.filter(checked=False,room__participant=request.user,room__private=True).exclude(user=request.user).order_by('-date_added')[0:5]
        
        p = Paginator(mymessages,8)
        page = self.request.GET.get('page')
    
        try:
            mymessages = p.page(page)
        except PageNotAnInteger:
            mymessages = p.page(1)
        except EmptyPage:
            mymessages = p.page(p.num_pages)
        
        
        context = {'mymessages':mymessages}
        return render(self.request,'rooms/mymessages.html',context)


    login_url = "/login/"
    redirect_field_name = "redirect_to"



class CheckMyMessageView(LoginRequiredMixin,View):

    def get(self,request,pk):

        message = get_object_or_404(Message,pk=pk)

        if request.user in message.room.participant.all() and request.user != message.user:

            message.checked = True
            message.save()
            messages.success(self.request,f'You set {message.user.username} message to read')
            return redirect('mymessages')
        
        else:
            return redirect('permission_denied')
       
    login_url = "/login/"
    redirect_field_name = "redirect_to"




class CheckAllmessageView(LoginRequiredMixin,View):


    def post(self,request):

        mymessages = Message.objects.filter(checked=False,room__participant=request.user,room__private=True).exclude(user=request.user).order_by('-date_added')

        checked = self.request.POST.get('MessageCheck')

        if checked == "all_checked":

            for message in mymessages:

                message.checked = True
                message.save()

            messages.success(self.request,'You set all message to read')

            return redirect('mymessages')
        
        else:
            return redirect('mymessages')
        
    login_url = "/login/"
    redirect_field_name = "redirect_to"





class CreateForumView(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = ForumCategory
    form_class = CreateForumCategoryForm
    template_name = 'rooms/universal_form.html'


    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

    def form_invalid(self,form):

        for error in list(form.errors.values()):
            messages.error(self.request,error)   
        return self.render_to_response(self.get_context_data(form=form))
    

    def get_success_message(self,cleaned_data):
        return('New forum successfully create' )
    

    def get_success_url(self):
      return reverse_lazy('forums')
    

    def get_context_data(self, *args, **kwargs):
        context = super(CreateForumView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "create_forum"
        return context
    


    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ForumEditView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):

    model = ForumCategory
    form_class = CreateForumCategoryForm
    template_name = 'rooms/universal_form.html'

    def get_success_message(self, cleaned_data):
        return ('forum updated')
    
    def get_success_url(self):
        return reverse_lazy('forums')
    
    def test_func(self):

        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            return False
        
    def get_context_data(self, *args, **kwargs):
        context = super(ForumEditView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "edit_forum"
        return context

    def handle_no_permission(self):
        return redirect('permission_denied')

    login_url = "/login/"
    redirect_field_name = "redirect_to"





class DeleteForumview(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = ForumCategory

    template_name = 'rooms/delete_confirmation.html'
    
    def get_success_message(self,cleaned_data):
            return('Forum deleted' )
    
    def get_success_url(self,**kwargs):

        return reverse_lazy('forums')
    
    def test_func(self):

        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            return False
            
    def handle_no_permission(self):

        return redirect('permission_denied')    

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class CreateChatRoomView(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = Room
    form_class = RoomCreateForm
    template_name = 'rooms/universal_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

    def form_invalid(self,form):

        for error in list(form.errors.values()):
            messages.error(self.request,error)   
        return self.render_to_response(self.get_context_data(form=form))
    

    def get_success_message(self,cleaned_data):
        return('New room successfully created' )
    

    def get_success_url(self):
      return reverse_lazy('rooms')
    

    def get_context_data(self, *args, **kwargs):
        context = super(CreateChatRoomView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "create_room"
        return context
    


    login_url = "/login/"
    redirect_field_name = "redirect_to"




class RoomEditView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):

    model = Room
    form_class = RoomCreateForm
    template_name = 'rooms/universal_form.html'

    def get_success_message(self, cleaned_data):
        return ('room updated')
    
    def get_success_url(self):
        return reverse_lazy('rooms')
    
    def test_func(self):

        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            return False
        
    def get_context_data(self, *args, **kwargs):
        context = super(RoomEditView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "edit_room"
        return context

    def handle_no_permission(self):
        return redirect('permission_denied')

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class DeleteRoomview(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = Room

    template_name = 'rooms/delete_confirmation.html'
    
    def get_success_message(self,cleaned_data):
            return('Room deleted' )
    
    def get_success_url(self,**kwargs):

        return reverse_lazy('rooms')
    
    def test_func(self):

        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            return False
            
    def handle_no_permission(self):

        return redirect('permission_denied')    

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ShowCommentReportView(SuperUserRequiredMixin,ListView):


    queryset = ForumMessageReport.objects.all()
    template_name = 'rooms/show_reports.html'
    ordering = ['-report_date']
    paginate_by = 1

    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class AllowReportedCommentView(SuperUserRequiredMixin,View):

    def get(self,request,pk):

        comment = get_object_or_404(ForumMessage,pk=pk)

        reports = ForumMessageReport.objects.filter(message=comment)

        if comment.hidden == True:
            comment.hidden = False
            comment.save()

        reports.delete()
        messages.success(self.request,'You allowed the reported comment and removed the reports')
        
        return redirect('forum_detail',comment.category.slug)



    login_url = "/login/"
    redirect_field_name = "redirect_to"


class HideCommentView(SuperUserRequiredMixin,View):

    def get(self,request,pk):

        comment = get_object_or_404(ForumMessage,pk=pk)
        comment.hidden = True
        comment.save()
        messages.success(self.request,'You hidden the comment message')
        return redirect('forum_detail',comment.category.slug)


    login_url = "/login/"
    redirect_field_name = "redirect_to"






class Permission_Deniedview(View):

    def get(self,request):

        return render(self.request,'rooms/permission_denied.html')
    


