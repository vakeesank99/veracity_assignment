# stream lit
import streamlit as st
import pandas as pd
import plotly.express as px 
from PIL import Image
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

st.set_page_config(page_title='CSV filter')
# st.write("hi")
st.header('CSV Filter')
#st.subheader('by Vakeesan')

#load the dataframe
csv_file='docs/dev.jsonl2.csv' # change the file path here
csv_name='DATA'

df=pd.read_csv(csv_file)
st.dataframe(filter_dataframe(df))

# pie_chart=px.pie(df,values='yes_no_answer',names='document_title')  #plotly express
# st.plotly_chart(pie_chart)

#images in streamlit
# img=Image.open('docs/1.png')
# st.image(img,
#          width=300,
#          caption='streamlit logo',
#          use_column_width=True)

#streamlit selection
# age_selection = (30,40)
# ages = df['Age'].unique().tolist()
# age_selection = st.slider('Select age range',
#                             min_value=min(ages),
#                             max_value=max(ages),
#                             value=(min(ages),max(ages))
#                         )
# ans = df['yes_no_answer'].unique().tolist()
# department_selection = st.multiselect('Select answer',
#                                       ans,
#                                       default=ans)
# mask = (df['age'].between(*age_selection) & df['department'].isin(department_selection))
# number_of_results = df[mask].shape[0]
# st.markdown(f'*Available results: {number_of_results}*')

#grouping
 