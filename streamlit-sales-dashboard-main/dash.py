import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_from_csv():
    df = pd.read_csv('C:\\Users\\SAHIL\\Downloads\\streamlit-sales-dashboard-main\\streamlit-sales-dashboard-main\\log(2).csv')
    df.columns = ["Timestamp","User","Log_Message","Severity","IP_Address","HTTP_Status_Code","Response_Time_ms"]
    severity_mapping = {'INFO': 1, 'WARNING': 2, 'ERROR': 3}
    df['Severity'] = df['Severity'].map(severity_mapping)
    return df

df = get_data_from_csv()

st.sidebar.header("Please Filter Here:")
user = st.sidebar.multiselect(
    "Select the User:",
    options=df["User"].unique(),
    default=df["User"].unique()
)

severity = st.sidebar.multiselect(
    "Select the Severity:",
    options=df["Severity"].unique(),
    default=df["Severity"].unique(),
)

http_status_code = st.sidebar.multiselect(
    "Select the HTTP Status Code:",
    options=df["HTTP_Status_Code"].unique(),
    default=df["HTTP_Status_Code"].unique()
)

df_selection = df.query(
    "User == @user & Severity == @severity & HTTP_Status_Code == @http_status_code"
)

if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

st.title(":bar_chart: Dashboard")
st.markdown("##")

total_response_time = int(df_selection["Response_Time_ms"].sum())
average_severity = round(df_selection["Severity"].mean(), 1)
average_response_time = round(df_selection["Response_Time_ms"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Response Time:")
    st.subheader(f"{total_response_time} ms")
with middle_column:
    st.subheader("Average Severity:")
    st.subheader(f"{average_severity}")
with right_column:
    st.subheader("Average Response Time Per Transaction:")
    st.subheader(f"{average_response_time} ms")

st.markdown("""---""")

response_time_by_user = df_selection.groupby(by=["User"])[["Response_Time_ms"]].sum().sort_values(by="Response_Time_ms")
fig_user_response_time = px.bar(
    response_time_by_user,
    x="Response_Time_ms",
    y=response_time_by_user.index,
    orientation="h",
    title="<b>Response Time by User</b>",
    color_discrete_sequence=["#0083B8"] * len(response_time_by_user),
    template="plotly_white",
)
fig_user_response_time.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

response_time_by_severity = df_selection.groupby(by=["Severity"])[["Response_Time_ms"]].sum()
fig_severity_response_time = px.bar(
    response_time_by_severity,
    x=response_time_by_severity.index,
    y="Response_Time_ms",
    title="<b>Response Time by Severity</b>",
    color_discrete_sequence=["#0083B8"] * len(response_time_by_severity),
    template="plotly_white",
)
fig_severity_response_time.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_severity_response_time, use_container_width=True)
right_column.plotly_chart(fig_user_response_time, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
