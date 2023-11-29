from django.db import models

from education.models import Course, Lesson
from users.models import User, NULLABLE


class Payment(models.Model):
    # !!! Закомментирована часть из предыдущих ДЗ, в текущей реализации не предполагается оплата не через stripe !!!
    # PAY_CARD = 'card'
    # PAY_CASH = 'cash'
    #
    # PAY_TYPES = (
    #     (PAY_CASH, 'наличные'),
    #     (PAY_CARD, 'перевод'),
    # )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты', auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Оплаченный курс', **NULLABLE)
    # lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='Оплаченный урок', **NULLABLE)
    # amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    # payment_type = models.CharField(choices=PAY_TYPES, default=PAY_CASH, max_length=10, verbose_name='Cпособ оплаты')
    session_id = models.CharField(max_length=100, verbose_name='id платежной сессии', **NULLABLE)
    is_paid = models.BooleanField(default=False, verbose_name='статус платежа')


    def __str__(self):
        # !!! Изменение в связи с заменой формы оплаты !!!
        return f'({self.user}) - {self.course}'
        # return f'({self.user}) - {self.lesson if self.lesson else self.course} - {self.amount}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
