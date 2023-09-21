# IMPORTING NECESSARY LIBRARIES

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sns
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import geojson

# SQL CONNECTION

host = "127.0.0.1"
user = 'root'
password = '12345'
port = 3306
database = 'phonepe_pulse'

# SQL CONNECTION
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            auth_plugin='mysql_native_password'
            )
mycursor = mydb.cursor()
mycursor.execute("USE phonepe_pulse")


# ENGINE CREATION

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# STREAMLIT PAGE CONFIGURATION

st.set_page_config(page_title="PhonePe Pulse Data Visualization ",
                   page_icon=":tada",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """Phonepe"""})

# OPTION MENU

with st.sidebar:
    selected = option_menu(None, ['About', 'PhonePe', 'Aggregated Transaction', 'Map Transaction', 'Top Transaction', 'Aggregated User', 'Map User', 'Top User', 'Queries'],
                           icons=['play', 'play', 'card-text',  'card-text', 'card-text', 'card-text', 'card-text', 'card-text', 'play'],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "10px",
                                                "--hover-color": "#713ABE"},
                                   "icon": {"font-size": "15px"},
                                   "container": {"max-width": "2000px"},
                                   "nav-link-selected": {"background-color": "#713ABE"}})

# ABOUT PAGE

if selected == "About":

    with st.container():
        st.title(""":violet[Project]: Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly:""")

    with st.container():
        st.header(":violet[Statement]:")
        st.write("""The Phonepe pulse Github repository contains a large amount of data related to 
        various metrics and statistics. The goal is to extract this data and process it to obtain insights and 
        information that can be visualized in a user-friendly manner.""")

    with st.container():
        st.header(":violet[Technologies Use]:")
        st.write(" Github Cloning, Python, Pandas, MySQL,SQLAlchemy, Streamlit, and Plotly.")

    with st.container():
        st.header(":violet[Overview] :")
        st.write("##")
        st.write("""The result of this project will be a live geo visualization dashboard that displays information
         and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner. 
         The dashboard will have at least 10 different dropdown options for users to select different facts and 
         figures to display. The data will be stored in a MySQL database for efficient retrieval and the dashboard 
         will be dynamically updated to reflect the latest data.
         Overall, the result of this project will be a comprehensive and user-friendly solution for extracting, 
         transforming, and visualizing data from the Phonepe pulse Github repository..""")



# PHONEPE PAGE

elif selected == "PhonePe":
    with st.container():
        st.title(":violet[PhonePe]")
        st.write("""PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, 
        Karnataka, India.PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer.
        The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.""")

    with st.container():
        st.subheader(":violet[One app for all things money:]")
        st.write("Pay bills, recharge, send money, buy gold, invest and shop at your favourite stores.")
        st.subheader(":violet[Pay whenever you like, wherever you like:]")
        st.write("Choose from options like UPI, the PhonePe wallet or your Debit and Credit Card.")
        st.subheader(":violet[Find all your favourite apps on PhonePe Switch.]")
        st.write("Book flights, order food or buy groceries. Use all your favourite apps without downloading them.")

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader(":violet[Contact Us]")
            st.write("PhonePe Private Limited")
            st.write("Office-2, Floor 4,5,6,7, Wing A, Block A,")
            st.write("Salarpuria Softzone, Service Road,")
            st.write("Green Glen Layout, Bellandur, Bangalore South,")
            st.write("Bangalore, Karnataka - 560103, India")
            st.write("CIN: U67190KA2012PTC176031")
            st.subheader(":violet[Download the App]")
            st.write("Click the below link to download PhonePe App")
            st.write("""The PhonePe app is safe and secure, meets all your payment, investment, mutual funds, insurance 
                and banking needs, and is much better than Internet banking.""")
            st.write("[Download](https://play.google.com/store/apps/details?id=com.phonepe.app&hl=en_IN&gl=US)")

        with right_column:
            video_file = open('C:/Users/MyPC/Downloads/phonepe.mp4', 'rb')
            video_bytes = video_file.read()

            st.video(video_bytes)



# AGGREGATED TRANSACTION PAGE

if selected == "Aggregated Transaction":

    st.title("AGGREGATED TRANSACTION")
    Quarter = st.selectbox("Select the quarter:", [1, 2, 3, 4])
    Year = st.selectbox("Select the year:", [2018, 2019, 2020, 2021, 2022])
    Transaction_type = st.selectbox("Select the Ttype:",
                                    ['Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments',
                                     'Financial Services', 'Others'])

    query1 = """SELECT State, Year, Quarter, Transaction_type, MAX(Transaction_count) AS Max_Count,MAX(Transaction_amount) AS Max_Amount 
                        FROM agg_trans 
                        WHERE Quarter = %s AND Transaction_type = %s AND Year = %s 
                        GROUP BY State, Year, Quarter, Transaction_type;"""

    df = pd.read_sql(query1, con=engine,
                     params=(Quarter, Transaction_type, Year))

    st.write(df)

    st.bar_chart(df.set_index('State')['Max_Amount'])


# MAP TRANSACTION PAGE

elif selected == "Map Transaction":

    st.title("MAP TRANSACTION")
    Quarter = st.selectbox("Select the quarter:", [1, 2, 3, 4])
    Year = st.selectbox("Select the year:", [2018, 2019, 2020, 2021, 2022])

    query3 = """SELECT State, Year, Quarter, MAX(Transaction_count) AS Max_Count, MAX(Transaction_amount) AS Max_Amount
                    FROM map_trans
                    WHERE Quarter = %s AND Year = %s
                    GROUP BY State, Year, Quarter;"""

    df = pd.read_sql(query3, con=engine, params=(Quarter, Year))

    st.write(df)

    st.bar_chart(df.set_index('State')['Max_Amount'])


# TOP TRANSACTION PAGE

elif selected == "Top Transaction":

    st.title("TOP TRANSACTION")
    Quarter = st.selectbox("Select the quarter:", [1, 2, 3, 4])
    Year = st.selectbox("Select the year:", [2018, 2019, 2020, 2021, 2022])

    query5 = """SELECT State, Year, Quarter, MAX(Transaction_count) AS Max_Count,MAX(Transaction_amount) AS Max_Amount
                    FROM top_trans_dist
                    WHERE Quarter = %s AND Year = %s
                    GROUP BY State, Year, Quarter;"""

    df = pd.read_sql(query5, con=engine, params=(Quarter, Year))

    st.write(df)

    st.bar_chart(df.set_index('State')['Max_Amount'])


# AGGREGATED USER PAGE

elif selected == "Aggregated User":

    st.title("AGGREGATED USER")
    Quarter = st.selectbox("Select the quarter:", [1, 2, 3, 4])
    Year = st.selectbox("Select the year:", [2018, 2019, 2020, 2021, 2022])
    Device_Brands = st.selectbox("Select the M-Brand:",
                                 ['Xiaomi', 'Samsung', 'Vivo', 'Oppo', 'OnePlus', 'Realme', 'Apple', 'Motorola',
                                  'Lenovo', 'Huawei', 'Others'])

    query2 = """SELECT State, Year, Quarter, Brand, Transaction_count, Percentage
                    FROM agg_user
                    WHERE Quarter = %s AND Year = %s AND Brand = %s
                    GROUP BY State, Year, Quarter,Transaction_count , Percentage;"""

    df = pd.read_sql(query2, con=engine,
                     params=(Quarter, Year, Device_Brands))

    st.write(df)

    st.bar_chart(df.set_index('State')['Transaction_count'])


# MAP USER PAGE

elif selected == "Map User":

    st.title("MAP USER")
    Quarter = st.selectbox("Select the quarter:", [1, 2, 3, 4])
    Year = st.selectbox("Select the year:", [2018, 2019, 2020, 2021, 2022])

    query4 = """SELECT State, Year, Quarter, District,MAX(Registered_users) AS Max_Reg
                    FROM map_user
                    WHERE Quarter = %s AND Year = %s
                    GROUP BY State, Year, Quarter, District;"""

    df = pd.read_sql(query4, con=engine, params=(Quarter, Year))

    st.write(df)

    st.bar_chart(df.set_index('State')['Max_Reg'])


# TOP USER PAGE

elif selected == "Top User":

    st.title("TOP USER")
    Quarter = st.selectbox("Select the quarter:", [1, 2, 3, 4])
    Year = st.selectbox("Select the year:", [2018, 2019, 2020, 2021, 2022])

    query6 = """SELECT State, Year, Quarter, MAX(Registered_users) AS Max_Registered_user
                    FROM top_user_dist
                    WHERE Quarter = %s AND Year = %s
                    GROUP BY State, Year;"""

    df = pd.read_sql(query6, con=engine, params=(Quarter, Year))

    st.write(df)

    st.bar_chart(df.set_index('State')['Max_Registered_user'])


# INSIGHTS PAGE

elif selected == "Queries":
    st.title("QUERIES")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District"]

    select = st.selectbox("Select the option", options)
    if select == "Top 10 states based on year and amount of transaction":
        mycursor.execute(
            "SELECT DISTINCT State, Year, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_trans_pin GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");

        df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Transaction_Year', 'Transaction_Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.line_chart(data=df.set_index('States')['Transaction_Amount'])

    elif select == "List 10 states based on type and amount of transaction":
        mycursor.execute(
            "SELECT DISTINCT State, SUM(Transaction_count) as Total FROM top_trans_pin GROUP BY State ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_transaction'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='State', y='Total_transaction', palette='coolwarm')
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('States')
            plt.ylabel('Total Transaction')
            st.pyplot(plt)

    elif select == "Top 5 Transaction_Type based on Transaction_Amount":
        mycursor.execute(
            "SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM agg_trans GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_Type', 'Transaction_Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.bar_chart(data=df, y="Transaction_Type", x="Transaction_Amount")

    elif select == "Top 10 Registered-users based on States and District":
        mycursor.execute(
            "SELECT DISTINCT State, District, SUM(Registered_users) AS Users FROM top_user_dist GROUP BY State, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'RegisteredUsers'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            fig = px.treemap(df, path=['State', 'District'], values='RegisteredUsers')
            st.plotly_chart(fig)

    elif select == "Top 10 Districts based on states and Count of transaction":
        mycursor.execute(
            "SELECT DISTINCT State,District,SUM(Transaction_count) AS Counts FROM top_trans_dist GROUP BY State,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Transaction_count'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            fig = px.sunburst(df, path=['State', 'District'], values='Transaction_count')
            fig.update_traces(textinfo='label+percent entry')
            fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
            st.plotly_chart(fig)

    elif select == "List 10 Districts based on states and amount of transaction":
        mycursor.execute(
            "SELECT DISTINCT State, year,SUM(Transaction_amount) AS Amount FROM agg_trans GROUP BY State, year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'year', 'Transaction_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='State', y='Transaction_amount', ci=None, estimator=min)
            plt.xlabel('State')
            plt.ylabel('Transaction Amount')
            plt.title('Least 10 Districts Based on States and Transaction Amount')
            plt.legend(title='District', loc='upper right')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(plt)

    elif select == "List 10 Transaction_Count based on Districts and states":
        mycursor.execute(
            "SELECT DISTINCT State, District, SUM(Transaction_count) AS Counts FROM map_trans GROUP BY State,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'District', 'Transaction_Count'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            plt.figure(figsize=(8, 8))
            plt.pie(df.groupby('States')['Transaction_Count'].sum(), labels=df['States'].unique(), autopct='%1.1f%%',
                    shadow=True)
            plt.title('Top 10 Transaction Counts Based on States')
            plt.tight_layout()
            st.pyplot(plt)

    elif select == "Top 10 RegisteredUsers based on states and District":
        mycursor.execute(
            "SELECT DISTINCT State,District, SUM(Registered_users) AS Users FROM map_user GROUP BY State,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'District', 'RegisteredUsers'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            # st.title("Top 10 RegisteredUsers based on states and District")
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x='States', y='RegisteredUsers', hue='District')
            plt.xlabel('States')
            plt.ylabel('Registered Users')
            plt.legend(title='District', loc='upper right')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(plt)
