# %%
from dash import Dash, dcc, html, callback, Output, Input, State, \
    no_update, ctx, dash_table
import datetime
import dash_bootstrap_components as dbc
from .extensions import db
from .callbacks import get_component_callbacks, get_col_type
from .components import ModelComponents
from .layout import serve_layout

# %%
def create_dash_app(flask_app, tbl_cls_cols):

    model_components = ModelComponents(db, tbl_cls_cols)
    callbacks = get_component_callbacks(db, tbl_cls_cols)

    dash_app = Dash(__name__,
                    server=flask_app,
                    url_base_pathname='/dash/', 
                    suppress_callback_exceptions=True,
                    external_stylesheets=[dbc.themes.JOURNAL]
            )

    dash_app.layout = serve_layout(model_components, tbl_cls_cols)

    return dash_app
