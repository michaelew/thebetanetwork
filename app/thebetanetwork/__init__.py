from flask import Flask

app = Flask(__name__)

app.secret_key = 'OSAdfhse89ugasognEWt09)e90guug'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = ".@gmail.com"
app.config["MAIL_PASSWORD"] = "."


from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:.@localhost/development'

from models import db
db.init_app(app)

import thebetanetwork.routes
