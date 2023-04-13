from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
<<<<<<< HEAD
from api.v1.views.places import *
=======
from api.v1.views.users import *
>>>>>>> 43077fb158b2be162999c8fab983b9fbd877e591
