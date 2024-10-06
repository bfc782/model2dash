import dash_bootstrap_components as dbc
from dash import dash_table, dcc
import datetime


class ModelComponents:
    # component_dict = {}
    def __init__(self, db, model_tbl):
        self.model_tbl = model_tbl
        self.db = db

        for ix, tbl in enumerate(model_tbl):
            setattr(self, f'{tbl}_btn', dbc.Button(tbl, id=f'{tbl}-btn'))
            setattr(self, f'{tbl}_modal', dbc.Modal(self.make_form(tbl, self.model_tbl[tbl]['cols']), 
                                                            id=f'{tbl}-modal'))
            setattr(self, f'{tbl}_table', dash_table.DataTable(
                id=f'{tbl}-table',
                columns=[{'id':c, 'name':c} for c in self.model_tbl[tbl]['cols']],
            ))

    def get_col_type(self, tbl, col):
        table = self.db.Model.metadata.tables[tbl]
        column = table.columns[col]
        return str(column.type)

    def get_input_component(self, tbl, col):
        col_type = self.get_col_type(tbl, col)
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

    def make_form(self, tbl, cols):
        form = dbc.Form(
            [dbc.Row(
                [
                    dbc.Label(col, width="auto"),
                    dbc.Col(
                        self.get_input_component(tbl, col)
                    )
                ]
            ) for ix, col in enumerate(cols)] +
            [dbc.Row([dbc.Button(f"Submit {tbl}", id=f"{tbl}-submit-btn")])]   
        )
        return form
