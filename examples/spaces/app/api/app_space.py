from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from indykite_sdk.config import ConfigClient
from app.config import API_PREFIX
from app.form.app_space import AppSpaceById, AppSpaceCreate
from app.utils.response import get_response, response_data
from app.utils.helper import change_display_to_name
from flask import Flask, render_template, request, url_for, flash, redirect, session

__version__ = "/v1"
__bp__ = "/app_space"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="AppSpace", description="AppSpace")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post("")
def create_app_space(body: AppSpaceCreate):
    client_config = ConfigClient()
    app_space = client_config.create_app_space(body.customer_id,
                                               change_display_to_name(body.display_name),
                                               body.display_name,
                                               body.description,
                                               [])
    if app_space:
        return response_data("AppSpaceCreate", get_response(app_space))
    else:
        return response_data("AppSpaceCreate", "Invalid app_space creation")


@api.get("/<id>")
def get_app_space(path: AppSpaceById):
    client_config = ConfigClient()
    app_space = client_config.get_app_space_by_id(path.id)
    if app_space:
        return response_data("AppSpaceById", get_response(app_space))
    else:
        return response_data("AppSpaceById", "Invalid app_space id")


@api.get("/new")
def new_app_space():
    return render_template('new_app_space.html')


@api.post("/new")
def new_app_space_post():
    session.clear()
    customer_id = request.form['customer_id']
    display_name = request.form['display_name']
    description = request.form['description']

    if not customer_id:
        flash('Customer id is required!')
    elif not display_name:
        flash('Display name is required!')
    elif not description:
        flash('Description is required!')
    else:
        client_config = ConfigClient()
        app_space = client_config.create_app_space(customer_id,
                                                   change_display_to_name(display_name),
                                                   display_name,
                                                   description,
                                                   [])
        if app_space:
            session['app_space'] = get_response(app_space)
            app_space_by_id = client_config.get_app_space_by_id(app_space.id)
            if app_space_by_id:
                session['app_space_by_id'] = get_response(app_space_by_id)
            return render_template('index.html')
        else:
            session['app_space'] = "Invalid app_space creation"
        return render_template('index.html')
    return render_template('new_app_space.html')
