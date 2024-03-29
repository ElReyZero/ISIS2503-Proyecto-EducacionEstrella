import requests 
from social_core.backends.oauth import BaseOAuth2, url_add_parameters
from django.conf import settings as cfg

class Auth0(BaseOAuth2): 
    """Auth0 OAuth authentication backend""" 
    name = 'auth0' 
    SCOPE_SEPARATOR = ' ' 
    ACCESS_TOKEN_METHOD = 'POST' 
    EXTRA_DATA = [ ('picture', 'picture') ]

    def get_redirect_uri(self, state=None):
        """Build redirect with redirect_state parameter."""
        if "localhost" in cfg.LOAD_BALANCER_IP:
            uri = "http://"+cfg.LOAD_BALANCER_IP+"/complete/auth0"
        else:
            uri = "https://"+cfg.LOAD_BALANCER_IP+"/complete/auth0"
        if self.REDIRECT_STATE and state:
            uri = url_add_parameters(uri, {'redirect_state': state})
        return uri

    def authorization_url(self): 
        """Return the authorization endpoint.""" 
        return "https://" + self.setting('DOMAIN') + "/authorize" 
        
    def access_token_url(self): 
        """Return the token endpoint.""" 
        return "https://" + self.setting('DOMAIN') + "/oauth/token" 
    
    def get_user_id(self, details, response): 
        """Return current user id.""" 
        return details['user_id'] 
    
    def get_user_details(self, response): 
        url = 'https://' + self.setting('DOMAIN') + '/userinfo' 
        headers = {'authorization': 'Bearer ' + response['access_token']} 
        resp = requests.get(url, headers=headers) 
        userinfo = resp.json() 
        return {'username': userinfo['nickname'], 'first_name': userinfo['name'], 'picture': userinfo['picture'], 'user_id': userinfo['sub']}

def getRole(request):
    user = request.user 
    auth0user = user.social_auth.get(provider="auth0")
    accessToken = auth0user.extra_data['access_token'] 
    url = "https://isis2503-elreyzero.us.auth0.com/userinfo" 
    headers = {'authorization': 'Bearer ' + accessToken}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()
    role = userinfo['https://isis2503-elreyzero.com/role']
    return (role)