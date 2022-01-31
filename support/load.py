import pandas as pd
import os
import lightgbm as gbm


file_path = os.getcwd()+'/model_training/production_data/'


class LoadFiles:

    # load trained models
    trained_models = pd.read_pickle(
        file_path+'trained_models_with_500_trees.pkl')

    # load encoding feature values
    encode_config = pd.read_pickle(file_path+'encode_config.pkl')

    # load feature engineered statistical features
    statistic_features = pd.read_pickle(file_path+'statistic_features.pkl')

    # store data
    store_ids = pd.read_pickle(file_path+'store_ids.pkl')

    # depatment data
    dept_ids = pd.read_pickle(file_path+'dept_ids.pkl')

    # event 1 names with event type 1
    event_name_1 = pd.read_pickle(file_path+'event_name_1.pkl')

    # type of event 1
    event_type_1 = pd.read_pickle(file_path+'event_type_1.pkl')

    # event 2 names with event type 2
    event_name_2 = pd.read_pickle(file_path+'event_name_2.pkl')

    # type of event 2
    event_type_2 = pd.read_pickle(file_path+'event_type_2.pkl')

    # required features to predict
    features = pd.read_pickle(file_path+'features.pkl')

    # items data
    item_ids = pd.read_pickle(file_path+'item_ids.pkl')

    # encode businessQuarter mapping
    businessQuarter = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2,
                       6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}

    # encode days mapping
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31,
                     6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
