from dash import dcc, html
import dash_bootstrap_components as dbc
from .ui_layer import tbl_to_layout_comps

def serve_layout(model_components, tbl_cls_cols):
        return html.Div(
                        [
                            html.Div([
                                    dcc.Location(id='url', refresh=False),
                                    html.Div(id='dummy-div', children=[], hidden=True)
                            ]),
                            html.Div(id="alert"),
                            dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            html.Div(children=[
                                                    getattr(model_components, f'{tbl}{comp}')
                                                    for comp in tbl_to_layout_comps[tbl]
                                                    ], id=f"{tbl}"),
                                            label=f'{tbl}',
                                        )
                                        for tbl in tbl_cls_cols
                                    ]
                                    
                            )
                        ]
                    )