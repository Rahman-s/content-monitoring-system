from django.db import models


# 1. Keyword model
class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# 2. ContentItem model
class ContentItem(models.Model):
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=255)
    body = models.TextField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.title


# 3. Flag model
class Flag(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),
    ]

    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE)

    score = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # suppression logic ke liye important field
    suppressed_at_content_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('keyword', 'content_item')

    def __str__(self):
        return f"{self.keyword.name} -> {self.content_item.title}"