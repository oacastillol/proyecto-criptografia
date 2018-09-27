from flask import Flask

from .config import app_config
from .models import db, bcrypt
from .controllers.UserController import user_api as user_blueprint
from .controllers.MessageController import message_api as message_blueprint
from .controllers.CipherController import cipher_api as cipher_blueprint
def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])
  bcrypt.init_app(app)
  db.init_app(app)

  app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(message_blueprint, url_prefix='/api/v1/messages')
  app.register_blueprint(cipher_blueprint, url_prefix='/api/v1/cipher') 
  
  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'

  return app
