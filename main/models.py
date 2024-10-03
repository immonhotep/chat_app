from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default="images/default_user.jpg",upload_to="images/profiles",blank=True, null=True)
    bio = models.TextField(max_length=500,blank=True, null=True)
    contacts = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self):

        return f'{self.user.username}'
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    


class FriendRequest(models.Model):

    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )
     
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    sent_from = models.ForeignKey(User, related_name="requests_sent", on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name="requests_received", on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.sent_from}-to-{self.sent_to}'
