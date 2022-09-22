import streamlit as st  # 🎈 data web app development
import plotly.express as px  # interactive charts
import pandas as pd  # read csv, df manipulation
import numpy as np  # np mean, np random
import time  # to simulate a real time data, time loop
import plotly.graph_objects as go


# Importing Dependencies

from sqlalchemy import create_engine

rds_connection_string = "postgres:postgres@localhost:5432/Remi_db"
engine = create_engine(f'postgresql://{rds_connection_string}')
engine.table_names()


# testing the table after connecting to ensure connection worked
table = pd.read_sql_query('select * from final', con=engine)

st.set_page_config(
    page_title="Remi Designs Dashboard",
    page_icon="✅",
    layout="wide",
)
# dashboard title
st.title("Remi Designs Dashboard")

# top-level filters
collection_filter = st.selectbox(
    "Select the Collection", pd.unique(table['collection']))


# creating a single element container
placeholder = st.empty()

# dataframe filter
collection_table = table[table['collection'] == collection_filter]


# creating KPIs-- eventually will include expenses and profit

while True:
    revenue = collection_table.loc[collection_table['refunded']
                                   == 'not refunded', 'post discount price'].sum()
    print(revenue)

    # clothing_type = collection_table(['clothing_type']).count()
    # print(clothing_type)

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(label="Revenue ⏳", value=f"$ {(revenue)} ")
        kpi2.metric(label="Expenses 💍", value=0)
        kpi3.metric(label="Profit ＄", value=0)

        # create three columns for charts

        fig_col1, fig_col2 = st.columns([1, 1])
        with fig_col1:
            st.markdown("### Revenue over time")
            fig = px.histogram(data_frame=collection_table, width=700,
                               labels={"post discount price": "Revenue",
                                       "date": "Date"},

                               y='post discount price', x='date')
            fig.update_layout(yaxis_tickprefix='$')
            st.write(fig)

        with fig_col2:
            st.markdown("### Most popular items")
            fig2 = px.histogram(data_frame=collection_table, width=700,
                                labels={  # replaces default labels by column name
                                    "color": "Item Colour",  "post discount price": "Revenue", "item": "Item"
                                },
                                y='post discount price', x='item', color="colour",
                                color_discrete_map={
                                    "Brown": "brown",
                                    "Orange": "orange",
                                    "White": "yellow",
                                    "Blue": "blue",

                                })
            fig2.update_layout(yaxis_tickprefix='$')
            st.write(fig2)

        fig_col3, fig_col4, fig_col5 = st.columns([2, 2, 2])
        with fig_col3:
            st.markdown("### Payment Type")
            fig3 = px.data.tips()
            fig3 = px.pie(data_frame=collection_table, width=450,
                          values='quantity', names='payment method')

            st.write(fig3)

        with fig_col4:
            st.markdown("### Clothing Type")
            fig4 = px.data.tips()
            fig4 = px.pie(data_frame=collection_table, width=400,
                          values='quantity', names='clothing type')
            st.write(fig4)

        with fig_col5:
            st.markdown("### Size")
            fig5 = px.data.tips()
            fig5 = px.pie(data_frame=collection_table, width=400,
                          values='quantity', names='size')
            st.write(fig5)

        st.markdown("### Detailed Data View")
        st.dataframe(collection_table)
        time.sleep(1)
