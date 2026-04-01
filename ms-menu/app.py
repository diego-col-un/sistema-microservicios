from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DB_URL')
})

import routes
routes.register_routes(app)

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 8004))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=port)