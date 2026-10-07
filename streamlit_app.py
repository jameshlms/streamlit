import pandas as pd
import streamlit as st

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(
    df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f"
)

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=["Sales"]).groupby(pd.Grouper(freq="ME")).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1)
selected_category = st.selectbox("Category", df["Category"].unique())

# (2)
subcats_in_category = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_subcats = st.multiselect(
    "Sub_Category", subcats_in_category, default=subcats_in_category
)

if selected_subcats:
    filtered = df[df["Sub_Category"].isin(selected_subcats)]

    # (3)
    sales_by_month_filtered = (
        filtered.filter(items=["Sales"]).groupby(pd.Grouper(freq="ME")).sum()
    )
    st.line_chart(sales_by_month_filtered, y="Sales")

    # (4) & (5)
    total_sales = filtered["Sales"].sum()
    total_profit = filtered["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100

    overall_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric(
        "Profit Margin (%)",
        f"{profit_margin:.2f}%",
        delta=f"{profit_margin - overall_margin:.2f}%",
    )
