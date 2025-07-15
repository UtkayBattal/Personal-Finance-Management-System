import os
from app import create_app, db
from flask_migrate import Migrate
from flask import Flask

app = Flask(__name__, static_url_path='/static')
app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Çevresel değişkenlerden debug modunu belirle
    debug_mode = True  
    app.run(debug=debug_mode)
