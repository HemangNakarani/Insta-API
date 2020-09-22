import uuid
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/', filename)


def story_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('stories/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(email=self.normalize_email(email),
                          username=username.lower(),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=60, blank=True)
    bio = models.TextField(blank=True)
    url = models.URLField(max_length=200, blank=True)
    profile_pic = models.ImageField(
        upload_to=image_file_path,
        default='avatar.png')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="user_followers",
                                       blank=True,
                                       symmetrical=False)

    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="user_following",
                                       blank=True,
                                       symmetrical=False)

    requests = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name="user_requested",
                                      blank=True,
                                      symmetrical=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0

    def __str__(self):
        return self.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_posts'
    )
    photo = models.ImageField(
        upload_to=image_file_path,
        blank=False,
        editable=False)
    text = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="likers",
                                   blank=True,
                                   symmetrical=False)

    class Meta:
        ordering = ['-posted_on']

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return f'{self.author}\'s post'


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_comments",
                               on_delete=models.CASCADE, )
    post = models.ForeignKey('Post',
                             related_name="post_comments",
                             on_delete=models.CASCADE, )

    text = models.TextField(max_length=50, blank=False)

    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f'{self.author}\'s comment'


class Story(models.Model):

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_story",
                               on_delete=models.CASCADE, )

    posted_on = models.DateTimeField(auto_now_add=True)

    story_image = models.ImageField(upload_to=story_file_path,
                                    default='story.png')

    views = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="story_viewers",
                                   blank=True,
                                   symmetrical=False)

    tagged = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="story_tagged",
                                    blank=True,
                                    symmetrical=False)

    def number_of_views(self):
        if self.views.count():
            return self.views.count()
        else:
            return 0

    def number_of_tags(self):
        if self.tagged.count():
            return self.tagged.count()
        else:
            return 0

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f'{self.author}\'s story'
