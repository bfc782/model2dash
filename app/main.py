# %%
from dash import Dash, dcc, html, callback, Output, Input, State, \
    no_update, ctx, dash_table
import datetime
import dash_bootstrap_components as dbc
from data import *

# %%
def result_to_dict_list_with_headers(query_result):
    """
    Converts a list of SQLAlchemy ORM instances to a list of dictionaries
    and extracts the column headers.

    Args:
        query_result (list): A list of SQLAlchemy ORM instances.

    Returns:
        tuple: A tuple containing a list of column headers and a list of dictionaries,
               where each dictionary represents a row in the table.
    """
    if not query_result:
        return [], []  # Return empty lists if the query result is empty

    # Extract column headers from the first row's table
    column_headers = [column.name for column in query_result[0].__table__.columns]

    # Convert each row into a dictionary
    rows = [{column: getattr(row, column) for column in column_headers} for row in query_result]
    # print(rows)
    dash_table_columns = [{'name': c, 'id': c} for c in column_headers]

    return dash_table_columns, rows

def fetch_data(session, tbl):
    res = session.query(tbl_cls_cols[tbl]['object']).all()
    _, data = result_to_dict_list_with_headers(res)
    return data


# %%
def get_col_type(tbl, col):
    table = Base.metadata.tables[tbl]
    column = table.columns[col]
    return str(column.type)

def get_input_component(tbl, col):
    col_type = get_col_type(tbl, col)
    if col_type == 'INTEGER':
        return dbc.Input(placeholder=f'enter {col}', id=f"{tbl}-{col}-input")
    elif col_type == 'DATE':
        return dcc.DatePickerSingle(
            id=f"{tbl}-{col}-input",
            min_date_allowed=datetime.date.today() - datetime.timedelta(days=2),
            max_date_allowed=datetime.date.today(),
            initial_visible_month=datetime.date.today(),
            date=datetime.date.today()
        )
    else:
        return dbc.Input(placeholder=f'enter {col}', id=f"{tbl}-{col}-input")

def make_form(tbl, cols):
    form = dbc.Form(
        [dbc.Row(
            [
                dbc.Label(col, width="auto"),
                dbc.Col(
                    get_input_component(tbl, col)
                )
            ]
        ) for ix, col in enumerate(cols)] +
        [dbc.Row([dbc.Button(f"Submit {tbl}", id=f"{tbl}-submit-btn")])]   
    )
    return form

def create_table_callback(tbl_name):
    @callback(
        Output(f'{tbl_name}-table', 'data'),
        Input('dummy-div', 'children')
    )
    def get_data(_):
        return fetch_data(session, tbl_name)

class ModelComponents:
    # component_dict = {}
    def __init__(self, model_tbl):
        self.model_tbl = model_tbl

        for ix, tbl in enumerate(model_tbl):
            setattr(self, f'{tbl}_btn', dbc.Button(tbl, id=f'{tbl}-btn'))
            setattr(self, f'{tbl}_modal', dbc.Modal(make_form(tbl, tbl_cls_cols[tbl]['cols']), 
                                                            id=f'{tbl}-modal'))
            setattr(self, f'{tbl}_table', dash_table.DataTable(
                id=f'{tbl}-table',
                columns=[{'id':c, 'name':c} for c in tbl_cls_cols[tbl]['cols']],
            ))

    def get_component_callbacks(self):
        for tbl in self.model_tbl:
            @callback(
                Output(f'{tbl}-modal', 'is_open'),
                Input(f'{tbl}-btn', 'n_clicks')
            )
            def show_modal(n1):
                if n1:
                    return True
                return False
            
            @callback(
                Output("alert", "children", allow_duplicate=True),
                Output('dummy-div', 'children', allow_duplicate=True),
                Input(f"{tbl}-submit-btn", "n_clicks"),
                [[State(f'{tbl}-{col}-input', "value") if get_col_type(tbl, col) != 'DATE' \
                   else State(f'{tbl}-{col}-input', "date") \
                  for col in tbl_cls_cols[tbl]['cols']]],
                prevent_initial_call=True
            )
            def submit_inputs(n1, inputs):
                '''
                Send inputs to database:
                - db is updated return success alert, table
                - db inputs are invalid return exception to alert
                - db server is unavailable return exception to alert
                - 
                '''

                inputs_txt = ", ".join([i if i else "" "" for i in inputs])
                btn = ctx.triggered_id
                if any(inputs):
                    for ix, _ in enumerate(inputs):
                        try:
                            inputs[ix] = datetime.date.fromisoformat(inputs[ix])
                        except ValueError:
                            pass
                    input_tbl = btn.split('-')[0]
                    tbl_obj = tbl_cls_cols[input_tbl]['object']
                    tbl_cols_k_v = {tbl_cls_cols[input_tbl]['cols'][ix]:inputs[ix] 
                                    for ix, _ in enumerate(inputs)}
                    session.add(
                        tbl_obj(
                            **tbl_cols_k_v   
                        ) 
                    )
                    session.commit()
                    return dbc.Alert(f"did this work? {input_tbl, inputs_txt, tbl_obj, tbl_cols_k_v}"), ''
                else:
                    no_update
            
            create_table_callback(tbl)

# %%    
model_components = ModelComponents(tbl_cls_cols)
callbacks = model_components.get_component_callbacks()

# %%
app = Dash(__name__, 
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

app.layout = serve_layout

if __name__ == '__main__':
    app.run(debug=True)
