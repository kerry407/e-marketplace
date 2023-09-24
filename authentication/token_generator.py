try:
    from secrets import SystemRandom
except ImportError:
    from random import SystemRandom


UNICODE_ASCII_CHARACTER_SET = (
    'abcdefghijklmnopqrstuvwxyz' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' '0123456789'
)


def token_generator(request, length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    """Generates a non-guessable OAuth Json Web Token
    OAuth (1 and 2) does not specify the format of tokens except that they
    should be strings of random characters. Tokens should not be guessable
    and entropy when generating the random characters is important. Which is
    why SystemRandom is used instead of the default random.choice method.
    """
    from django.conf import settings
    from jose import jwt
    from datetime import datetime, timedelta
    import calendar

    rand = SystemRandom()
    secret = getattr(settings, 'SECRET_KEY')
    token = ''.join(rand.choice(chars) for _ in range(length))

    expires_in = getattr(settings, 'OAUTH2_PROVIDER')['ACCESS_TOKEN_EXPIRE_SECONDS']
    exp = calendar.timegm((datetime.utcnow() + timedelta(seconds=expires_in)).utctimetuple())
    
    jwtted_token = jwt.encode({'token': token, 'exp': exp}, secret, algorithm='HS256')
    return jwtted_token
    