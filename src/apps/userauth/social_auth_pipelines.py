from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from social_core.exceptions import AuthException, AuthFailed


def check_social_data(backend, details, *args, **kwargs):
    if backend.name != 'deezer' and not (kwargs.get('email') or details.get('email')):
        raise AuthException(backend, _('Email address is required in order to complete the registration!'))
    return {}


def create_user(strategy, backend, details, response, user=None, *args, **kwargs):
    if backend.name == 'deezer':
        if not user:
            raise AuthFailed(backend, _('You can not create a user using backend {}!'.format(backend.name)))
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
            'is_new': False,
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
    if strategy.storage.user.user_exists(login=fields['login']):
        fields['login'] = strategy.storage.user.objects.generate_login(login=fields['login'], email=fields['login'])
    # todo generate password
    # todo send mail generate password  and email
    user = strategy.create_user(**fields)
    user.save()
    return {
        'is_new': True,
        'user': user
    }


def set_user_first_reg_social_info(backend, response, user, is_new, *args, **kwargs):
    if not user or not is_new:
        return {
            'is_new': is_new,
            'user': user
        }
    if backend.name == 'google-oauth2':
        gp_url = response.get('url')
        if gp_url and gp_url != user.info.google:
            user.info.google = gp_url
            user.info.save()
    elif backend.name == 'facebook':
        fb_url = response.get('url')
        if fb_url and fb_url != user.info.facebook:
            user.info.facebook = fb_url
            user.info.save()
    elif backend.name == 'deezer':
        dz_url = response.get('link')
        if dz_url and dz_url != user.info.deezer:
            user.info.deezer = dz_url
            user.info.save()
    return {}


def set_user_social_info(backend, response, user, is_new, *args, **kwargs):
    if not user or is_new:
        return {}
    if backend.name == 'google-oauth2':
        gp_url = response.get('url')
        if gp_url:
            if gp_url == user.info.google:
                user.info.google = ''
            else:
                user.info.google = gp_url
            user.info.save()
    elif backend.name == 'facebook':
        fb_url = response.get('url')
        if fb_url:
            if fb_url == user.info.facebook:
                user.info.facebook = ''
            else:
                user.info.facebook = fb_url
            user.info.save()
    elif backend.name == 'deezer':
        dz_url = response.get('link')
        if dz_url:
            if dz_url == user.info.deezer:
                user.info.deezer = ''
            else:
                user.info.deezer = dz_url
            user.info.save()
    return {}
