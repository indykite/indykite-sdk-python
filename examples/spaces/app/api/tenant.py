from flask_openapi3 import APIBlueprint
from flask_openapi3 import Tag
from indykite_sdk.config import ConfigClient
from app.config import API_PREFIX
from app.form.tenant import TenantById, TenantCreate
from app.utils.response import get_response, response_data
from app.utils.helper import change_display_to_name
from flask import Flask, render_template, request, url_for, flash, redirect, session

__version__ = "/v1"
__bp__ = "/tenant"
url_prefix = API_PREFIX + __version__ + __bp__
tag = Tag(name="Tenant", description="Tenant")
api = APIBlueprint(__bp__, __name__, url_prefix=url_prefix, abp_tags=[tag])


@api.post("")
def create_tenant(body: TenantCreate):
    print(body.display_name)

    client_config = ConfigClient()
    tenant = client_config.create_tenant(body.issuer_id,
                                         change_display_to_name(body.display_name),
                                         body.display_name,
                                         body.description, [])
    if tenant:
        return response_data("TenantCreate", get_response(tenant))
    else:
        return response_data("TenantCreate", "Invalid tenant creation")


@api.get("/<id>")
def get_tenant(path: TenantById):
    client_config = ConfigClient()
    tenant = client_config.get_tenant_by_id(path.id)
    if tenant:
        return response_data("TenantById", get_response(tenant))
    else:
        return response_data("TenantById", "Invalid tenant id")


@api.get("/new")
def new_tenant():
    return render_template('new_tenant.html')


@api.post("/new")
def new_tenant_post():
    issuer_id = request.form['issuer_id']
    display_name = request.form['display_name']
    description = request.form['description']

    if not issuer_id:
        flash('Issuer id is required!')
    elif not display_name:
        flash('Display name is required!')
    elif not description:
        flash('Description is required!')
    else:
        client_config = ConfigClient()
        tenant = client_config.create_tenant(issuer_id,
                                             change_display_to_name(display_name),
                                             display_name,
                                             description,
                                             [])
        if tenant:
            session['tenant'] = get_response(tenant)
            tenant_by_id = client_config.get_tenant_by_id(tenant.id)
            if tenant_by_id:
                session['tenant_by_id'] = get_response(tenant_by_id)
            return render_template('index.html')
        else:
            session['tenant'] = "Invalid tenant creation"
        return render_template('index.html')
    return render_template('new_tenant.html')
