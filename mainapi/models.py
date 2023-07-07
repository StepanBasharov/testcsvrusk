from django.db import models


class User(models.Model):
    nickname = models.CharField("Имя пользователя", max_length=30)
    total_spent = models.FloatField("Траты за все время", null=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Rock(models.Model):
    rock_name = models.CharField("Название камня", max_length=30)

    def __str__(self):
        return self.rock_name

    class Meta:
        verbose_name = "Камень"
        verbose_name_plural = "Камни"


class Trade(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="trades")
    rock_item = models.ForeignKey(Rock, verbose_name="Купленый камень", on_delete=models.CASCADE)
    total = models.FloatField("Сумма сделки")
    quantity = models.IntegerField("Количество товара")
    date = models.DateTimeField("Дата и время совершения сделки")

    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
