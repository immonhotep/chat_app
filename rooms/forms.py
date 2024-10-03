from django import forms

from .models import ForumMessage,ForumMessageReport,ForumCategory,Room


class EditForumMessageForm(forms.ModelForm):
     
    class Meta:
        model = ForumMessage
        fields = ('message',)

    
    message = forms.CharField(widget=forms.Textarea(attrs={

        'placeholder':'Your comment',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]', 


    }))


class ReportMessageForm(forms.ModelForm):

    class  Meta:
        
        model = ForumMessageReport
        fields =('title','detail')

    
    


    title_choices=[
        ('Rude Talk','Rude talk'),
        ('Insulting','Insulting'),
        ('Offensive comment','Offensive comment'),
        ('Other','Other'),
    ]



    title = forms.ChoiceField(
        
        choices=title_choices,
        widget=forms.Select(attrs={
         
            'class':'bg-red-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
             
        })


    )


    detail = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Detail',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]',


    }))




class CreateForumCategoryForm(forms.ModelForm):

    class Meta:

        model = ForumCategory
        fields=('name','description','image')

    
    name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Forum Name',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]',


    })) 


    description = forms.CharField(widget=forms.Textarea(attrs={

        'placeholder':'Description',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]', 


    }))   

    image = forms.ImageField(required=True)


      

class RoomCreateForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('name','description','image')


    name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Chatroom Name',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]',


    })) 


    description = forms.CharField(widget=forms.Textarea(attrs={

        'placeholder':'Description',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]', 


    }))   

    image = forms.ImageField(required=True)

