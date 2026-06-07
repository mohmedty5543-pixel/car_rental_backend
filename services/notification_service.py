from core.models import Notification
class NotificationService:
    @staticmethod
    def notify(user, title, body=''):
        return Notification.objects.create(user=user, title=title, body=body)
