from datetime import timedelta

from django.core.mail import send_mail


class MenuMixin:
    page_title: str = None
    page_description: str = None

    def get_mixin_context(self, context: dict, **kwargs) -> dict:
        context.update(kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.page_title is not None:
            context['title'] = self.page_title

        if self.page_description is not None:
            context['description'] = self.page_description

        return context


def check_day_dispatch(now_date, start_date, end_date, frequency):
    flag = False

    if now_date < start_date or now_date > end_date:
        return flag

    current_date = start_date

    if frequency == 'daily':
        while current_date <= end_date:
            if current_date == now_date:
                flag = True
                break
            current_date += timedelta(days=1)
    elif frequency == 'weekly':
        while current_date <= end_date:
            if current_date == now_date:
                flag = True
                break
            current_date += timedelta(weeks=1)
    elif frequency == 'monthly':
        while current_date <= end_date:
            if current_date == now_date:
                flag = True
                break

            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)

    return flag


def send_mail_custom(subject, message, from_email, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )
    except Exception as e:
        print(e)
