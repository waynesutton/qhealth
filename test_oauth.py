#!/usr/bin/env python

from rauth import OAuth2Service, OAuth2Session
from rauth.utils import parse_utf8_qsl
import json

redirect_uri = 'http://localhost:5000/humanapi/callback'

service  = OAuth2Service(
    client_id='9ecad85680972ea571a3af89f267d248526834d2',
    client_secret='9b49f4368f8aab29536ab0c528921ae4382ac74f',
    name='humanapi',
    authorize_url='https://user.humanapi.co/oauth/authorize',
    access_token_url='https://user.humanapi.co/oauth/token',
    base_url='https://api.humanapi.co/v1/human/')


authorize_url = service.get_authorize_url(
    response_type='code',
    redirect_uri=redirect_uri,
)
print 'Authorize URL: ' + authorize_url

# Send user to authorize_url and retrieve code (hardcoded next instead)

code = 'k0zSNiAfW8AQmICwfd1x1N'
print 'Using authorize code %s to request OAuth session' % code

# retrieve the authenticated session (response is a JSON string, so we need a custom decoder)
session = service.get_auth_session(data={
    'scope': 'profile',
    'code': code,
}, decoder=json.loads)
print 'Got OAuth2 session with access token:', session.access_token

# make a request using the authenticated session
profile = session.get('profile').json()

print 'profile:', profile

