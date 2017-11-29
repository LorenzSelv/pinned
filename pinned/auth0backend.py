from six.moves.urllib import request
from jose import jwt
from social_core.backends.oauth import BaseOAuth2


class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'

    def authorization_url(self):
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        idToken = response.get('id_token')
        jwks = request.urlopen("https://" + self.setting('DOMAIN') + "/.well-known/jwks.json")
        issuer = "https://" + self.setting('DOMAIN') + "/"
        audience = self.setting('KEY')  # CLIENT_ID
        data = jwks.read().decode('utf-8')
        payload = jwt.decode(idToken, data, algorithms=['RS256'], audience=audience, issuer=issuer)

        # Get provider and user id on the provider
        pipe_index = payload['sub'].find('|')
        provider = payload['sub'][:pipe_index]
        provider_id = payload['sub'][pipe_index+1:]

        user_data = {'username': payload['nickname'],
                     'first_name': payload['name'],
                     'user_id': payload['sub'],
                     'picture': payload['picture'],
                     'provider': provider,
                     'provider_id': provider_id}
        
        return user_data
