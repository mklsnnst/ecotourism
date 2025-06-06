from django.db import models
from django.utils import timezone

class Tour(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание")
    price_numeric = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_interval = models.IntegerField(verbose_name="Длительность (дни)")
    start_location = models.CharField(max_length=255, verbose_name="Место начала")
    end_location = models.CharField(max_length=255, verbose_name="Место окончания")
    max_participants = models.IntegerField(verbose_name="Максимум участников")
    available_dates = models.DateField(verbose_name="Дата проведения")
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Кем создан")
    status = models.CharField(max_length=50, verbose_name="Статус", default="Доступен")

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['-available_dates']

    def __str__(self):
        return self.title

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, verbose_name="Тур")
    booking_date = models.DateTimeField(default=timezone.now, verbose_name="Дата бронирования")
    participant_count = models.IntegerField(verbose_name="Количество участников")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая цена")
    status = models.CharField(max_length=50, verbose_name="Статус", default="Ожидает")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-booking_date']

    def __str__(self):
        return f"Бронирование {self.id} для тура {self.tour}"

    def save(self, *args, **kwargs):
        self.total_price = self.tour.price_numeric * self.participant_count
        super().save(*args, **kwargs)

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, verbose_name="Тур")
    review_text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(verbose_name="Рейтинг")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_date']

    def __str__(self):
        return f"Отзыв {self.id} для тура {self.tour}"

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, verbose_name="Тур")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        ordering = ['user']

    def __str__(self):
        return f"Избранное {self.id} пользователя {self.user}"

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.CharField(max_length=255, verbose_name="Электронная почта")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    role = models.CharField(max_length=50, verbose_name="Роль", default="Гость")
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['-registration_date']

    def __str__(self):
        return self.name

class TourUser(models.Model):
    id = models.AutoField(primary_key=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, verbose_name="Тур")
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    role = models.CharField(max_length=50, verbose_name="Роль", default="Участник")

    class Meta:
        verbose_name = "Участник тура"
        verbose_name_plural = "Участники туров"
        ordering = ['tour']

    def __str__(self):
        return f"Тур {self.tour} - Пользователь {self.user}"