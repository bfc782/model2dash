from dash import dcc, html
import dash_bootstrap_components as dbc
from .ui_layer import tbl_to_layout_comps

def serve_layout(model_components, tbl_cls_cols):
        return html.Div(
                        [
                            html.Div(id='dummy-div', children=[], hidden=True),
                            html.Div(id="alert"),
                            dbc.Tab(

                            )]
                        + 
                        [getattr(model_components, f'{tbl}{comp}')
                            for tbl in tbl_cls_cols for comp in tbl_to_layout_comps[tbl]
                            # for tbl in tbl_cls_cols for comp in ['_btn', '_modal', '_table']
                        ]
                    )