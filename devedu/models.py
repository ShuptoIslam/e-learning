from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import User

from django.utils.text import slugify

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(blank=True, max_length=200)
    last_name = models.CharField(blank=True, max_length=200)
    profile_pic = models.ImageField(upload_to="profilePics", blank=True)
    about = models.TextField(validators=[MaxLengthValidator(2000)], blank=True)
    linkedin = models.URLField(blank=True, max_length=1000)
    github = models.URLField(blank=True, max_length=1000)
    mail = models.URLField(blank=True, max_length=1000)
    website = models.URLField(blank=True, max_length=1000)
    is_instructor = models.BooleanField(default=False, blank=True)
    applied = models.BooleanField(default=False, blank=True)
    resume = models.FileField(blank=True, null=True)

    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"{self.user.username}"

    def __str__(self):
        return self.full_name()


class Instructor(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, blank=True, related_name="user_profile"
    )

    def __str__(self):
        return self.user.full_name()


class Course(models.Model):
    title = models.CharField(unique=True, max_length=150, null=True)
    author = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, null=True, related_name="courses")
    description = models.TextField(validators=[MaxLengthValidator(3000)])
    thumb_nail = models.ImageField(upload_to="thumb_nails", null=True)
    created_on = models.DateField(auto_now=True)
    last_updated_on = models.DateField(auto_now=True)
    price = models.FloatField()
    slug = models.SlugField(blank=True, unique=True, null=True)
    enrolled_students = models.ManyToManyField(
        UserProfile, blank=True, related_name="courses")

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate the slug only if it's not set yet
            self.slug = slugify(str(self.title))
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.author}"


class CourseContent(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, related_name="contents")
    serial = models.IntegerField(null=True)
    title = models.CharField(max_length=150, null=True)
    file = models.FileField(null=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} {self.title}"
