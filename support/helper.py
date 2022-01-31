import pandas as pd
import numpy as np
import streamlit as st
from support.load import LoadFiles as lf
from datetime import datetime


class SupportMethods:
    def __init__(self):
        self.store_ids = lf.store_ids
        self.item_ids = lf.item_ids
        self.dept_ids = lf.dept_ids

        self.event_name_1 = lf.event_name_1
        self.event_type_1 = lf.event_type_1
        self.event_name_2 = lf.event_name_2
        self.event_type_2 = lf.event_type_2

        self.trained_models = lf.trained_models
        self.encode_config = lf.encode_config
        self.statistic_features = lf.statistic_features

        self.features = lf.features
        self.days_in_month = lf.days_in_month
        self.businessQuarter = lf.businessQuarter

    def store_dropbox(self):
        store_values = self.store_ids
        store_id = st.sidebar.selectbox(
            'Select a Store ID',
            store_values,
            index=store_values.index('<select store_id>'))
        return store_id

    def department_dropbox(self):
        dept_values = self.dept_ids
        department_id = st.sidebar.selectbox(
            'Select a Department ID',
            dept_values,
            index=dept_values.index('<select department>'))
        return department_id

    def item_dropbox(self, department):
        item_values = self.item_ids.get(
            department, '[<select item_id>]')
        item_id = st.sidebar.selectbox(
            'Select a Item',
            item_values,
            index=item_values.index('<select item id>'))
        return item_id

    def event_type1_dropbox(self):
        event_type1_values = self.event_type_1
        event_type1 = st.sidebar.selectbox(
            'Select a Event Type 1',
            event_type1_values,
            index=event_type1_values.index('<select event type_1>'))
        return event_type1

    def event_name1_dropbox(self, event_type_1):
        event_name1_values = self.event_name_1.get(
            event_type_1, '[<select event name_1>]')
        event_name1 = st.sidebar.selectbox(
            'Select a Event Name 1',
            event_name1_values,
            index=event_name1_values.index('<select event name_1>'))
        return event_name1

    def event_type2_dropbox(self):
        event_type2_values = self.event_type_2
        event_type2 = st.sidebar.selectbox(
            'Select a Event Type 2',
            event_type2_values,
            index=event_type2_values.index('<select event type_2>'))
        return event_type2

    def event_name2_dropbox(self, event_type_2):
        event_name2_values = self.event_name_2.get(
            event_type_2, '[<select event name_2>]')
        event_name2 = st.sidebar.selectbox(
            'Select a Event Name 2',
            event_name2_values,
            index=event_name2_values.index('<select event name_2>'))
        return event_name2

    def get_date(self):
        date = st.sidebar.date_input("Pick a date", min_value=datetime.combine(datetime.now().today(), datetime.min.time()))
        return datetime.combine(date.today(), datetime.min.time())

    def sales_forecasting(self):
        store_id = self.store_dropbox()
        department_id = self.department_dropbox()
        if (store_id != '<select store_id>'):
            if (department_id != '<select department>'):
                item_id = self.item_dropbox(department_id)
                date = self.get_date()
                # should add event base inputs
                if (item_id != '<select item id>'):
                    if st.sidebar.button('Submit'):
                        start = datetime.now()
                        predicted_value = self.predict_single_entry(
                            store_id, item_id, request_date=date)
                        end = datetime.now()
                        st.write("Request got completed in ", int(
                            (end-start).total_seconds() * 1000),  " milliseconds")
                        st.write('predicted_value', predicted_value)

    def compute_statistic_features(self, data, store_id):
        for category in ['store', 'dept', 'item']:
            for peroidic in ['month', 'wday']:
                for stats in ['min', 'max', 'mean', 'median', 'std']:
                    key = f'{category}_{peroidic}_{stats}' 
                    data[key] = self.statistic_features[key].get(f'{store_id}_train_fea_{data.get(peroidic)}')

    def predict_single_entry(self, store_id, item_id, event_type_1=None, event_name_1=None, event_type_2=None, event_name_2=None, request_date=datetime.now()):

        # create dictionary to store preprocessed and compute feature engineered values
        data = {}

        # encoded values
        data['item_id'] = self.encode_config['item_id_map'].get(item_id)
        data['dept_id'] = self.encode_config['dept_id_map'].get(
            '_'.join(item_id.split('_')[:2]))
        data['cat_id'] = self.encode_config['cat_id_map'].get(
            item_id.split('_')[0])
        data['store_id'] = self.encode_config['store_id_map'].get(store_id)
        data['state_id'] = self.encode_config['state_id_map'].get(store_id[:2])
        data['d'] = (request_date -
                     datetime.strptime('2011-01-29', '%Y-%m-%d')).days
        # sat-1 sun-2 mon-3 tue-4 wed-5 thu-6 fri-7
        data['wday'] = request_date.weekday(
        )+3 if request_date.weekday() < 6 else request_date.weekday()-5
        data['month'] = request_date.month
        data['year'] = request_date.year
        data['event_name_1'] = 1 if not self.encode_config['event_name_1_map'].get(
            event_name_1) else self.encode_config['event_name_1_map'].get(event_name_1)
        data['event_type_1'] = 1 if not self.encode_config['event_type_1_map'].get(
            event_type_1) else self.encode_config['event_type_1_map'].get(event_type_1)
        data['event_name_2'] = 1 if not self.encode_config['event_name_2_map'].get(
            event_name_2) else self.encode_config['event_name_2_map'].get(event_name_2)
        data['event_type_2'] = 1 if not self.encode_config['event_type_2_map'].get(
            event_type_2) else self.encode_config['event_type_2_map'].get(event_type_2)
        data['snap_CA'] = 1 if store_id[:2] == 'CA' else 0
        data['snap_TX'] = 1 if store_id[:2] == 'TX' else 0
        data['snap_WI'] = 1 if store_id[:2] == 'WI' else 0
        data['sell_price'] = self.statistic_features['sell_price_mean'].get(
            f'{store_id}_train_fea')

        # calculate wm_yr_wk
        yr = str(request_date.year)[2:]
        wk = int(np.ceil(
            ((request_date - datetime.strptime(f'{request_date.year}-01-01', '%Y-%m-%d')).days-5)/7))
        wk = f'0{wk}' if wk < 9 else f'{wk}'
        wm_yr_wk = int(''.join(['1', yr, wk]))
        data['wm_yr_wk'] = wm_yr_wk

        # feature engineered values
        data['IsWeekend'] = 1 if data.get('wday') in [1, 2] else 0
        data['IsFoods'] = 1 if data.get('cat_id') == 'FOODS' else 0
        data['IsFoods_3'] = 1 if data.get('dept_id') == 'FOODS_3' else 0
        data['IsReligiousEvent'] = 1 if data.get('event_type_1') == 5 else 0
        data['BusinessQuarter'] = self.businessQuarter[data.get('month')]
        data['days_in_month'] = self.days_in_month[data.get('month')]
        data['IsMonthStart'] = 1 if request_date.day == 1 else 0
        data['IsMonthEnd'] = 1 if request_date.day in [28, 29, 30, 31] else 0
        data['IsYearStart'] = 1 if (data.get('month') == 1) & (
            data.get('IsMonthStart') == 1) else 0
        data['IsYearEnd'] = 1 if (data.get('month') == 12) & (
            data.get('IsMonthEnd') == 1) else 0
        data['IsQuaterStart'] = 1 if data.get('BusinessQuarter') in [
            1, 4, 7, 11] else 0
        data['IsQuaterEnd'] = 1 if data.get('BusinessQuarter') in [
            3, 6, 9, 12] else 0
        data['IsLeapYear'] = 1 if ((data.get('year') % 4 == 0) and (
            data.get('year') % 100 != 0)) or (data.get('year') % 400 == 0) else 0

        # compute statistical features
        self.compute_statistic_features(data, store_id)

        # prepare input values for prediction
        input = pd.DataFrame(data, index=[0])[self.features].values

        # load the respective model
        model = self.trained_models[store_id]

        # predict the future sale
        predicted_sale_value = model.predict(input)

        return predicted_sale_value[0]

    def set_page_title(self, title):
        st.sidebar.markdown(unsafe_allow_html=True, body=f"""
            <iframe height=0 srcdoc="<script>
                const title = window.parent.document.querySelector('title') \

                const oldObserver = window.parent.titleObserver
                if (oldObserver) {{
                    oldObserver.disconnect()
                }} \

                const newObserver = new MutationObserver(function(mutations) {{
                    const target = mutations[0].target
                    if (target.text !== '{title}') {{
                        target.text = '{title}'
                    }}
                }}) \

                newObserver.observe(title, {{ childList: true }})
                window.parent.titleObserver = newObserver \

                title.text = '{title}'
            </script>" />
        """)
