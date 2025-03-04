from django.db import models
from django.conf import settings
from django.utils.text import slugify



class Article(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, blank=True)
    content = models.TextField(max_length=10000, blank=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_premium = models.BooleanField(
        default=False,
        verbose_name="Is it a premium article?"
    )

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        unique_together = ('slug', 'author')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
