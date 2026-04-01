from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

import models
import routes
routes.register_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.getenv('FLASK_PORT', 8002))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=port)