from django.utils import timezone

from .models import User


def get_count_current_online_users():
    return User.objects.filter(is_online=True).count()


def insert_info_into_log_file(log_file, info):
    logger = open(log_file, 'a')
    log_str = str(timezone.now()) + " : " + info + '\n'
    logger.write(log_str)
    logger.close()
