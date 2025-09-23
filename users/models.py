from django.db import models
from common import BaseModel, PREFECTURES

# class Title(models.TextChoices):
#     MISOKATSU_MASTER = "MisokatsuMaster", "味噌カツマスター"

class Profile(BaseModel): #認証用とは別。1対1。
    display_name = models.CharField(max_length=20)
#   title = models.CharField(max_length=20, choices=Title.choices)
    prefecture = models.CharField(max_length=10, choices=PREFECTURES)
    is_prefecture_public = models.BooleanField(default=False)