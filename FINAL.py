# IMPORTING NECESSARY LIBRARIES

import pandas as pd
import json
import os
import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
import plotly.express as px

# PHONEPE PULSE CLONING

# !pip install gitpython
# !pip install git-clone
# !git-clone https://github.com/PhonePe/pulse.git  ----> By using this phonepe pulse will get cloned

# STREAMLIT PAGE CONFIGURATION

st.set_page_config(page_title="Phonepe Pulse Data Visualization ",
                   page_icon=":tada",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """YTH"""})

# STREAMLIT OPTION MENU

with st.sidebar:
    selected = option_menu(None, ['Home', "Top Charts", "Explore Data"],
                           icons=['house-door-fill', 'cloud-upload', 'tools',  'card-text'],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "25px", "text-align": "left", "margin": "10px",
                                                "--hover-color": "violet"},
                                   "icon": {"font-size": "20px"},
                                   "container": {"max-width": "2000px"},
                                   "nav-link-selected": {"background-color": "violet"}})


# AGGREGATED TRANSACTION

path_1 = r"C:\\Users\\MyPC/pulse/data/aggregated/transaction/country/india/state/"
Agg_Trans_list = os.listdir(path_1)

clm_1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in Agg_Trans_list:
    cur_state = os.path.join(path_1, state)

    # Check if the current state directory exists
    if os.path.exists(cur_state):
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = os.path.join(cur_state, year)
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = os.path.join(cur_year, file)
                data = open(cur_file, 'r')
                A = json.load(data)

                for i in A['data']['transactionData']:
                    name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']

                    # Appending to agg_trans_list
                    clm_1['Transaction_type'].append(name)
                    clm_1['Transaction_count'].append(count)
                    clm_1['Transaction_amount'].append(amount)
                    clm_1['State'].append(state)
                    clm_1['Year'].append(year)
                    clm_1['Quarter'].append(int(file.removesuffix('.json')))

    else:
        print(f"Directory '{cur_state}' not found.")

Agg_Trans = pd.DataFrame(clm_1)
# Agg_Trans

# AGGREGATED USER

path_2 = r"C:\\Users\\MyPC/pulse/data/aggregated/user/country/india/state/"
Agg_user_list = os.listdir(path_2)

clm_2 = {'State': [], 'Year': [], 'Quarter': [], 'Brand': [], 'Transaction_count': [], 'Percentage': []}

for state in Agg_user_list:
    cur_state = os.path.join(path_2, state)

    if os.path.exists(cur_state):
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = os.path.join(cur_state, year)
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = os.path.join(cur_year, file)

                with open(cur_file, 'r') as data:
                    B = json.load(data)
                    try:
                        for i in B["data"]["usersByDevice"]:
                            brand_name = i["brand"]
                            counts = i["count"]
                            percents = i["percentage"]

                            # Appending to agg_user_list
                            clm_2["Brand"].append(brand_name)
                            clm_2["Transaction_count"].append(counts)
                            clm_2["Percentage"].append(percents)
                            clm_2["State"].append(state)
                            clm_2["Year"].append(year)
                            clm_2["Quarter"].append(int(file.removesuffix('.json')))
                    except:
                        pass
    else:
        print(f"Directory '{cur_state}' not found.")

Agg_user = pd.DataFrame(clm_2)
# Agg_user

# MAP TRANSACTION

path_3 = r"C:\\Users\\MyPC/pulse/data/map/transaction/hover/country/india/state/"
Map_Trans_list = os.listdir(path_3)

clm_3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in Map_Trans_list:
    cur_state = os.path.join(path_3, state)

    # Check if the current state directory exists
    if os.path.exists(cur_state):
        map_year_list = os.listdir(cur_state)

        for year in map_year_list:
            cur_year = os.path.join(cur_state, year)
            map_file_list = os.listdir(cur_year)

            for file in map_file_list:
                cur_file = os.path.join(cur_year, file)
                data = open(cur_file, 'r')
                C = json.load(data)

                for i in C["data"]["hoverDataList"]:
                    district = i["name"]
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]

                    clm_3["District"].append(district.removesuffix(' district').title().replace(' And', ' and'))
                    clm_3["Transaction_count"].append(count)
                    clm_3["Transaction_amount"].append(amount)
                    clm_3['State'].append(state)
                    clm_3['Year'].append(year)
                    clm_3['Quarter'].append(int(file.removesuffix('.json')))
    else:
        print(f"Directory '{cur_state}' not found.")

Map_Trans = pd.DataFrame(clm_3)
# Map_Trans

# MAP USER

path_4 = r"C:\\Users\\MyPC/pulse/data/map/user/hover/country/india/state/"
Map_User_list = os.listdir(path_4)

clm_4 = {"State": [], "Year": [], "Quarter": [], "District": [], "Registered_users": [], "App_opens": []}

for state in Map_User_list:
    cur_state = os.path.join(path_4, state)
    map_year_list = os.listdir(cur_state)

    for year in map_year_list:
        cur_year = os.path.join(cur_state, year)
        map_file_list = os.listdir(cur_year)

        for file in map_file_list:
            cur_file = os.path.join(cur_year, file)
            data = open(cur_file, 'r')
            D = json.load(data)

            for i in D["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appOpens = i[1]['appOpens']

                # Appending to map_user_dict
                clm_4["District"].append(district.removesuffix(' district').title().replace(' And', ' and'))
                clm_4["Registered_users"].append(registereduser)
                clm_4["App_opens"].append(appOpens)
                clm_4['State'].append(state)
                clm_4['Year'].append(year)
                clm_4['Quarter'].append(int(file.strip('.json')))

Map_User = pd.DataFrame(clm_4)
# Map_User

# TOP TRANSACTION DISTRICT

path_5 = r"C:\\Users\\MyPC/pulse/data/top/transaction/country/india/state/"

Top_Trans_Dist_list = os.listdir(path_5)

clm_5 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in Top_Trans_Dist_list:
    cur_state = os.path.join(path_5, state)
    top_year_list = os.listdir(cur_state)

    for year in top_year_list:
        cur_year = os.path.join(cur_state, year)
        top_file_list = os.listdir(cur_year)

        for file in top_file_list:
            cur_file = os.path.join(cur_year, file)
            data = open(cur_file, 'r')
            E = json.load(data)

            for i in E['data']['districts']:
                name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']

                # Appending to top_trans_dist_dict

                clm_5['Transaction_count'].append(count)
                clm_5['Transaction_amount'].append(amount)
                clm_5['State'].append(state)
                clm_5['Year'].append(year)
                clm_5['Quarter'].append(int(file.removesuffix('.json')))
                clm_5['District'].append(name.title().replace(' And', ' and'))

Top_Trans_Dist = pd.DataFrame(clm_5)
# Top_Trans_Dist

# TOP TRANSACTION PINCODE

path_6 = r"C:\\Users\\MyPC/pulse/data/top/transaction/country/india/state/"

Top_Trans_Pincode_list = os.listdir(path_6)

clm_6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in Top_Trans_Pincode_list:
    cur_state = os.path.join(path_6, state)
    top_year_list = os.listdir(cur_state)

    for year in top_year_list:
        cur_year = os.path.join(cur_state, year)
        top_file_list = os.listdir(cur_year)

        for file in top_file_list:
            cur_file = os.path.join(cur_year, file)
            data = open(cur_file, 'r')
            F = json.load(data)

            for i in F['data']['pincodes']:
                name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']

                # Appending to top_trans_pin_dict

                clm_6['Pincode'].append(name)
                clm_6['Transaction_count'].append(count)
                clm_6['Transaction_amount'].append(amount)
                clm_6['State'].append(state)
                clm_6['Year'].append(year)
                clm_6['Quarter'].append(int(file.removesuffix('.json')))

Top_Trans_Pincode = pd.DataFrame(clm_6)
# Top_Trans_Pincode

# TOP USER DISTRICT

path_7 = r"C:\\Users\\MyPC/pulse/data/top/user/country/india/state/"
Top_User_Dist_list = os.listdir(path_7)

clm_7 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Registered_users': []}

for state in Top_User_Dist_list:
    cur_state = os.path.join(path_7, state)
    top_year_list = os.listdir(cur_state)

    for year in top_year_list:
        cur_year = os.path.join(cur_state, year)
        top_file_list = os.listdir(cur_year)

        for file in top_file_list:
            cur_file = os.path.join(cur_year, file)
            data = open(cur_file, 'r')
            G = json.load(data)

            for i in G['data']['districts']:
                name = i['name']
                registeredUsers = i['registeredUsers']

                clm_7['District'].append(name.title().replace(' And', ' and'))
                clm_7['Registered_users'].append(registeredUsers)
                clm_7['State'].append(state)
                clm_7['Year'].append(year)
                clm_7['Quarter'].append(int(file.removesuffix('.json')))

Top_User_Dist = pd.DataFrame(clm_7)
# Top_User_Dist

# TOP USER PINCODE

path_8 = r"C:\\Users\\MyPC/pulse/data/top/user/country/india/state/"
Top_User_Pincode_list = os.listdir(path_8)

clm_8 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Registered_users': []}

for state in Top_User_Pincode_list:
    cur_state = os.path.join(path_8, state)
    top_year_list = os.listdir(cur_state)

    for year in top_year_list:
        cur_year = os.path.join (cur_state, year)
        top_file_list = os.listdir(cur_year)

        for file in top_file_list:
            cur_file = os.path.join(cur_year, file)
            data = open(cur_file, 'r')
            H = json.load(data)

            for i in H['data']['pincodes']:
                name = i['name']
                registeredUsers = i['registeredUsers']

                # Appending to top_user_pin_dict
                clm_8['Pincode'].append(name)
                clm_8['Registered_users'].append(registeredUsers)
                clm_8['State'].append(state)
                clm_8['Year'].append(year)
                clm_8['Quarter'].append(int(file.removesuffix('.json')))

Top_User_Pincode = pd.DataFrame(clm_8)
# Top_User_Pincode

# DROPPING DUPLICATES

ATD = Agg_Trans.drop_duplicates()

AUD = Agg_user.drop_duplicates()

MTD = Map_Trans.drop_duplicates()

MUD = Map_User.drop_duplicates()

TTDD = Top_Trans_Dist.drop_duplicates()

TTPD = Top_Trans_Pincode.drop_duplicates()

TUDD = Top_User_Dist.drop_duplicates()

TUPD = Top_User_Pincode.drop_duplicates()

# NULL VALUE COUNTING

NULL_1 = ATD.isnull().sum()
# print(NULL_1)
# print(ATD.shape)
# print("\n\n")

NULL_2 = AUD.isnull().sum()
# print(NULL_2)
# print(AUD.shape)
# print("\n\n")

NULL_3 = MTD.isnull().sum()
# print(NULL_3)
# print(MTD.shape)
# print("\n\n")

NULL_4 = MUD.isnull().sum()
# print(NULL_4)
# print(MUD.shape)
# print("\n\n")

NULL_5 = TTDD.isnull().sum()
# print(NULL_5)
# print(TTDD.shape)
# print("\n\n")

NULL_6 = TTPD.isnull().sum()
# print(NULL_6)
# print(TTPD.shape)
# print("\n\n")

NULL_7 = TUDD.isnull().sum()
# print(NULL_7)
# print(TUDD.shape)
# print("\n\n")

N8 = TUPD.isnull().sum()
# print(N8)
# print(TUPD.shape)
# print("\n\n")

# TRANSFORMING TO CSV FILES

ATD.to_csv("AGG_TRANS.CSV", index=False)

AUD.to_csv("AGG_USER.CSV", index=False)

MTD.to_csv("MAP_TRANS.CSV", index=False)

MUD.to_csv("MAP_USER.CSV", index=False)

TTDD.to_csv("TOP_TRANS_DIST.CSV", index=False)

TTPD.to_csv("TOP_TRANS_PINCODE.CSV", index=False)

TUDD.to_csv("TOP_USER_DIST.CSV", index=False)

TUPD.to_csv("TOP_USER_PINCODE.CSV", index=False)

# SQL CONNECTION

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            auth_plugin='mysql_native_password'
            )
mycursor = mydb.cursor()
mycursor.execute("USE phonepe_pulse")

# CREATING TABLES
# TABLE FOR AGGREGATED TRANSACTION

mycursor.execute("CREATE TABLE IF NOT EXISTS agg_trans (State VARCHAR(255),Year YEAR,Quarter INTEGER,Transaction_type VARCHAR(255),Transaction_count INTEGER,Transaction_amount FLOAT)")

for i, row in Agg_Trans.iterrows():
    sql = 'insert into agg_trans values(%s,%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR AGGREGATED USER

mycursor.execute("CREATE TABLE IF NOT EXISTS agg_user (State VARCHAR(255),Year YEAR,Quarter INTEGER,Brand VARCHAR(255),Transaction_count INTEGER,Percentage FLOAT)")

for i, row in Agg_user.iterrows():
    sql = 'insert into agg_user values(%s,%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR MAP TRANSACTION

mycursor.execute("CREATE TABLE IF NOT EXISTS map_trans (State VARCHAR(255),Year YEAR,Quarter INTEGER,District VARCHAR(255),Transaction_count INTEGER,Transaction_amount FLOAT)")

for i, row in Map_Trans.iterrows():
    sql = 'insert into map_trans values(%s,%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR MAP USER

mycursor.execute("CREATE TABLE IF NOT EXISTS map_user (State VARCHAR(255),Year YEAR,Quarter INTEGER,District VARCHAR(255),Registered_users INTEGER,App_opens INTEGER)")

for i, row in Map_User.iterrows():
    sql = 'insert into map_user values(%s,%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR TOP TRANSACTION DISTRICT

mycursor.execute("CREATE TABLE IF NOT EXISTS top_trans_dist (State VARCHAR(255),Year YEAR,Quarter INTEGER,District VARCHAR(255),Transaction_count INTEGER,Transaction_amount FLOAT)")

for i, row in Top_Trans_Dist.iterrows():
    sql = 'insert into top_trans_dist values(%s,%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR TOP TRANSACTION PINCODE

mycursor.execute("CREATE TABLE IF NOT EXISTS top_trans_pin (State VARCHAR(255),Year YEAR,Quarter INTEGER,Pincode VARCHAR(255),Transaction_count INTEGER,Transaction_amount FLOAT)")

for i, row in Top_Trans_Pincode.iterrows():
    sql = 'insert into top_trans_pin values(%s,%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR TOP USER DISTRICT

mycursor.execute("CREATE TABLE IF NOT EXISTS top_user_dist (State VARCHAR(255),Year YEAR,Quarter INTEGER,District VARCHAR(255),Registered_users INTEGER)")

for i, row in Top_User_Dist.iterrows():
    sql = 'insert into top_user_dist values(%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# TABLE FOR TOP USER PINCODE

mycursor.execute("CREATE TABLE IF NOT EXISTS top_user_pin (State VARCHAR(255),Year YEAR,Quarter INTEGER,Pincode VARCHAR(255),Registered_users INTEGER)")

for i, row in Top_User_Pincode.iterrows():
    sql = 'insert into top_user_pin values(%s,%s,%s,%s,%s)'
    mycursor.execute(sql, tuple(row))
    mydb.commit()

# STREAMLIT PAGE

# HOME PAGE

if selected == "Home":
    with st.container():
        st.title(":violet[Project]: Phonepe Pulse Data Visualization:")
    with st.container():
        st.write(""":violet[Statement]: Streamlit application that allows users to access
         and analyze data of Phonepe App.""")
    with st.container():
        st.write(""":violet[Technologies Use]: Github Cloning, Python, Pandas, MySQL-mysql-connector-python,
         Streamlit,Plotly.""")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header(":violet[PhonePe] :")
            st.write("##")
            st.write(""""  .""")
        with right_column:
            video_file = open('C:\Users\MyPC\Downloads\phonepe.mp4', 'rb')
            video_bytes = video_file.read()

            st.video(video_bytes)

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1, 1.5], gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
            """
            #### From this menu we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """, icon="🔍"
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(
                f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(
                f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(
                f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    if Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(
                    f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(
                f"select district, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(
                f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(
                f"select state, sum(Registereduser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Appopens'],
                         labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(
                f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(
                r'C:\Users\samue\Downloads\bus attrocates\Phonepe_Pulse_Data_Visualization-main\Phonepe_Pulse_Data_Visualization\Data\Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(
                f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(
                r'C:\Users\samue\Downloads\bus attrocates\Phonepe_Pulse_Data_Visualization-main\Phonepe_Pulse_Data_Visualization\Data\Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(
            f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=False)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        mycursor.execute(
            f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")

        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                         'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    # EXPLORE DATA - USERS
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(
            f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df2 = pd.read_csv(
            r'C:\Users\samue\Downloads\bus attrocates\Phonepe_Pulse_Data_Visualization-main\Phonepe_Pulse_Data_Visualization\Data\Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        mycursor.execute(
            f"select State,year,quarter,District,sum(Registereduser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")

        df = pd.DataFrame(mycursor.fetchall(),
                          columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

