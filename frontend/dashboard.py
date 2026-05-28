import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Database connection
engine = create_engine("sqlite:///./hostel_tickets.db")

# Load tickets
df = pd.read_sql("SELECT * FROM tickets", engine)

# Page config
st.set_page_config(
    page_title="AI Hostel Dashboard",
    layout="wide"
)

# Title
st.title("AI Hostel Complaint Analytics Dashboard")

# KPI Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", len(df))

high_priority = len(df[df["priority"] == "High"])

col2.metric("High Priority Tickets", high_priority)

most_common = (
    df["category"]
    .value_counts()
    .idxmax()
)

col3.metric(
    "Most Common Category",
    most_common
)

# Category Chart
st.subheader("Complaint Categories")

category_chart = px.bar(
    df["category"].value_counts(),
    labels={
        "value": "Count",
        "index": "Category"
    }
)

st.plotly_chart(category_chart)

# Priority Pie Chart
st.subheader("Priority Distribution")

priority_chart = px.pie(
    df,
    names="priority"
)

st.plotly_chart(priority_chart)

# Ticket Table
st.subheader("All Complaints")

st.dataframe(df)