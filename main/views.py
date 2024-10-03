from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import Signupform,UserLoginForm,UpdateUserForm,UpdateProfileForm,ChangePasswordForm
from django.contrib.auth import login,logout
from django.contrib import messages
from .models import Profile,FriendRequest
from rooms.models import Connected
from django.contrib.auth.models import User
from rooms.models import Room,Message,ForumCategory,ForumMessage
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.views.generic import ListView,DeleteView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q




class Homeview(View):
    
    def get(self,request):
    
        context={}
        return render(self.request,'main/frontpage.html',context)
    


class UserListView(LoginRequiredMixin,ListView):

    queryset = User.objects.all()
    template_name = 'main/users.html'
    ordering = ['-username']
    
    paginate_by = '8'

    def get_queryset(self):
        qs = super().get_queryset()   
        return qs.exclude(pk=self.request.user.pk)


    login_url = "/login/"
    redirect_field_name = "redirect_to"




class ContactListView(LoginRequiredMixin,View):

    def get(self,request):

        contacts = self.request.user.profile.contacts.all()

        p = Paginator(contacts,8)
        page = request.GET.get('page')
    
        try:
            contacts = p.page(page)
        except PageNotAnInteger:
            contacts = p.page(1)
        except EmptyPage:
            contacts = p.page(p.num_pages)


        context = {'contacts':contacts}
        return render(self.request,'main/contacts.html',context)

 

    login_url = "/login/"
    redirect_field_name = "redirect_to"





class Signupview(View):

    def get(self,request):
        
        form = Signupform()

        context={'form':form}
        return render(self.request,'main/signup.html',context)

    def post(self,request):
            
        form = Signupform(self.request.POST)
        if form.is_valid():     
            user = form.save()
            Profile.objects.create(user = user, pk=user.pk)
            login(self.request,user)

            messages.success(self.request,'You now logged in')
            messages.warning(self.request,'Please create your profile')
            return redirect('update_profile') 
                  
        else:
            for error in list(form.errors.values()):
                messages.error(self.request,error)

            return redirect('signup')
        


class UpdateProfileView(LoginRequiredMixin,View):
        

        def get(self,request):
            
            user = self.request.user
            profile = self.request.user.profile

            user_form = UpdateUserForm(instance=user)
            profile_form = UpdateProfileForm(instance=profile)

            context={'user_form':user_form,'profile_form':profile_form}
            return render(self.request,'main/update_user.html',context)


        def post(self,request):

            user = self.request.user
            profile = self.request.user.profile

            user_form = UpdateUserForm(self.request.POST,instance=user)
            profile_form = UpdateProfileForm(self.request.POST,request.FILES,instance=profile)

            if user_form.is_valid and profile_form.is_valid:
               user_form.save()
               profile_form.save()

               messages.success(self.request,'Your Profile updated')
               return redirect('home')

            else:

                for error in list(user_form.errors.values()):
                    return messages.error(self.request,error)
                
                for error in list(profile_form.errors.values()):
                    return messages.error(self.request,error)
                
                return redirect('update_profile')

        login_url = "/login/"
        redirect_field_name = "redirect_to"        

        

class Myloginview(SuccessMessageMixin,LoginView):

    template_name = 'main/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

   
    def get_success_message(self,cleaned_data):
        return(f'{self.request.user} logged in successfully' )
    

    def get_success_url(self):

        if self.request.user.is_superuser:
            try:
                self.request.user.profile
                return reverse('home')
            except:
                Profile.objects.create(user=self.request.user,pk=self.request.user.pk)
                messages.warning(self.request,'Update your profile')
                return reverse('update_profile')

        else:

            if self.request.user.profile.image:
                return reverse_lazy('home')
        
            else:
                messages.warning(self.request,'Please make your profile whole')
                return reverse('update_profile')


    def form_invalid(self,form):
        messages.error(self.request,'Invalid Username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

class Mylogoutview(LogoutView):


    def get_success_message(self,cleaned_data):
        return(f'{self.request.user} logged out successfully' )
    
    def get_success_url(self):
      
      return reverse_lazy('login')
    

class UserProfileView(LoginRequiredMixin,DetailView):

    model = Profile
    template_name = 'main/profile_detail.html'

    def get_context_data(self,*args, **kwargs):
        context=super(UserProfileView,self).get_context_data(*args, **kwargs)

        profile = get_object_or_404(Profile,pk=self.kwargs['pk'])
        context['profile'] = profile
        return context


    login_url = "/login/"
    redirect_field_name = "redirect_to"
    

    
class MakeFriendRequestView(LoginRequiredMixin,View):

    def get(self,request,pk):
        
        sender = self.request.user
        receiver = User.objects.get(pk=pk)

        if sender == receiver:
            messages.error(self.request,'Unable to connect to yourself')
            return redirect('home')

        if receiver.profile not in request.user.profile.contacts.all():

            friend_request, created =  FriendRequest.objects.get_or_create(sent_from=sender,sent_to=receiver)
            if created:
                messages.success(self.request,f'You sent connection request to {receiver}')
            else:
                messages.error(self.request,f'You already sent connection request to {receiver}')

            return redirect('list_users')
        
        else:
            messages.warning(self.request,f'{receiver} already in your contact list')
            return redirect('list_users')



    login_url = "/login/"
    redirect_field_name = "redirect_to" 


class ListRequestsView(LoginRequiredMixin,View):

    def get(self, request):
        requests = FriendRequest.objects.filter(sent_from=self.request.user).order_by('-sent_date')

        p = Paginator(requests,8)
        page = request.GET.get('page')
    
        try:
            requests = p.page(page)
        except PageNotAnInteger:
            requests = p.page(1)
        except EmptyPage:
            requests = p.page(p.num_pages)

        context={'requests':requests}
        return render(self.request,'main/list_requests.html',context)


    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ListInvitationsView(LoginRequiredMixin,View):

    def get(self, request):

        invitations = FriendRequest.objects.filter(sent_to=self.request.user).order_by('-sent_date')

        p = Paginator(invitations,8)
        page = request.GET.get('page')
    
        try:
            invitations = p.page(page)
        except PageNotAnInteger:
            invitations = p.page(1)
        except EmptyPage:
            invitations = p.page(p.num_pages)

        context={'invitations':invitations}
        return render(self.request,'main/list_invitations.html',context)


    login_url = "/login/"
    redirect_field_name = "redirect_to"



class CancelRequestView(LoginRequiredMixin,SuccessMessageMixin,UserPassesTestMixin,DeleteView):

    model = FriendRequest
    template_name = 'main/confirm_delete.html'

    def get_success_message(self,cleaned_data):
            return('Request Cancelled' )
    
    def get_success_url(self,**kwargs):

        return reverse_lazy('list_requests')
    
    def test_func(self):

        object = self.get_object()
        if object.sent_from == self.request.user:
            return True
        else:
            return False
            
    def handle_no_permission(self):
        return redirect('permission_denied')




    login_url = "/login/"
    redirect_field_name = "redirect_to"


class AcceptInvitationView(LoginRequiredMixin,View):


    def get(self,request,pk):

        invitation = FriendRequest.objects.get(pk=pk)

        if invitation.sent_to == self.request.user:

            if invitation.status == 1 or invitation.status == 3:

                invitation.status = 2
                invitation.save()
            
                self.request.user.profile.contacts.add(invitation.sent_from.profile)
                
                messages.success(self.request,f'You accepted {invitation.sent_from} invitation.')
            
            return redirect('list_invitations')

        else:
            return redirect('permission_denied')
        

class RejectInvitationView(LoginRequiredMixin,View):

    def get(self,request,pk):

        invitation = FriendRequest.objects.get(pk=pk)

        if invitation.sent_to == self.request.user:

            if invitation.status == 1:

                invitation.status = 3
                invitation.save()
                
                messages.warning(self.request,f'You rejected {invitation.sent_from} invitation.')
            
            return redirect('list_invitations')

        else:
            return redirect('permission_denied')


    login_url = "/login/"
    redirect_field_name = "redirect_to"



class RemoveContactView(LoginRequiredMixin,View):

    def get(self,request,pk):

        return render(self.request,'main/confirm_delete.html')

    def post(self,request,pk):

        profile = Profile.objects.get(pk=pk)

        invitation = FriendRequest.objects.filter(Q(sent_from=self.request.user,sent_to=profile.user) | Q(sent_from=profile.user,sent_to=self.request.user))
        invitation.delete()

        request.user.profile.contacts.remove(profile)
        messages.success(self.request,f'You removed {profile.user.username} from your contacts' )
        return redirect('list_contacts')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class CustomPassworchangeView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):

    form_class = ChangePasswordForm
    template_name = 'main/change_password.html'

    def get_success_message(self, cleaned_data):

        return('Your password has been changed')

    def get_success_url(self):
        return reverse('home')
    
    def form_invalid(self,form):

        for error in list(form.errors.values()):
                messages.error(self.request,error) 

        return self.render_to_response(self.get_context_data(form=form))
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"








