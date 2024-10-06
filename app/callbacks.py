from dash import callback, no_update, State, Input, Output, ctx
import dash_bootstrap_components as dbc
import datetime

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
            #TODO: add alert to modal; keep data in form; allow for retry if failure
            # Output(f'{tbl}-modal', "children", allow_duplicate=True),
            Output("alert", "children", allow_duplicate=True),
            Output('dummy-div', 'children', allow_duplicate=True),
            Input(f"{tbl}-submit-btn", "n_clicks"),
            [[State(f'{tbl}-{col}-input', "value") if self.get_col_type(tbl, col) != 'DATE' \
                else State(f'{tbl}-{col}-input', "date") \
                for col in self.model_tbl[tbl]['cols']]],
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
                tbl_obj = self.model_tbl[input_tbl]['object']
                tbl_cols_k_v = {self.model_tbl[input_tbl]['cols'][ix]:inputs[ix] 
                                for ix, _ in enumerate(inputs)}
                self.db.session.add(
                    tbl_obj(
                        **tbl_cols_k_v   
                    ) 
                )
                self.db.session.commit()
                return dbc.Alert(f"did this work? {input_tbl, inputs_txt, tbl_obj, tbl_cols_k_v}"), ''
            else:
                no_update
        
        self.create_table_callback(tbl)