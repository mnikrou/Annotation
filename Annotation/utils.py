from django.contrib.auth.models import User, Group
from django.db.models import Q

def is_expert_user(user):
    return user.groups.filter(name='EXPERT_USERS').exists()

def is_crowd_user(user):
    return user.groups.filter(Q(name='TRAINED_POWER_USERS') | Q(name='UNTRAINED_POWER_USERS')).exists()