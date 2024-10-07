from dash import callback, no_update, State, Input, Output, ctx
import dash_bootstrap_components as dbc
import datetime

'''
self.model_tbl: tbl_cls_cols dict 
'''

def get_col_type(db, tbl, col):
        table = db.Model.metadata.tables[tbl]
        column = table.columns[col]
        return str(column.type)


def fetch_data(db, model_tbl, tbl):
        res = db.session.query(model_tbl[tbl]['object']).all()
        _, data = result_to_dict_list_with_headers(res)
        return data


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


def create_table_callback(db, model_tbl, tbl_name):
        @callback(
            Output(f'{tbl_name}-table', 'data'),
            Input('dummy-div', 'children')
        )
        def get_data(_):
            return fetch_data(db, model_tbl, tbl_name)


def get_component_callbacks(db, tbl_cls_cols):
    for tbl in tbl_cls_cols:
        @callback(
            Output(f'{tbl}-modal', 'is_open'),
            Input(f'{tbl}-btn', 'n_clicks')
        )
        def show_modal(n1):
            if n1:
                return True
            return False
        
        @callback(
            #TODO: add alert to modal; keep data in form; allow for retry if failure
            # Output(f'{tbl}-modal', "children", allow_duplicate=True),
            Output("alert", "children", allow_duplicate=True),
            Output('dummy-div', 'children', allow_duplicate=True),
            Input(f"{tbl}-submit-btn", "n_clicks"),
            [[State(f'{tbl}-{col}-input', "value") if get_col_type(db, tbl, col) != 'DATE' \
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
                db.session.add(
                    tbl_obj(
                        **tbl_cols_k_v   
                    ) 
                )
                db.session.commit()
                return dbc.Alert(f"did this work? {input_tbl, inputs_txt, tbl_obj, tbl_cols_k_v}"), ''
            else:
                no_update
        
        create_table_callback(db, tbl_cls_cols, tbl)