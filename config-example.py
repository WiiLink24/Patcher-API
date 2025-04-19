db_url = "postgresql://username:password:@localhost/db_name"
secret_key = "please_change_thank_you"

# OpenID Connect configuration
oidc_redirect_uri = "http://localhost:8080/authorize"
oidc_client_secrets_json = {
    "web": {
        "client_id": "",
        "client_secret": "",
        "auth_uri": "",
        "token_uri": "",
        "userinfo_uri": "",
        "issuer": "",
        "redirect_uris": [oidc_redirect_uri],
    }
}
oidc_logout_url = ""
