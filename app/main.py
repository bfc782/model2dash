# %%
from dash import Dash, dcc, html, callback, Output, Input, State, \
    no_update, ctx, dash_table
import datetime
import dash_bootstrap_components as dbc
from .extensions import db
from .callbacks import get_component_callbacks, get_col_type
from .components import ModelComponents

# %%
def create_dash_app(flask_app, tbl_cls_cols):
    model_components = ModelComponents(db, tbl_cls_cols)
    # callbacks = model_components.get_component_callbacks()
    callbacks = get_component_callbacks(db, tbl_cls_cols)

    dash_app = Dash(__name__,
                    server=flask_app,
                    # url_base_pathname='/dash/', 
                    suppress_callback_exceptions=True,
                    external_stylesheets=[dbc.themes.JOURNAL]
            )

    def serve_layout():
        return html.Div(
                        [
                            html.Div(id='dummy-div', children=[], hidden=True),
                            html.Div(id="alert"),
                            dbc.Tab(

                            )]
                        + 
                        [getattr(model_components, f'{tbl}{comp}')
                            for tbl in tbl_cls_cols for comp in ['_btn', '_modal', '_table']
                        ]
                    ) 

    dash_app.layout = serve_layout

    return dash_app
