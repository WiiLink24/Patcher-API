import config
from flask import Flask, redirect, render_template, session, url_for
from flask_oidc import OpenIDConnect
from flask_migrate import Migrate
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.secret_key
app.config["OIDC_CLIENT_SECRETS"] = config.oidc_client_secrets_json
app.config["OIDC_SCOPES"] = "openid profile"
app.config["OIDC_OVERWRITE_REDIRECT_URI"] = config.oidc_redirect_uri


db.init_app(app)

migrate = Migrate(app, db)

oidc = OpenIDConnect(app)

with app.app_context():
    # Ensure our database is present.
    db.create_all()

@app.route('/')
def index():
    if oidc.user_loggedin:
        return redirect('/patches')
    else:
        return redirect('/login')
    
@app.route('/login')
def login():
    session.permanent = True
    
    if 'oidc_auth_state' in session:
        del session['oidc_auth_state']
        
    redirect_uri = url_for('oidc_callback', _external=True)
    
    return oidc.redirect_to_auth_server(redirect_uri)

@app.route('/logout')
def logout():
    oidc.logout()
    session.clear()
    return redirect(config.oidc_logout_url)

@app.route('/auth/callback')
def oidc_callback():
    try:
        return redirect('/patches')
    except Exception as e:
        session.clear()
        return render_template('errors/error.html',
                              error_code="Auth",
                              error_title="Authentication Error",
                              error_message="There was a problem with your authentication. Please try again.",
                              error_details=str(e),
                              auto_redirect=True), 400

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/error.html', 
                          error_code=404,
                          error_title="Page Not Found",
                          error_message="The page you're looking for doesn't exist or has been moved.",
                          error_details=str(e)), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/error.html',
                          error_code=500,
                          error_title="Server Error",
                          error_message="Something went wrong on our end. Please contact a developer.",
                          error_details=str(e)), 500

@app.errorhandler(401)
def unauthorized(e):
    return render_template('errors/error.html',
                          error_code=401,
                          error_title="Unauthorized",
                          error_message="You need to be authenticated to access this resource.",
                          error_details=str(e)), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/error.html',
                          error_code=403,
                          error_title="Forbidden",
                          error_message="You don't have permission to access this resource.",
                          error_details=str(e)), 403

@app.errorhandler(Exception)
def handle_exception(e):
    if hasattr(e, 'code') and 400 <= e.code < 600:
        return e
    
    if "MismatchingStateError" in str(e) or "invalid_request" in str(e):
        session.clear()
        return render_template('errors/error.html',
                              error_code="Auth",
                              error_title="Authentication Error",
                              error_message="There was a problem with your authentication session. Please try logging in again.",
                              error_details=str(e),
                              auto_redirect=True), 400
    
    return render_template('errors/error.html',
                          error_code=500,
                          error_title="Server Error",
                          error_message="An unexpected error occurred.",
                          error_details=str(e)), 500

import catalog
import patches