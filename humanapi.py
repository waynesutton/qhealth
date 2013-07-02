from rauth import OAuth2Service
import json

redirect_uri = 'http://localhost:5000/humanapi/callback'

HumanAPI = OAuth2Service(
    client_id='9ecad85680972ea571a3af89f267d248526834d2',
    client_secret='9b49f4368f8aab29536ab0c528921ae4382ac74f',
    name='humanapi',
    authorize_url='https://user.humanapi.co/oauth/authorize',
    access_token_url='https://user.humanapi.co/oauth/token',
    base_url='https://api.humanapi.co/v1/human/')


# Wrapper functions for building authorize URL and session easily
def get_authorize_url(redirect_uri):
    return HumanAPI.get_authorize_url(
        response_type='code',
        redirect_uri=redirect_uri,
    )

def get_auth_session(code, scope='profile'):
    # retrieve the authenticated session (response is a JSON string, so we need a custom decoder)
    session = HumanAPI.get_auth_session(data={
        'scope': scope,
        'code': code,
    }, decoder=json.loads)

    return session

def recreate_session(access_token):
    return OAuth2Session(
        HumanAPI.client_id,
        HumanAPI.client_secret,
        access_token,
        HumanAPI
    )
