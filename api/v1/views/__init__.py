from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
<<<<<<< HEAD
from api.v1.views.amenities import *
=======
from api.v1.views.cities import *
>>>>>>> 1eff77a237326c6ee2a3a6577e3dc8113e9dea42
