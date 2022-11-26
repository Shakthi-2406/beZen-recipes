from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Recipe(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True)
    prept = models.IntegerField(null = True, blank=True, default=10)
    cookt = models.IntegerField(null = True, blank=True, default=20)
    totalt = models.IntegerField(null = True, blank=True)
    servings = models.IntegerField(null = True, blank=True, default=2)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipes')
    cover = models.ImageField(default='Recipe.jpg', upload_to='recipe_covers/')
    is_veg = models.BooleanField(default=False, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=300)
    steps = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    ingredients = models.TextField(blank=False, null=False)
    liked = models.ManyToManyField(User, blank=True, related_name='favorites')

    def __str__(self):
        return f"{self.name} by {self.author}"

    @property
    def liked_count(self):
        return self.liked.all().count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.totalt = int(self.prept) + int(self.cookt)
        super(Recipe, self).save(*args, **kwargs)
