# stream lit
import streamlit as st
import pandas as pd
import plotly.express as px 
from PIL import Image

st.set_page_config(page_title='CSV filter')
# st.write("hi")
st.header('CSV Filter')
st.subheader('by Vakeesan')

#load the dataframe
csv_file='docs/dev.jsonl2.csv' 
csv_name='DATA'

df=pd.read_csv(csv_file)
st.dataframe(df)

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
ans = df['yes_no_answer'].unique().tolist()
department_selection = st.multiselect('Select answer',
                                      ans,
                                      default=ans)
# mask = (df['age'].between(*age_selection) & df['department'].isin(department_selection))
# number_of_results = df[mask].shape[0]
# st.markdown(f'*Available results: {number_of_results}*')

#grouping
 