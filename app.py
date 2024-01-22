# stream lit
import streamlit as st
import pandas as pd
import plotly.express as px 
from PIL import Image
import json
import ijson
import csv
import pandas as pd

def clean_dataset(input_file_path,output_file_path):
    input_file_path = 'C:\\Users\\vakee\\veracity_ai\\docs\\dev.jsonl'
    output_file_path = 'C:\\Users\\vakee\\veracity_ai\\docs\\cleaned_file.jsonl'

    with open(input_file_path, 'r',encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                json.loads(line)
                outfile.write(line)
            except json.JSONDecodeError as e:
                print(f"Ignoring line due to JSON decoding error: {e}")

# def jsonl2csv():

st.set_page_config(page_title='CSV filter')
# st.write("hi")
st.header('my CSV filter')
st.subheader('by Vakeesan')

#load the dataframe
csv_file='docs/dev.jsonl2.csv'
csv_name='DATA'

df=pd.read_csv(csv_file)
st.dataframe(df)

# pie_chart=px.pie(df,values='question_text',names='document_title')  #plotly express
# st.plotly_chart(pie_chart)

#images in streamlit
# img=Image.open('docs/1.png')
# st.image(img,
#          width=300,
#          caption='streamlit logo',
#          use_column_width=True)

#streamlit selection
# age_selection = (30,40)
ages = df['Age'].unique().tolist()
age_selection = st.slider('Select age range',
                            min_value=min(ages),
                            max_value=max(ages),
                            value=(min(ages),max(ages))
                        )
departments = df['Department'].unique().tolist()
department_selection = st.multiselect('Select departments',
                                      departments,
                                      default=departments)
mask = (df['age'].between(*age_selection) & df['department'].isin(department_selection))
number_of_results = df[mask].shape[0]
st.markdown(f'*Available results: {number_of_results}*')

#grouping
 