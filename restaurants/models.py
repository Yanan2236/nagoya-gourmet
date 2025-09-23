from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from common import BaseModel, PREFECTURES


class Category(models.TextChoices):
    MISOKATSU = "MISOKATSU", "味噌カツ"
    HITSUMABUSHI = "HITSUMABUSHI", "ひつまぶし"
    KISHIMEN = "KISHIMEN", "きしめん"
    MISONIKOMIUDON = "MISONIKOMIUDON", "味噌煮込みうどん"
    OGURATOAST = "OGURATOAST", "小倉トースト"
    TEBASAKI = "TEBASAKI", "手羽先"
    TAIWAN_RAMEN = "TAIWAN_RAMEN", "台湾ラーメン"

class City(models.TextChoices):
    NAGOYA = "NAGOYA", "名古屋市"

class NagoyaWard(models.TextChoices):
    CHIKUSA = "CHIKUSA", "千種区"
    HIGASHI = "HIGASHI", "東区"
    KITA = "KITA", "北区"
    NISHI = "NISHI", "西区"
    NAKAMURA = "NAKAMURA", "中村区"
    NAKA = "NAKA", "中区"
    SHOWA = "SHOWA", "昭和区"
    MIZUHO = "MIZUHO", "瑞穂区"
    ATSUTA = "ATSUTA", "熱田区"
    NAKAGAWA = "NAKAGAWA", "中川区"
    MINATO = "MINATO", "港区"
    MINAMI = "MINAMI", "南区"
    MORIYAMA = "MORIYAMA", "守山区"
    MIDORI = "MIDORI", "緑区"
    MEITO = "MEITO", "名東区"
    TEMPAKU = "TEMPAKU", "天白区"

class PriceRange(models.TextChoices):
    UNDER_ONE = "-1000", "～¥1,000"
    ONE_TO_TWO = "1000-2000", "¥1,000～¥2,000"
    TWO_TO_THREE = "2000-3000", "¥2,000～¥3,000"
    THREE_TO_FIVE = "3000-4999", "¥3,000～¥4,999"
    FIVE_TO_TEN = "5000-9999", "¥5,000～¥9,999"
    OVER_TEN = "10000-", "¥10,000～"

class Rank(models.IntegerChoices):
    ONE = 1, "★☆☆☆☆"
    TWO = 2, "★★☆☆☆"
    THREE = 3, "★★★☆☆"
    FOUR = 4, "★★★★☆"
    FIVE = 5, "★★★★★"

class Weekday(models.IntegerChoices):
    MONDAY = 0, "月"
    TUESDAY = 1, "火"
    WEDNESDAY = 2, "水"
    THURSDAY = 3, "木"
    FRIDAY = 4, "金"
    SATURDAY = 5, "土"
    SUNDAY = 6, "日"

class Tag(models.Model): 
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=50)
    def __str__(self): return self.label

class Restaurant(BaseModel):
    name = models.CharField(max_length=100)

    prefecture = models.CharField(max_length=10, choices=PREFECTURES, default="aichi")
    city = models.CharField(max_length=20, choices=City.choices, default=City.NAGOYA)
    ward = models.CharField(max_length=20, choices=NagoyaWard, null=True, blank=True)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    phone_number = models.CharField(max_length=20)

    category = models.CharField(max_length=20, choices=Category.choices)
    short_feature = models.CharField(max_length=255, blank=True)
    long_feature = models.TextField(blank=True)
    #tags = models.ManyToManyField(Tag, blank=True, related_name="restaurants")

    price_range = models.CharField(max_length=10, choices=PriceRange.choices)

    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name

    class Meta:
        indexes = [
            models.Index(fields=["category", "city"]),
            models.Index(fields=["city", "price_range"]),
            ]
        constraints = [
            models.CheckConstraint(
                name="ward_required_when_nagoya",
                check=(
                    ~Q(city="NAGOYA") 
                    | (Q(city="NAGOYA") & Q(ward__isnull=False) & ~Q(ward=""))
                ),
            ),
        ]
    
class OpeningWindow(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="opening_windows")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        qs = OpeningWindow.objects.filter(
            restaurant=self.restaurant, weekday=self.weekday
        ).exclude(pk=self.pk)
        for w in qs:
            if not (self.end_time <= w.start_time or self.start_time >= w.end_time):
                raise ValidationError("営業時間が重複しています。")

class Review(BaseModel):
    #user = models.ForeignKey() <-User作ったら実装
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=Rank.choices)
    text = models.TextField()
    #tags = models.ManyToManyField(Tag, blank=True, related_name="reviews")

