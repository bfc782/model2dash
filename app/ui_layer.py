# for tbl in tbl_cls_cols for comp in ['_btn', '_modal', '_table']
# note that tbl is model table name, e.g. tables (lower cased plural)

# config MODELS_TO_LOAD = ['User', 'Team', 'Roster', 'Target', 'Event', 'Training', 'Challenge', 'TrainingSession']

tbl_to_layout_comps = {
    'users': ['_btn', '_modal', '_table'],
    'teams': ['_btn', '_modal', '_table'],
    'rosters': ['_btn', '_modal', '_table'],
    'targets': ['_btn', '_modal', '_table'],
    'events': ['_btn', '_modal', '_table'],
    'trainings': ['_btn', '_modal', '_table'],
    'challenges': ['_btn', '_modal', '_table'],
    'training_sessions': ['_btn', '_modal', '_table'],
}

tbl_to_ui_cols = {
    'users': ['user_name']
}