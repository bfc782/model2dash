# %%
from dash import Dash, dcc, html, callback, Output, Input, State, \
    no_update, callback_context, ctx, dash_table
import datetime
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import pandas as pd

# def check_tbl(db, tbl):
#     engine = create_engine(f"sqlite:///{db}")
#     session = Session(engine)
#     res = session.query(tbl).all()
#     return [rec for rec in res]

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
    print(rows)
    dash_table_columns = [{'name': c, 'id': c} for c in column_headers]

    return dash_table_columns, rows

def fetch_data(session, tbl):
    res = session.query(tbl_cls_cols[tbl]['object']).all()
    _, data = result_to_dict_list_with_headers(res)
    return data

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, user_name={self.user_name!r})"
    
class Team(Base):
    __tablename__ = "teams"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(30))
    max_size: Mapped[int]
    min_size: Mapped[int]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_date: Mapped[datetime.date]

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, team_name={self.team_name!r}, creator_id={self.creator_id!r})"

### Rest of models

class Roster(Base): # userteamlink
    __tablename__ = "rosters"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_status: Mapped[str] = mapped_column(String(30)) # Invited, Confirmed, Rejected, Left, Inactive
    user_role: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Roster(team_id={self.team_id!r}, user_id={self.user_id!r})"

class Baseline(Base):
    __tablename__ = "baselines"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    baseline_event_result: Mapped[int] # in minutes
    baseline_event_url: Mapped[str] = mapped_column(String(150))
    baseline_block_training_count: Mapped[int] # in training sessions

    def __repr__(self) -> str:
        return f"Baseline(user_id={self.user_id!r}, event_id={self.event_id!r})"

class Target(Base):
    __tablename__ = "targets"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"))
    target_event_result: Mapped[int] # in minutes
    target_block_training_count: Mapped[int] # in training sessions
    target_block_training_metric: Mapped[str] # Distance, Time, Repetitions, Ascent
    target_block_training_measure: Mapped[int] # in minutes, km, reps, m

    def __repr__(self) -> str:
        return f"Target(user_id={self.user_id!r}, event_id={self.event_id!r}, training_id={self.training_id!r})"

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.date]
    url: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(150))

class Prizegiving(Base):
    __tablename__ = "prizegivings"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    ceremony_date: Mapped[datetime.date]
    ceremony_location: Mapped[str] = mapped_column(String(150))
    first_prize: Mapped[str] = mapped_column(String(30))
    second_prize: Mapped[str] = mapped_column(String(30))
    team_prize: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Prizegiving(id={self.id!r}, challenge_id={self.challenge_id!r}, user_id={self.user_id!r})"

class Training(Base):
    __tablename__ = "trainings"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))
    activity: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(30))
    phase: Mapped[int]
    intensity: Mapped[str] = mapped_column(String(30)) # Low, Medium, High
    metric: Mapped[str] = mapped_column(String(30)) # Distance, Time, Repetitions, Ascent
    target: Mapped[int]

    def __repr__(self) -> str:
        return f"Training(id={self.id!r}, name={self.training_name!r}"
    
class Challenge(Base):
    __tablename__ = "challenges"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"))
    start_date: Mapped[datetime.date]
    block_duration: Mapped[int] # in weeks
    wager: Mapped[int] # in CCY
    currency: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Challenge(id={self.id!r}, challenge_name={self.name!r}, challenge_creator={self.challenge_creator!r})"
    
class UpcomingForecast(Base):
    __tablename__ = "upcoming_forecasts"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"))
    forecast_block_training_count: Mapped[int] # in training sessions
    prior_forecast_block_training_count: Mapped[int] # in training sessions
    prior_forecast_achieved: Mapped[bool]

    def __repr__(self) -> str:
        return f"UpcomingForecast(user_id={self.user_id!r}, event_id={self.event_id!r})"
    
class TrainingSession(Base):
    __tablename__ = "training_sessions"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"))
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"))
    completion_date: Mapped[datetime.date]
    upload_timestamp: Mapped[datetime.date] # within 2 days of completion and before block end date
    url: Mapped[str] = mapped_column(String(150))

    def __repr__(self) -> str:
        return f"TrainingSession(user_id={self.user_id!r}, training_id={self.training_id!r})"

class Block(Base): # TODO: make this a view
    __tablename__ = "blocks"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30)) # weekly, fortnightly, monthly
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    block_number: Mapped[int]
    block_start_date: Mapped[datetime.date]
    block_end_date: Mapped[datetime.date]

    def __repr__(self) -> str:
        return f"Block(id={self.id!r}, name={self.name!r}"

class ProgressScore(Base): # TODO: make this a view
    __tablename__ = "progress_scores"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"))
    user_block_training_count: Mapped[int] # in training sessions
    team_block_training_count: Mapped[int] # in training sessions
    user_total_training_count: Mapped[int] # in training sessions
    team_total_training_count: Mapped[int] # in training sessions


    def __repr__(self) -> str:
        return f"ProgressScore(user_id={self.user_id!r}, challenge_id={self.challenge_id!r})"


### End of rest of models

engine = create_engine("sqlite:///intendif.db", echo=True,
                       connect_args={'check_same_thread': False})
session = Session(engine)

Base.metadata.create_all(engine)

# %%
tbl_cls_cols = {cls.__tablename__: {'object': cls, 'cols': cls.__table__.columns.keys()} \
                for cls in Base.__subclasses__() if cls.__name__ != "Base"}

tbl_cls_col_type = {cls.__tablename__: {'object': cls, 'cols': cls.__table__.columns.keys()} \
                for cls in Base.__subclasses__() if cls.__name__ != "Base"}

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
                    # dbc.Input(placeholder=f'enter {col}', id=f"{tbl}-{col}-input")
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
                        except:
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
                        # getattr(model_components, 'users_btn'),
                        # model_components.users_btn,
                        # model_components.component_dict['users-btn'],

                        # getattr(model_components, f'{tbl}_modal'),
                        # getattr(model_components, 'users_modal'),
                        # model_components.users_modal,
                        # model_components.component_dict['users-modal'],

                        # getattr(model_components, f'{tbl}_table')
                        # getattr(model_components, 'users_table'),
                        # model_components.users_table,
                        # model_components.component_dict['users-table'],

                        # getattr(model_components, 'teams_btn'),
                        # model_components.teams_btn,
                        #component_dict['teams_btn'],

                        # getattr(model_components, 'teams_modal'),
                        # model_components.teams_modal,
                        # model_components.component_dict['teams-modal'],

                        # getattr(model_components, 'teams_table'),
                        # model_components.teams_table
                        # model_components.component_dict['teams-table'],
                        for tbl in tbl_cls_cols for comp in ['_btn', '_modal', '_table']
                    ]
                ) 

app.layout = serve_layout

if __name__ == '__main__':
    app.run(debug=True)
