from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User

from library.models import Formula, Variable

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = None
        try:
            user = User.objects.create_superuser("root", 'admin@123.ru', 'qwerty')
        except IntegrityError:
            pass
        if not user:
            return
        try:
            Formula.objects.create(
                name="Площадь круга",
                value="S=pi*r^2",
                user_id=user
            )

            Formula.objects.create(
                name="Периметр квадрата",
                value="P=4*a",
                user_id=user
            )

            Formula.objects.create(
                name="Площадь треугольника",
                value="S=\\frac{1}{2}*a*h",
                user_id=user
            )

            Formula.objects.create(
                name="Формула Пифагора",
                value="c^2=a^2+b^2",
                user_id=user
            )

            Formula.objects.create(
                name="Объем куба",
                value="V=a^3",
                user_id=user
            )

            Formula.objects.create(
                name="Объем сферы",
                value="V=\\frac{4}{3}*\\pi*r^3",
                user_id=user
            )

            Formula.objects.create(
                name="Объем цилиндра",
                value="V=\\pi*r^2*h",
                user_id=user
            )

            Formula.objects.create(
                name="Формула для арифметической прогрессии",
                value="a_n=a_1+(n-1)*d",
                user_id=user
            )

            Formula.objects.create(
                name="Сумма первых n натуральных чисел",
                value="S_n=\\frac{n*(n + 1)}{2}",
                user_id=user
            )

            Formula.objects.create(
                name="Квадрат суммы",
                value="(a+b)^2=a^2+2*a*b+b^2",
                user_id=user
            )

            Formula.objects.create(
                name="Формула бинома Ньютона",
                value="(a+b)^n=\\sum_{k=0}^{n}\\binom{n}{k}a^{n-k}*b^k",
                user_id=user
            )

            Formula.objects.create(
                name="Производная функции",
                value="f'(x)=lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}",
                user_id=user
            )

            Formula.objects.create(
                name="Интеграл от функции",
                value="\\int f(x)\\,dx=F(x)+C",
                user_id=user
            )

            Formula.objects.create(
                name="Закон всемирного тяготения",
                value="F=G\\frac{m_1 m_2}{r^2}",
                user_id=user
            )

            Formula.objects.create(
                name="Формула Эйлера",
                value="e^{i\\theta}=\\cos(\\theta)+i*\\sin(\\theta)",
                user_id=user
            )

            Formula.objects.create(
                name="Закон Ома",
                value="I=\\frac{U}{R}",
                user_id=user
            )

            Formula.objects.create(
                name="Формула для объема конуса",
                value="V=\\frac{1}{3}*\\pi*r^2*h",
                user_id=user
            )

            Formula.objects.create(
                name="Скорость равномерного движения",
                value="v=\\frac{s}{t}",
                user_id=user
            )

            Formula.objects.create(
                name="Формула для нахождения угла между векторами",
                value="\\cos(\\theta)=\\frac{A*B}{||A|| ||B||}",
                user_id=user
            )

            Formula.objects.create(
                name="Формула Герона для площади треугольника",
                value="S=\\sqrt{p(p-a)(p-b)(p-c)},\\text{где}p=\\frac{a+b+c}{2}",
                user_id=user
            )
        except Exception as e:
            print(e)
