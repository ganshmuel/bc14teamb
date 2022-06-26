from weightApp import weightApp, requests, get_weight, post_weight, get_unknown, GETitem, GEThealth, GETsession, POSTbatch_weight
from flask import request, render_template
from . import weightApp
from .post_weight import post_weight
from .get_weight import get_weight
from .get_item import get_item
from .get_health import get_health
from .get_unknown import unknown_containers
from .GETsession import GETsession
from .db_module import DB_Module
from .POSTbatch_weight import POSTbatch_weight



@weightApp.route('/health')
def get_health():
    return Response("OK", status=200, mimetype="text")
