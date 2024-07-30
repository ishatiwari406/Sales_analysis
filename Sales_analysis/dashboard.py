import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt


st.set_page_config(page_title= "Sales Data Analysis", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sales Data Analysis")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True) # heading to be displayed at littlt more on the top
df = pd.read_excel("Sample - Superstore.xls")

col1,col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting minimum and maximum date

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date",startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date",endDate))
    
df = df[(df["Order Date"]>= date1) & (df["Order Date"]<= date2)].copy()

# Creating filter for Region
st.sidebar.header("Choose your filter:")
region = st.sidebar.multiselect("Pick your Region",df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]
 
# Creating filter for State
state = st.sidebar.multiselect("Pick your State",df["State"].unique())
if not region:
    df3 = df.copy()
else:
    df3 = df[df["Region"].isin(state)]

# Creating filter for City
city = st.sidebar.multiselect("Pick your City",df["City"].unique())    

# Filter the data based on Region, State and City (applying permutation and combination)

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not state:
    filtered_df = df[df["City"].isin(city)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df["State"].isin(state)]   
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Column chart and pie chart
category_df = filtered_df.groupby(by= ["Category"], as_index=False)["Sales"].sum()
with col1:
    st.subheader("Category Wise Sales")
    fig = px.bar(category_df, x= "Category", y= "Sales", text= ['${:,.2f}'.format(x) for x in category_df["Sales"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=100)
with col2:
    st.subheader("Region Wise Sales")
    fig = px.pie(filtered_df, values="Sales",names="Region", hole=0.5)   
    fig.update_traces(text=filtered_df["Region"],textposition = "outside")
    st.plotly_chart(fig, use_container_width=True) 
filtered_df["month-year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

# Time Series Analysis
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month-year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x= "month-year", y= "Sales", labels= {"Sales : Amount"}, height=500, width= 1000)
st.plotly_chart(fig2, use_container_width=True)
with st.expander("View Data of Time Series: "):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv= linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data=csv, file_name="Timeseries_analysis.csv", mime="txt/csv")
    
# Creating Segment-wise and Category-wise Sales pie-chart
chart1, chart2 = st.columns(2)
with chart1:
    st.subheader("Segment Wise Sales")
    fig= px.pie(filtered_df, values= "Sales", names="Segment")
    fig.update_traces(text= filtered_df["Segment"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
with chart2:
    st.subheader("Category Wise Sales")
    fig= px.pie(filtered_df, values= "Sales", names="Category")
    fig.update_traces(text= filtered_df["Category"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
    
# Creating Scatter plot
st.subheader("Relationship between Sales and Profit using Scatter Plot")
data1=px.scatter(filtered_df, x= "Sales", y= "Profit", size= "Quantity")
st.plotly_chart(data1, use_container_width=True)