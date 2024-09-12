import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium 
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from matplotlib_venn import venn3
from pathlib import Path

st.set_page_config(layout="wide")

# read dataset
df_path = Path(__file__).parents[1] / 'output2.csv'
df = pd.read_csv(df_path)

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

    return px.pie(programming_language, values='count', names='programming_language', title='is programming language required')

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

def etl3():
    etl = df[df['etl'] == True]['id'].tolist()
    spark = df[df['spark'] == True]['id'].tolist()
    kafka = df[df['kafka'] == True]['id'].tolist()
    hive = df[df['hive'] == True]['id'].tolist()
    snowflake = df[df['snowflake'] == True]['id'].tolist()
    talend = df[df['talend'] == True]['id'].tolist()
    dataiku = df[df['dataiku'] == True]['id'].tolist()
    kinesis = df[df['kinesis'] == True]['id'].tolist()
    pentaho = df[df['pentaho'] == True]['id'].tolist()

    others = kafka + hive + snowflake + talend + dataiku + kinesis + pentaho

    plt.figure(figsize=(3,3))
    # Create the venn diagram
    venn3([set(etl), set(spark), set(others)], ('etl', 'spark', 'others'))
    return plt.show()

def data_viz1():
    cols = ['dv', 'tableau', 'powerbi', 'matplotlib', 'seaborn', 'plotly']

    # Check if any of the columns have true value
    is_true = df[cols].any(axis=1)

    # Get the list of id
    ids = df[is_true]['id'].tolist()

    data_pie =  {'type': ['required', 'not_required'], 
                'count': [len(ids), len(df)-len(ids)]
                }
    pie = pd.DataFrame(data_pie)

    # pie
    return px.pie(pie, values='count', names='type', title='is data visualization required')

def data_viz2():
    cols = ['dv', 'tableau', 'powerbi', 'matplotlib', 'seaborn', 'plotly']
    len_cols = []
    for col in cols:
        len_cols.append(len(df[df[col] == True]['id'].tolist()))

    data_bar = {
        'cols': ['visualisasi', 'tableau', 'powerbi', 'matplotlib', 'seaborn', 'plotly'],
        'len_cols': len_cols
    }

    # sort the data by len_cols
    data_bar = pd.DataFrame(data_bar)
    data_bar = data_bar.sort_values(by='len_cols', ascending=False)

    # Create the bar chart
    return px.bar(x=data_bar['cols'], y=data_bar['len_cols'], title='Data Visualization tools')

def data_viz3():
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

    return px.pie(communication, values='count', names='type', title="Communication skills")

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

def intro():
    st.markdown("author: Nadhira Haifa Firdausi")
    st.markdown("email: nadhirahaifafirdausi@gmail.com")
    st.markdown(r"""
                    <p style='text-align:justify; margin:5%' >
                    Sebagai seorang yang tertarik untuk terjun di bidang data dan menjadi praktisi data, melakukan riset mendalam mengenai pekerjaan dalam industri ini merupakan langkah yang penting. Salah satu sumber informasi yang berharga adalah melakukan scraping data dari LinkedIn. Dengan melakukan scraping data dari LinkedIn, kita dapat memperoleh pemahaman yang lebih jelas mengenai situasi pekerjaan di bidang data di Indonesia. Informasi yang didapatkan melalui pengambilan data ini akan membantu dalam mengetahui tren pekerjaan di bidang data, seperti jenis pekerjaan yang paling banyak tersedia, persyaratan umum yang dibutuhkan oleh perusahaan, kemampuan yang paling dicari, dan perusahaan-perusahaan terkemuka yang aktif mencari profesional data. Dengan demikian, pengambilan data ini akan memberikan wawasan yang berguna bagi individu yang berencana untuk membangun karir sebagai praktisi data di Indonesia. 
                    </p>
                    """, unsafe_allow_html=True)
    with st.container():
        st.image('pict2.png', caption='Proses dan Tools Project')
        st.text("")

    pic, expl = st.columns(2)
    with pic:
            st.image('pict1.png')
    with expl:
        st.markdown(r"""
                    <p style='text-align:justify; margin:10%' >
                    Scraping dilakukan pada website linkedin dengan menggunakan python, library selenium dan web browser chrome untuk mendapatkan data berupa csv. Keyword yang digunakan untuk mencari pekerjaan di bidang data adalah Data Engineer, Data Analyst, Data Science, Business Intelligence, ETL developer dan Business Information dengan total data yang didapatkan adalah 220 data.
                    </p>
                    """, unsafe_allow_html=True)

def main():
    st.title('Scraping and Analyzing LinkedIn Job Data: A Study of Tools and Skills in the Data-Driven Professions in Indonesia')

    intro()
    
    "### Maps of Distribution of Jobs in Indonesia"
    st_folium(load_map(), width=1200, height=500)


    "### Distribution of Jobs in Indonesia"
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(work_type())
    with col2:
        st.markdown(r"""
                    <p style='text-align:justify; margin:25%' >
                    Lowongan pekerjaan pada bidang data per pada Mei 2023 mayoritas dengan tipe on-site (44.5) diikuti dengan remote (25%) dan hybrid 19.5%
                    </p>
                    """, unsafe_allow_html=True)

    "### Total Applicant"
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(total_applicant())
    with col4:
        st.markdown(r"""
                    <p style='text-align:justify; margin:25%' >
                    Total pelamar pada bidang data per Mei 2023 mayoritas berjumlah 0-19 orang (41.5%) diikuti dengan 20-39 orang (20.5%) dan 40-59 orang (12.5%)
                    </p>
                    """, unsafe_allow_html=True)


    "### Programming Language"
    tab1, tab2, tab3 = st.tabs(["pie chart", "venn", "bar chart"])
    with tab1:
        pict1, expl1 = st.columns(2)
        with pict1:
            st.plotly_chart(pr1())
        with expl1:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Lowongan pekerjaan pada bidang data per pada Mei 2023 mayoritas sebanyak 60% lowongan membutuhkan pelamar yang memiliki kemampuan pada bahasa pemrograman seperti pyhon, r, dan scala.
                        </p>
                        """, unsafe_allow_html=True)
    with tab2:
        pict2, expl2 = st.columns(2)
        with pict2:
            st.pyplot(pr2(), use_container_width=False)
        with expl2:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%'>
                        Bahasa pemrograman yang paling banyak diminati/digunakan oleh perusahaan adalah python.<br>
                        Jika dilihat pada diagram venn disamping, bahasa R dan scala hanya alternatif dari bahasa python, bahkan bahasa semua lowongan yang menyantumkan R menyantumkan juga python. Sehingga bahasa python merupakan pilihan bahasa terbaik dipelajari untuk seorang praktisi data.
                        </p>
                        """, unsafe_allow_html=True)
    with tab3:
        pict3, expl3 = st.columns(2)
        with pict3:
            st.plotly_chart(pr3())
        with expl3:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Bahasa pemrograman yang paling banyak diminati/digunakan oleh perusahaan adalah python yang disebutkan129 lowongan secara spesifik. Adapun bahasa R disebutkan 52 lowongan dan scala 21.
                        </p>
                        """, unsafe_allow_html=True)
        
    "### ETL"
    tab1, tab2, tab3 = st.tabs(["pie chart", "bar chart", "venn"])
    with tab1:
        expl1, pict1 = st.columns(2)
        with expl1:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Meskipun ETL software disebutkan dibutuhkan pada lowongan sebanyak bahasa pemrograman, tetapi penguasaan ETL software tetap dibutuhkan oleh 37.3% perusahaan atau sebanyak 82 perusahaan.
                        </p>
                        """, unsafe_allow_html=True)
        with pict1:
            st.plotly_chart(etl1())
    with tab2:
        expl2, pict2 = st.columns(2)
        with expl2:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        ETL software yang dibutuhkan oleh perusahaan adalah paling banyak disebutkan adalah apache spark diikuti apache kafka dan hive. Namun apabila dilihat bahwa penyebutan ETL lebih banyak dibandingkan dengan penyebutan software ETL secara eksplisit.
                        </p>
                        """, unsafe_allow_html=True)
        with pict2:
            st.plotly_chart(etl2())
    with tab3:
        expl3, pict3 = st.columns(2)
        with expl3:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Berdasarkan diagram venn diatas, penyebutan ETL juga banyak dengan tidak memasukkan software yang digunakan secara spesifik sehingga penguasaan konsep mengenai software ETL lebih penting dibandingkan dengan penguasaan software tertentu.
                        </p>
                        """, unsafe_allow_html=True)
        with pict3:
            st.pyplot(etl3(), use_container_width=False)

    "### Data Visualization"
    tab1, tab2, tab3 = st.tabs(["pie chart", "venn", "bar chart"])
    with tab1:
        pict1, expl1 = st.columns(2)
        with pict1:
            st.plotly_chart(data_viz1())
        with expl1:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Tentunya sebagai seorang praktisi data, data visualisasi merupakan suatu hal salah satu skill yang penting untuk dimiliki. Seperti yang dapat dilihat pada pie chart, sebanyak 60% menyebutkan software visualisasi maupun kata visualisasi itu sendiri.
                        </p>
                        """, unsafe_allow_html=True)
    with tab2:
        pict2, expl2 = st.columns(2)
        with pict2:
            st.plotly_chart(data_viz2())
        with expl2:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Tools visualisasi yang paling sering disebutkan adalah tableau. Namun apabila dilihat bahwa jumlah perusahaan yang menyebutkan software visualisasi secara tidak spesifik pun tidak jauh berbeda. Sementara penyebutan matplotlib, seaborn dan plotly <10. Hal ini menunjukkan bahwa kemampuan untuk menggunakan software visualisasi lebih dibutuhkan praktisi data untuk memberikan informasi sehingga lebih mudah untuk berkolaborasi.
                        </p>
                        """, unsafe_allow_html=True)
    with tab3:
        pict3, expl3 = st.columns(2)
        with pict3:
            st.pyplot(data_viz3(), use_container_width=False)
        with expl3:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Visualisasi data biasanya dapat dilakukan selama menguasai konsep dari visualisasi data itu sendiri, software biasanya merupakan sebuah alat pembantu untuk mempermudah dari visualisasi tersebut. Namun, Tableau masih memiliki keunggulan dibandingkan dengan powerBI dimana 57 lowongan menyebutkannya secara eksplisit.
                        </p>
                        """, unsafe_allow_html=True)
            
    "### Databases"
    expl1, pict1 = st.columns(2)
    with expl1:
        st.markdown(r"""
                    <p style='text-align:justify; margin:25%' >
                    Seorang praktisi data dibutuhkan untuk menguasai database yakni sebanyak 65.5% menyebutkannya secara eksplisit, lebih banyak dibandingkan yang perlu menguasai bahasa pemrograman yakni 60.5%
                    </p>
                    """, unsafe_allow_html=True)
    with pict1:
        st.plotly_chart(db1())

    "### Others"
    tab1, tab2, tab3 = st.tabs(["Communication", "English", "GIT"])
    # todo PPT
    with tab1:
        pict1, expl1 = st.columns(2)
        with pict1:
            st.plotly_chart(others_comm())
        with expl1:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Pada bidang data, kemampuan komunikasi yang paling banyak dibutuhkan adalah kemampuan komunikasi verbal (75%) diikuti dengan kemampuan komunikasi non-verbal (25%)
                        </p>
                        """, unsafe_allow_html=True)
    with tab2:
        pict2, expl2 = st.columns(2)
        with pict2:
            st.plotly_chart(others_eng())
        with expl2:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Kemampuan menguasai bahasa inggris merupakan salah satu kemampuan yang penting untuk dimiliki dimana hingga 64.5% lowongan membutuhkan pelamar yang memiliki kemampuan bahasa inggris. 
                        Kemampuan bahasa inggris ini penting karena dibutuhkan untuk berkomunikasi dengan tim, stakeholder maupun pihak eksternal dengan latar belakang yang berbeda-beda.
                        </p>
                        """, unsafe_allow_html=True)
    with tab3:
        pict3, expl3 = st.columns(2)
        with pict3:
            st.plotly_chart(others_git())
        with expl3:
            st.markdown(r"""
                        <p style='text-align:justify; margin:25%' >
                        Ternyata seorang praktisi data tidak dituntut untuk dapat menguasai git karena hanya 5.45% lowongan yang menyebutkan pelamar harus menguasai git.
                        </p>
                        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()