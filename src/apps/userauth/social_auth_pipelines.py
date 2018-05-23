from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from social_core.exceptions import AuthException


def check_social_data(backend, details, *args, **kwargs):
    if backend.name != 'deezer' and not (kwargs.get('email') or details.get('email')):
        raise AuthException(backend, _('Email address is required in order to complete the registration!'))
    return {}


def create_user(strategy, backend, details, response, user=None, *args, **kwargs):
    if backend.name == 'deezer':
        return {}
    if user:
        return {'is_new': False}
    user_model = get_user_model()
    fields = {
        'login': kwargs.get('username') or details.get('username'),
        'email': kwargs.get('email') or details.get('email'),
        'password': None,
    }
    if strategy.storage.user.user_exists(email=fields['email']):
        return {
            'is_new': True,
            'user': user_model.objects.get(email=fields['email'])
        }
        # raise AuthException(backend, _('A user with this email already exists.'))
    if backend.name in ('google-oauth2', 'facebook'):
        fields['first_name'] = details.get('first_name')
        fields['last_name'] = details.get('last_name')
        gender = response.get('gender')
        if gender == 'male':
            fields['gender'] = user_model.GENDER_MALE
        elif gender == 'female':
            fields['gender'] = user_model.GENDER_FEMALE
    else:
        return
    user = strategy.create_user(**fields)
    user.save()
    return {
        'is_new': True,
        'user': user
    }
