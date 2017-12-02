from ..models import UserNotification

def get_user_notifications(user):
    notifications = UserNotification.objects.filter(user=user)
    result = [notification.content_object for notification in notifications]
    return result