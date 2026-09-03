import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

SCRIPT_DIR =os.path.dirname(os.path.abspath(__file__))
DATA_DIR=os.path.join(SCRIPT_DIR,"..","data_export")

st.set_page_config(page_title="Gold Price Analysis", layout="wide")
st.title("Gold Price Analysis")


#Load data
gold_inr = pd.read_csv(os.path.join(DATA_DIR,"gold_inr_derived.csv"), parse_dates=["date"])
duty = pd.read_csv(os.path.join(DATA_DIR,"import_duty.csv"), parse_dates=["effective_date"])


#Panel 1
st.header("Gold Price (INR per 10g) Over Time")


fig =go.Figure()
fig.add_trace(go.Scatter(
            x=gold_inr["date"], 
            y=gold_inr["gold_inr_per_10g_landed"],
            mode="lines",
              name="Gold Price (INR per 10g)"))

for i,(_, row) in enumerate(duty.iterrows()):
    fig.add_vline(
        x=row["effective_date"].timestamp()*1000,
          line_dash="dash", 
          line_color="gray", 
          opacity=0.5,
          annotation_text=f"Duty: {row['duty_pct']}%" if i==0 else f"{row['duty_pct']}%",
          annotation_position="top" if i%2==0 else "bottom",
          annotation_font_size=10,name="Import Duty Change")

fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode="lines",
    line=dict(color="gray", dash="dash"),
    name="Import duty change"
))
    
fig.update_layout(xaxis_title="Date", yaxis_title="INR per 10g", height=500)
st.plotly_chart(fig, use_container_width=True)

st.header("Comparing Trends: Gold (INR) vs Global Gold vs USD/INR")

compare_df = gold_inr[["date", "gold_inr_per_10g_landed", "gold_usd_oz", "usdinr_rate"]].dropna()

# Rebase each series so it starts at 100
compare_df["gold_inr_indexed"] = compare_df["gold_inr_per_10g_landed"] / compare_df["gold_inr_per_10g_landed"].iloc[0] * 100
compare_df["gold_usd_indexed"] = compare_df["gold_usd_oz"] / compare_df["gold_usd_oz"].iloc[0] * 100
compare_df["usdinr_indexed"] = compare_df["usdinr_rate"] / compare_df["usdinr_rate"].iloc[0] * 100

fig_compare = go.Figure()
fig_compare.add_trace(go.Scatter(x=compare_df["date"], y=compare_df["gold_inr_indexed"], name="Gold price (INR)"))
fig_compare.add_trace(go.Scatter(x=compare_df["date"], y=compare_df["gold_usd_indexed"], name="Gold price (USD)"))
fig_compare.add_trace(go.Scatter(x=compare_df["date"], y=compare_df["usdinr_indexed"], name="USD/INR rate"))
fig_compare.update_layout(
    xaxis_title="Date", yaxis_title="Indexed to 100 at start date",
    height=500
)

for i,(_, row) in enumerate(duty.iterrows()):
    fig_compare.add_vline(
        x=row["effective_date"].timestamp()*1000,
          line_dash="dash", 
          line_color="gray", 
          opacity=0.5,
          annotation_text=f"Duty: {row['duty_pct']}%" if i==0 else f"{row['duty_pct']}%",
          annotation_position="top" if i%2==0 else "bottom",
          annotation_font_size=10,name="Import Duty Change")

fig_compare.update_layout(
    xaxis_title="Date",
    yaxis_title="Indexed to 100 at start date (log scale)",
    yaxis_type="log",
    height=500
)
st.plotly_chart(fig_compare, use_container_width=True)
#panel 2
st.header("Factors Affecting Gold Price Changes")
decomposition = pd.read_csv(os.path.join(DATA_DIR,"decomposition.csv"), parse_dates=["date"])

min_date = decomposition["date"].min()
max_date = decomposition["date"].max()  
date_range=st.slider("Select Date Range",
                     min_value=min_date.to_pydatetime(),
                     max_value=max_date.to_pydatetime(),
                     value=(max_date.to_pydatetime() - pd.Timedelta(days=180), max_date.to_pydatetime()))


filtered= decomposition[(decomposition["date"]>=date_range[0]) & (decomposition["date"]<=date_range[1])]

fig2=go.Figure()
fig2.add_trace(go.Scatter(
               x=filtered["date"],y=filtered["gold_usd_change"],
               mode="lines",name="Global Gold Price Change (%)"))
fig2.add_trace(go.Scatter(
               x=filtered["date"],y=filtered["usdinr_change"],
               mode="lines",name="Currency (USD/INR) effect (%)", marker_color="red"))
fig2.add_trace(go.Scatter(
               x=filtered["date"],y=filtered["duty_change_pp"],
               mode="lines",name="Import Duty Effect (%)", marker_color="orange"))

fig2.update_layout(
    xaxis_title="Date",
    yaxis_title="Percentage Change (%)",
    height=500,
    barmode="overlay")

st.plotly_chart(fig2, use_container_width=True)

# Panel 3 

st.header("Trend and Volatility")

window_data=pd.read_csv(os.path.join(DATA_DIR,"window_function.csv"), parse_dates=["date"])

wf_min_date= window_data["date"].min()
wf_max_date= window_data["date"].max()

wf_date_range=st.slider("Select Date Range for Trend/Volatility View",
                        min_value=wf_min_date.to_pydatetime(),
                        max_value=wf_max_date.to_pydatetime(),
                        value=(wf_max_date.to_pydatetime() - pd.Timedelta(days=365*3), wf_max_date.to_pydatetime()),
                        key="window_slider")  

wf_filtered=window_data[(window_data["date"]>= wf_date_range[0])&(window_data["date"]<= wf_date_range[1])] 

col1, col2=st.columns(2)

with col1:
    fig3=go.Figure()
    fig3.add_trace(go.Scatter(
        x=wf_filtered["date"],y=wf_filtered["gold_inr_per_10g_landed"],
        mode="lines",name="Actual Gold Price (INR per 10g)",
        line=dict(width=1, color="lightgray")))
    fig3.add_trace(go.Scatter(
        x=wf_filtered["date"],y=wf_filtered["moving_avg_7d"],
        mode="lines",name="7 Day Moving Average"))
    fig3.add_trace(go.Scatter(
            x=wf_filtered["date"],y=wf_filtered["moving_avg_30d"],
            mode="lines",name="30 Day Moving Average"))
    fig3.update_layout(title="Price with Moving Averages",
                       xaxis_title="Date", yaxis_title="INR per 10g", height=400)
    st.plotly_chart(fig3, use_container_width=True)
              
with col2:
    fig3b=go.Figure()
    fig3b.add_trace(go.Scatter(
        x=wf_filtered["date"],y=wf_filtered["day_30_rolling_volatility"],
        mode="lines",name="30 day rolling volatility",
        line_color="darkred"))
    fig3b.update_layout(title="Rolling 30-Day Volatility",
                        xaxis_title="Date", yaxis_title="Std Dev of daily % change", height=400)
    st.plotly_chart(fig3b, use_container_width=True)    

#panel 4

st.header("Price Trends by Year and Month")

monthly=pd.read_csv(os.path.join(DATA_DIR,"monthly_aggregation.csv"))

yearly=monthly.groupby("yr").agg(
    avg_price=("avg_price","mean"),
    min_price=("min_price","min"),
    max_price=("max_price","max")
).reset_index()

fig4a=go.Figure()
fig4a.add_trace(go.Scatter(
    x=yearly["yr"],y=yearly["avg_price"],
    mode="lines+markers",name="Yearly avg price"))
fig4a.add_trace(go.Scatter(
    x=yearly["yr"],y=yearly["max_price"],
    mode="lines",name="Yearly max price",line=dict(dash="dot")))
fig4a.add_trace(go.Scatter(
    x=yearly["yr"],y=yearly["min_price"],
    mode="lines",name="Yearly min price",line=dict(dash="dot")))
fig4a.update_layout(xaxis_title="Year", yaxis_title="INR per 10g", height=450)

st.plotly_chart(fig4a,use_container_width=True)


st.subheader("Monthly Price Trends")
selected_year=st.selectbox("Select Year", sorted(monthly["yr"].unique(),reverse=True))
year_data=monthly[monthly["yr"]==selected_year].sort_values("mo")

fig4b=go.Figure()
fig4b.add_trace(go.Scatter(
    x=year_data["mo"],y=year_data["avg_price"],
    name="Avg Price"))
fig4b.add_trace(go.Scatter(
    x=year_data["mo"],y=year_data["max_price"],
    name="Max Price",mode="markers",marker_symbol="triangle-up"))
fig4b.add_trace(go.Scatter(
    x=year_data["mo"],y=year_data["min_price"],
    name="Min Price",mode="markers",marker_symbol="triangle-down"))

fig4b.update_layout(
    xaxis_title="Month", yaxis_title="INR per 10g",
    xaxis=dict(tickmode="array",tickvals=list(range(1,13))),
    height=450)
st.plotly_chart(fig4b, use_container_width=True)    