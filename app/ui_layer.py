# for tbl in tbl_cls_cols for comp in ['_btn', '_modal', '_table']
# note that tbl is model table name, e.g. tables (lower cased plural)

# config MODELS_TO_LOAD = ['User', 'Team', 'Roster']

tbl_to_layout_comps = {
    'users': ['_btn', '_modal'],
    'teams': ['_btn', '_modal', '_table'],
    'rosters': ['_btn', '_modal'],
    'targets': ['_btn', '_modal'],
    'events': ['_btn', '_modal'],
}

tbl_to_ui_cols = {
    'users': ['user_name']
}