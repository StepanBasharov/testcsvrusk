import io

from rest_framework.views import APIView
from .models import User, Rock, Trade
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.db.models import Count
from .serializers import UploadDetailsSerializer
import csv


def create_user(csv_file):
    """Функция создания нового объекта пользователя"""

    # Список в который будут добавлены пользователи для создания
    users_to_create = []
    # Пользователи которые уже были добавлены в список
    already_created = []
    # Чтение данных из cvs файла
    reader = csv.reader(io.StringIO(csv_file))
    # Переход с перовй строки (customer, item, total, etc...)
    next(reader)
    # Проход циклом по всем строкам файла
    for row in reader:
        # Получение имени пользователя
        nickname = row[0]
        try:
            # Проверка на наличие пользователя в базе данных
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            # Проверка был ли уже добавлен этот пользователь
            if nickname in already_created:
                pass
            else:
                # Создание объекта пользователя и внесение его в список
                user = User(nickname=nickname, total_spent=0)
                users_to_create.append(user)
                already_created.append(nickname)
    # Добавление пользователей в БД
    User.objects.bulk_create(users_to_create)


def create_trade(csv_file):
    trade_to_create = []
    # Чтение csv файла
    reader = csv.reader(io.StringIO(csv_file))
    # Переход с перовй строки (customer, item, total, etc...)
    next(reader)
    for row in reader:
        # Создание объекта транзакции
        nickname = User.objects.get(nickname=row[0])
        rock_name = Rock.objects.get(rock_name=row[1])
        total = float(row[2])
        quantity = int(row[3])
        date = row[4]

        new_trade = Trade(user=nickname, rock_item=rock_name, total=total, quantity=quantity, date=date)
        # Добавление в список для создания
        trade_to_create.append(new_trade)
    # Добавление транзакций в БД
    Trade.objects.bulk_create(trade_to_create)


def create_rocks(csv_file):
    """Функция создания нового объекта камня"""

    # Список в который будут добавлены камни для создания
    rocks_to_create = []
    # Камни которые уже были добавлены в список
    already_created = []
    # Чтение csv файла
    reader = csv.reader(io.StringIO(csv_file))
    # Переход с перовй строки (customer, item, total, etc...)
    next(reader)
    # Проход циклом по всем строкам файла
    for row in reader:
        # Получение названия камня
        rock_name = row[1]
        try:
            # Проверка на сущетвование камня в БД
            rock = Rock.objects.get(rock_name=rock_name)
        except Rock.DoesNotExist:
            # Проверка был ли уже добавлен этот пользователь
            if rock_name in already_created:
                pass
            else:
                # Создание камня пользователя и внесение его в список
                rock = Rock(rock_name=rock_name)
                rocks_to_create.append(rock)
                already_created.append(rock_name)
    # Добавление камня в БД
    Rock.objects.bulk_create(rocks_to_create)


def calk_total_spent(csv_file):
    """Функция подсчета и обновления общей суммы трат"""

    # Чтение csv файла
    reader = csv.reader(io.StringIO(csv_file))
    # Переход с перовй строки (customer, item, total, etc...)
    next(reader)
    # Список с пользователями для обновления total_spent
    user_to_update = []
    # Словарь для хранения никнеймов и общей суммы трат
    users = {}
    # Проход циклом по всем строкам файла
    for row in reader:
        # Получение никнейма
        nickname = row[0]
        # Получение суммы за операцию
        total_spent = float(row[2])
        # Если пользователь уже есть в словаре мы прибавляем сумму транзакции к общей сумме
        if nickname in users:
            users[nickname] += total_spent
        # Если пользователя нет в словаре мы создаем его и присваиваем ему сумму транзакции
        else:
            users[nickname] = total_spent
    # Проход циклом по всем пользователям в словаре
    for user in users:
        # Получаем пользователя по никнейму и устанавливаем total_spent
        update_user = User.objects.get(nickname=user)
        update_user.total_spent += users[user]
        user_to_update.append(update_user)
    # Вносим изменения в базу
    User.objects.bulk_update(user_to_update, fields=['total_spent'])


class TradeView(APIView):
    """Контроллер возвращает 5 пользователей потративших максимальную сумму, количество потраченых денег и камни
    которые были куплены как минимум 2 пользователями из списка"""
    renderer_classes = [JSONRenderer]

    def get(self, request):
            # Список в который будет передан результат
            result = []
            # Получаем 5 пользователей с самыми большими тратами
            top_users = User.objects.order_by('-total_spent')[:5]
            # Фильтрация и анотация камней
            rocks = Rock.objects.filter(trade__user__in=top_users).annotate(num_buyers=Count('trade__user')).filter(
                num_buyers__gt=1)
            # Создание словаря с пользователями и их камнями
            user_rocks = {}
            for user in top_users:
                user_rocks[user] = [rock.rock_name for rock in rocks.filter(trade__user=user)]
            # Приведение данных к правильному формату
            for i in user_rocks:
                result.append({
                    "username": i.nickname,
                    "spent_money": i.total_spent,
                    "gems": user_rocks[i]
                })
            return Response(result)


class UploadDetailsView(APIView):
    """Контроллер считывает данные из csv и вносит их в базу данных"""

    def post(self, request):
        Trade.objects.all().delete()
        User.objects.all().delete()
        Rock.objects.all().delete()
        # Подключение сериализатора
        serializer = UploadDetailsSerializer(data=request.data)
        if serializer.is_valid():
            # Получение csv файла
            csv_file = serializer.validated_data['csv_file']
            # Чтение и деодирование файла
            decoded_file = csv_file.read().decode('utf-8')
            try:
                # Функция создания пользоватлей
                create_user(decoded_file)
                # Функция создания камней
                create_rocks(decoded_file)
                # Функция расчета трат
                calk_total_spent(decoded_file)
                # Функция для создания транзакций
                create_trade(decoded_file)

                return Response("OK", status=200)
            except Exception as error:
                return  Response(f"ERROR: {error}", status=500)
        return Response(f"ERROR: {serializer.errors}", status=400)