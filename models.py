from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Новое поле для лайков/просмотров
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title