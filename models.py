from django.db import models
from django.contrib.auth.models import User


class Kanji(models.Model):
    character = models.CharField(max_length=10)   # 女
    reading = models.CharField(max_length=100)     # おんな
    meaning = models.CharField(max_length=100)    # women
    level = models.CharField(max_length=10) 

    def __str__(self):
        return self.character

class SavedKanji(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.kanji.character}"

class UserKanji(models.Model):
    STATUS_CHOICES = (
        ('known', 'Known'),
        ('unknown', 'Unknown'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.kanji.character}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png'
    )

    def __str__(self):
        return self.user.username