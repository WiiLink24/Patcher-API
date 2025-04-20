from app import oidc

def get_user_info():
    # Get all relevant user information at once
    user_info = oidc.user_getinfo([
        'email', 
        'sub', 
        'preferred_username', 
        'picture', 
        'name',
        'groups',
        'given_name',
        'family_name'
    ])
    
    profile_picture = user_info.get('picture')
    
    if not profile_picture and 'avatar' in user_info:
        profile_picture = user_info.get('avatar')
        
    return {
        'username': user_info.get('preferred_username', 
                     user_info.get('name',
                       user_info.get('email', 'User'))),
        'profile_picture': profile_picture,
        'email': user_info.get('email'),
        'full_name': user_info.get('name', ''),
        'first_name': user_info.get('given_name', ''),
        'last_name': user_info.get('family_name', ''),
        'groups': user_info.get('groups', []),
        'is_admin': 'admin' in user_info.get('groups', [])
    }