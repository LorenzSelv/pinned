def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = details['picture']
    
    # If user is authenticated with facebook get the larger version of his picture
    if details['provider'] == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % details['provider_id']

    user.picture = url
    user.save()
