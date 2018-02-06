from django.contrib.auth.models import User, Group

def is_expert_user(user):
    return user.groups.filter(name='EXPERT_USERS').exists()