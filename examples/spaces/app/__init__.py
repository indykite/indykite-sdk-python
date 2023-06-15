import traceback
from flask import redirect, url_for, render_template, session
from flask_openapi3 import HTTPBearer, HTTPBase
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from werkzeug.exceptions import HTTPException


def init_exception(app: OpenAPI):
    from app.utils.exceptions import BaseAPIException

    @app.errorhandler(Exception)
    def handler(e):
        if isinstance(e, HTTPException):
            code = e.code
            message = e.description
            return BaseAPIException(code, message)
        else:
            print(traceback.format_exc())
            return e


def register_apis(app: OpenAPI):
    from app.api.app_space import api as app_space_api
    from app.api.tenant import api as tenant_api
    from app.api.app_with_agent_credentials import api as app_with_agent_credentials_api
    app.register_api(app_space_api)
    app.register_api(tenant_api)
    app.register_api(app_with_agent_credentials_api)


def create_app():
    from . import config
    app = OpenAPI(
        __name__,
        info=Info(title=config.APP_NAME, version=config.APP_VERSION),
        security_schemes={
            "basic": HTTPBase(),
            "jwt": HTTPBearer(bearerFormat="JWT")
        },
        doc_expansion="none",
    )

    app.json.ensure_ascii = False
    app.config.from_object(config)
    init_exception(app)
    register_apis(app)
    return app


app = create_app()
app.config['SECRET_KEY'] = 'aaaaaaaaaaaaaaaaaaaa' # for flash session to work


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/kill")
def kill():
    session.clear()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


