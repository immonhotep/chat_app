from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.contrib.auth.models import User





class Room(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    private = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    participant = models.ManyToManyField(User, related_name="participants" ,blank=True)
    description = models.CharField(max_length=255,null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/rooms")

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Room)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)




class Message(models.Model):

    room = models.ForeignKey(Room,related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    checked = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        
        return f'{self.user}-{self.room}-{self.pk}'

    class Meta:
        
        ordering = ('date_added',)



class ForumCategory(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, blank = True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/forum/category")


    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name_plural = "ForumCategories"


@receiver(pre_save, sender=ForumCategory)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


class ForumMessage(models.Model):

   
    category = models.ForeignKey(ForumCategory,related_name="categories",on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='forum_reply', null=True, blank=True)
    like = models.ManyToManyField(User, related_name="comment_like", blank=True )
    hidden = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_reply(self):
        return ForumMessage.objects.filter(reply=self).reverse()


    def __str__(self):   
        return f'{self.category}-@{self.user.username}-{self.pk}'
    

class ForumMessageReport(models.Model):

    message = models.ForeignKey(ForumMessage,related_name="reported_comment",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reported_by" ,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    report_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f'{self.message}-{self.title}'





class Connected(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="connected")
    room_name = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="connection")
    channel_name = models.CharField(max_length=100, null=True)
    connect_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
   
        
