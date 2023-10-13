from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=10)
    name = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model): 
    slug = models.CharField(blank=True, null=True, max_length=350)
    title = models.CharField('Title', blank=False, max_length=255)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    tags = TaggableManager(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails')
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.content[:200]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(blank=False, max_length=50)
    email = models.EmailField(max_length=256)
    message = models.TextField(blank=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return 'Comment by {} - {}'.format(self.name, self.pk) 
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    
    


