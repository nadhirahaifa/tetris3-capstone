import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium 
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from venn import venn
from matplotlib_venn import venn3

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.cache_data()

df = pd.read_csv('output2.csv')

def load_map():
    map = folium.Map(location=[-2.945311, 119.579316], zoom_start=5)
    mCluster = MarkerCluster(name='jobs').add_to(map)

    for id, lat, lng in zip(df['id'].dropna(), df['lat'].dropna(), df['lng'].dropna()):
        folium.Marker([lat, lng], popup=id).add_to(mCluster)

    return map

def work_type():
    df['work_type'] = df['work_type'].fillna('unknown')
    work_type = df['work_type'].value_counts()
    work_type = pd.DataFrame(work_type)
    work_type = work_type.reset_index()
    work_type.columns = ['work_type', 'count']
    # null value is 24

    # return as pie chart
    return px.pie(work_type, values='count', names='work_type', title='Work Type')

def total_applicant():
    bins = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 201]
    labels = ['0', '20-39', '40-59', '60-79', '80-99', '100-119', '120-139', '140-159', '160-179', '180-199', '200+']
    
    df['range'] = pd.cut(df['applicant_count'], bins=bins, labels=labels, right=False)
    grouped_df = df.groupby('range')['applicant_count'].count().reset_index()

    return px.bar(grouped_df, x='range', y='applicant_count', title='Total Applicant')

def pr1():
    programming_language = df['programming'].value_counts()
    programming_language = pd.DataFrame(programming_language)
    programming_language = programming_language.reset_index()
    programming_language.columns = ['programming_language', 'count']

    return px.pie(programming_language, values='count', names='programming_language', title='is programming language required?')

def pr2():
    python = df[df['python'] == True]['id'].tolist()
    r = df[df['r'] == True]['id'].tolist()
    scala = df[df['scala'] == True]['id'].tolist()

    # Create the venn diagram
    plt.figure(figsize=(2,2))
    venn3([set(python), set(r), set(scala)], ('Python', 'R', 'Scala'), set_colors=('skyblue', 'darkblue', 'g'))
    return plt.show()

def pr3():
    python = df[df['python'] == True]['id'].tolist()
    r = df[df['r'] == True]['id'].tolist()
    scala = df[df['scala'] == True]['id'].tolist()

    return px.bar(x=['Python', 'R', 'Scala'], y=[len(python), len(r), len(scala)], title='Programming Language')

def etl1():
    # check if theres any True value in 'etl', 'talend', 'dataiku', 'pentaho', 'snowflake', 'hive', 'spark', 'kafka', 'kinesis'
    cols = ['etl', 'talend', 'dataiku', 'pentaho', 'snowflake', 'hive', 'spark', 'kafka', 'kinesis']

    # Check if any of the columns have true value
    is_true = df[cols].any(axis=1)

    # Get the list of id
    ids = df[is_true]['id'].tolist()

    data_pie =  {'type': ['required', 'not_required'], 
                'count': [len(ids), len(df)-len(ids)]
                }
    pie = pd.DataFrame(data_pie)

    # pie
    return px.pie(pie, values='count', names='type', title='is ETL required')

def etl2():
    cols = ['etl', 'talend', 'dataiku', 'pentaho', 'snowflake', 'hive', 'spark', 'kafka', 'kinesis']
    len_cols = []
    for col in cols:
        len_cols.append(len(df[df[col] == True]['id'].tolist()))

    data_bar = {
        'cols': cols,
        'len_cols': len_cols
    }

    # sort the data by len_cols
    data_bar = pd.DataFrame(data_bar)
    data_bar = data_bar.sort_values(by='len_cols', ascending=False)

    # Create the venn diagram
    return px.bar(x=data_bar['cols'], y=data_bar['len_cols'], title='ETL tools')


def data_viz1():
    cols = ['tableau', 'powerbi', 'matplotlib', 'seaborn', 'plotly',]
    is_true = df[cols].any(axis=1)
    ids = df[is_true]['id'].tolist()

    data_pie =  {'type': ['required', 'not_required'], 
                'count': [len(ids), len(df)-len(ids)]
                }
    
    pie = pd.DataFrame(data_pie)

    return px.pie(pie, values='count', names='type', title='Required Data Visualization')

def data_viz2():
    tableau = df[df['tableau'] == True]['id'].tolist()
    powerbi = df[df['powerbi'] == True]['id'].tolist()
    matplotlib = df[df['matplotlib'] == True]['id'].tolist()
    seaborn = df[df['seaborn'] == True]['id'].tolist()
    plotly = df[df['plotly'] == True]['id'].tolist()

    # merge matplotlib and seaborn and plotly
    others = matplotlib + seaborn + plotly

    # Create the venn diagram
    # fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.figure(figsize=(3,3))
    venn3([set(tableau), set(powerbi), set(others)], ('tableau', 'powerbi', 'others'))


    return plt.show()

def db1():
    cols = ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'sql server', 'bigquery', 'nosql',]

    # Check if any of the columns have true value
    is_true = df[cols].any(axis=1)

    # Get the list of id
    ids = df[is_true]['id'].tolist()

    data_pie =  {'type': ['required', 'not_required'], 
                'count': [len(ids), len(df)-len(ids)]
                }
    pie = pd.DataFrame(data_pie)

    # pie
    return px.pie(pie, values='count', names='type', title='Required database')

def db2():
    cols = ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'sql server', 'bigquery', 'nosql']
    len_cols = []
    for col in cols:
        len_cols.append(len(df[df[col] == True]['id'].tolist()))

    data_bar = {
        'cols': cols,
        'len_cols': len_cols
    }

    # sort the data by len_cols
    data_bar = pd.DataFrame(data_bar)
    data_bar = data_bar.sort_values(by='len_cols', ascending=False)

    # Create the venn diagram
    return px.bar(x=data_bar['cols'], y=data_bar['len_cols'], title='Database')

def others_comm():
    communication = df['communication'].value_counts()
    communication = pd.DataFrame(communication)
    communication = communication.reset_index()
    communication.columns = ['type', 'count']
    # communication

    return px.pie(communication, values='count', names='type', title="communication skills")

def others_eng():
    eng = df['english'].value_counts()
    eng = pd.DataFrame(eng)
    eng = eng.reset_index()
    eng.columns = ['type', 'count']

    return px.pie(eng, values='count', names='type', title="English skills")

def others_etl():
    etl = df['etl'].value_counts()
    etl = pd.DataFrame(etl)
    etl = etl.reset_index()
    etl.columns = ['type', 'count']

    return px.pie(etl, values='count', names='type', title="ETL")

def others_git():
    git = df['git'].value_counts()
    git = pd.DataFrame(git)
    git = git.reset_index()
    git.columns = ['type', 'count']

    return px.pie(git, values='count', names='type', title="GIT")

st.title('Title here')


"### Maps of Distribution of Jobs in Indonesia"
st_folium(load_map(), width=1200, height=500)

"### Distribution of Jobs in Indonesia"
st.plotly_chart(work_type())

"### Total Applicant"
st.plotly_chart(total_applicant())


"### Programming Language"
sec11, sec12, sec13 = st.columns(3)
fig1, exp1= st.columns(2)
fig2, exp2= st.columns(2)
fig3, exp3= st.columns(2)

with sec11:
    with fig1:
        st.plotly_chart(pr1())
    with exp1:
        "penjelasan"
with sec12:
    with fig2:
        st.pyplot(pr2(), use_container_width=False)
    with exp2:
        "penjelasan"
with sec13:
    with fig3:
        st.plotly_chart(pr3())
    with exp3:
        "penjelasan"

"### ETL"
sec21, sec22 = st.columns(2)
fig4, exp4= st.columns(2)
fig5, exp5= st.columns(2)

with sec21:
    with fig4:
        st.plotly_chart(etl1())
    with exp4:
        "penjelasan"
with sec22:
    with fig5:
        st.plotly_chart(etl2())
    with exp5:
        "penjelasan"

"### Data Visualization"
sec31, sec32 = st.columns(2)
fig6, exp6= st.columns(2)
fig7, exp7= st.columns(2)

with sec31:
    with fig6:
        st.plotly_chart(data_viz1())
    with exp6:
        "penjelasan"
with sec32:
    with fig7:
        st.pyplot(data_viz2(), use_container_width=False)
    with exp7:
        "penjelasan"



"### Databases"
sec41, sec42 = st.columns(2)
fig8, exp8= st.columns(2)
fig9, exp9= st.columns(2)

with sec41:
    with fig8:
        st.plotly_chart(db1())
    with exp8:
        "penjelasan"
with sec42:
    with fig9:
        st.plotly_chart(db2())
    with exp9:
        "penjelasan"


"### Others"
sec51, sec52, sec53, sec54, sec55 = st.columns(5)
fig10, exp10= st.columns(2)
fig11, exp11= st.columns(2)
fig12, exp12= st.columns(2)
fig13, exp13= st.columns(2)

with sec51:
    with fig10:
        st.plotly_chart(others_comm())
    with exp10:
        "penjelasan"
with sec52:
    with fig11:
        st.plotly_chart(others_eng())
    with exp11:
        "penjelasan"
with sec53:
    with fig12:
        st.plotly_chart(others_etl())
    with exp12:
        "penjelasan"
with sec54:
    with fig13:
        st.plotly_chart(others_git())
    with exp13:
        "penjelasan"
        



