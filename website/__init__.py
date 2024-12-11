from flask import Flask  # type: ignore

def create_app():

    app = Flask(__name__)
    # app.config['SUPABASE_URL'] = "https://zjpwitgacrwipwlwztsp.supabase.co"
    # app.config['SUPABASE_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpqcHdpdGdhY3J3aXB3bHd6dHNwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE0MzMyMDQsImV4cCI6MjA0NzAwOTIwNH0.Fk1DQa8vF1qsqEd_5_Cmr1S1tpDc5cmpz8B3FG8Aqc0"
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    from website.views.view import views
    from website.views.auth import auth

    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')
    
    return app