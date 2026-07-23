import streamlit as st
import pandas as pd
import plotly.express as px


# 1. Page Configuration

st.set_page_config(
    page_title="Executive Workforce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. Data Loading & Caching

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("output/employee_cleaned_data.xlsx")
    except Exception:
        df = pd.DataFrame({
            "Department": ["IT", "HR", "Sales", "IT", "Sales", "HR"],
            "City": ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai", "Delhi"],
            "Salary": [85000, 62000, 75000, 95000, 71000, 68000],
            "Age": [29, 34, 26, 41, 31, 38],
            "Experience": [4, 8, 2, 14, 5, 9]
        })
    return df

df_raw = load_data()


# 3. Compact Sidebar Filters (No CSS, Single Screen Fit)

st.sidebar.title("🔍 Navigation & Filters")

# 1️⃣ View Selector Options
VIEW_OPTIONS = [
    "All Charts (Full Dashboard)",
    "Department Analysis",
    "Salary & Compensation",
    "Experience & Growth",
    "Avg Salary & Experience Matrix",
    "Age & Demographics",
    "Location & City Analysis"
]
chart_type = st.sidebar.selectbox("📊 Dashboard View", VIEW_OPTIONS)

# 2️⃣ Department Filter
departments = ["All"] + sorted(list(df_raw["Department"].dropna().unique()))
selected_dept = st.sidebar.selectbox("🏢 Department", departments)

# 3️⃣ City Filter
df_dept_filtered = df_raw if selected_dept == "All" else df_raw[df_raw["Department"] == selected_dept]
cities = ["All"] + sorted(list(df_dept_filtered["City"].dropna().unique()))
selected_city = st.sidebar.selectbox("📍 City", cities)

# 4️⃣ Sliders (Salary & Experience)
min_sal, max_sal = int(df_raw["Salary"].min()), int(df_raw["Salary"].max())
salary_range = st.sidebar.slider("💰 Salary Range", min_sal, max_sal, (min_sal, max_sal))

min_exp, max_exp = int(df_raw["Experience"].min()), int(df_raw["Experience"].max())
exp_range = st.sidebar.slider("📈 Experience (Years)", min_exp, max_exp, (min_exp, max_exp))

# Apply Data Filtering
filtered_df = df_raw.copy()

if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["Department"] == selected_dept]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

filtered_df = filtered_df[
    (filtered_df["Salary"] >= salary_range[0]) & (filtered_df["Salary"] <= salary_range[1]) &
    (filtered_df["Experience"] >= exp_range[0]) & (filtered_df["Experience"] <= exp_range[1])
]


# 4. Header & Executive KPIs

st.title("📊 Workforce Analytics & HR Intelligence Dashboard")
st.caption("Interactive enterprise analytics built for executive decision-making.")

st.markdown("---")

# KPI Calculations
total_emp = len(filtered_df)
avg_sal = filtered_df["Salary"].mean() if not filtered_df.empty else 0
avg_exp = filtered_df["Experience"].mean() if not filtered_df.empty else 0
total_payroll = filtered_df["Salary"].sum() if not filtered_df.empty else 0

total_emp_raw = len(df_raw)
avg_sal_raw = df_raw["Salary"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Employees",
        value=f"{total_emp:,}",
        delta=f"{total_emp - total_emp_raw} vs Overall" if selected_dept != "All" or selected_city != "All" else None
    )

with col2:
    st.metric(
        label="Average Salary",
        value=f"₹{avg_sal:,.0f}",
        delta=f"₹{avg_sal - avg_sal_raw:,.0f} vs Avg" if selected_dept != "All" or selected_city != "All" else None
    )

with col3:
    st.metric(
        label="Total Payroll Budget",
        value=f"₹{total_payroll:,.0f}"
    )

with col4:
    st.metric(
        label="Avg Experience",
        value=f"{avg_exp:.1f} Yrs"
    )

st.markdown("---")

if filtered_df.empty:
    st.error("⚠️ No employee records match the selected filter criteria. Please broaden your selection.")
    st.stop()


# 5. Executive Insight Box

top_dept = filtered_df.groupby("Department")["Salary"].mean().idxmax()
top_dept_sal = filtered_df.groupby("Department")["Salary"].mean().max()

st.info(
    f"💡 **Executive Insight:** The highest average salary is in the **{top_dept}** department "
    f"(Avg: **₹{top_dept_sal:,.0f}**). Filtered view currently represents "
    f"**{(total_emp/total_emp_raw)*100:.1f}%** of the total workforce."
)


# 6. Plotly Charts Functions

def chart_department_distribution(df):
    st.subheader("🏢 Department Workforce Share `[Donut Chart]`")
    dept_counts = df.groupby("Department").size().reset_index(name="Count")
    fig = px.pie(
        dept_counts, names="Department", values="Count", hole=0.45,
        color="Department", color_discrete_sequence=px.colors.qualitative.Set2,
        title="Department Share (%)"
    )
    fig.update_traces(textinfo="percent+label", pull=[0.02]*len(dept_counts))
    fig.update_layout(showlegend=False, title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

def chart_department_salary_treemap(df):
    st.subheader("🗺️ Total Payroll Share by Dept `[Treemap Chart]`")
    dept_salary = df.groupby("Department")["Salary"].sum().reset_index()
    fig = px.treemap(
        dept_salary, path=["Department"], values="Salary",
        color="Salary", color_continuous_scale="Viridis",
        title="Payroll Allocation Tree"
    )
    fig.update_layout(title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

def chart_salary_spread_violin(df):
    st.subheader("💰 Salary Range & Pay Distribution `[Violin Chart]`")
    fig = px.violin(
        df, x="Department", y="Salary", color="Department",
        box=True, points="all", color_discrete_sequence=px.colors.qualitative.Bold,
        title="Department-wise Salary Density"
    )
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Salary (₹)", title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

def chart_experience_vs_salary(df):
    st.subheader("📈 Experience vs Salary Growth Trend `[Bubble Scatter Chart]`")
    fig = px.scatter(
        df, x="Experience", y="Salary", color="Department",
        size="Age" if "Age" in df.columns else None,
        hover_data=["City"], color_discrete_sequence=px.colors.qualitative.Vivid,
        labels={"Experience": "Years of Experience", "Salary": "Current Salary (₹)"},
        title="Experience vs Salary Correlation"
    )
    fig.update_layout(title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

def chart_age_demographics(df):
    st.subheader("🎂 Employee Age Brackets `[Histogram]`")
    fig = px.histogram(
        df, x="Age", nbins=10, color="Department", barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        title="Age Group Breakdown"
    )
    fig.update_layout(title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

def chart_dept_exp_salary(df):
    st.subheader("📊 Avg Salary & Experience Matrix `[Grouped Bar Chart]`")
    agg_df = df.groupby("Department").agg({"Salary": "mean", "Experience": "mean"}).reset_index()
    fig = px.bar(
        agg_df, x="Department", y="Salary", color="Experience",
        text_auto=".2s", color_continuous_scale="Tealgrn",
        title="Avg Salary & Experience Depth per Department"
    )
    fig.update_layout(title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

def chart_city_headcount(df):
    st.subheader("📍 City-wise Employee Headcount `[Horizontal Bar Chart]`")
    city_df = df.groupby("City").size().reset_index(name="Headcount").sort_values("Headcount", ascending=True)
    fig = px.bar(
        city_df, y="City", x="Headcount", text="Headcount",
        color="Headcount", color_continuous_scale="Blues",
        orientation="h", title="Workforce Concentration by Location"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)


# Dynamic Chart Filtering Router

if chart_type == "All Charts (Full Dashboard)":
    c1, c2 = st.columns(2)
    with c1:
        chart_department_distribution(filtered_df)
    with c2:
        chart_department_salary_treemap(filtered_df)

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        chart_salary_spread_violin(filtered_df)
    with c4:
        chart_experience_vs_salary(filtered_df)

    st.markdown("---")
    c5, c6 = st.columns(2)
    with c5:
        chart_dept_exp_salary(filtered_df)
    with c6:
        chart_city_headcount(filtered_df)

    st.markdown("---")
    chart_age_demographics(filtered_df)

elif chart_type == "Department Analysis":
    c1, c2 = st.columns(2)
    with c1:
        chart_department_distribution(filtered_df)
    with c2:
        chart_department_salary_treemap(filtered_df)

elif chart_type == "Salary & Compensation":
    chart_salary_spread_violin(filtered_df)

elif chart_type == "Experience & Growth":
    chart_experience_vs_salary(filtered_df)

elif chart_type == "Avg Salary & Experience Matrix":
    chart_dept_exp_salary(filtered_df)

elif chart_type == "Age & Demographics":
    chart_age_demographics(filtered_df)

elif chart_type == "Location & City Analysis":
    chart_city_headcount(filtered_df)


# 7. Pivot Table & Master Data Table with Export

st.markdown("---")
st.subheader("📌 Executive Summary Pivot Table")
pivot = pd.pivot_table(
    filtered_df, index="Department", columns="City" if "City" in filtered_df.columns else None,
    values="Salary", aggfunc=["count", "mean", "sum"], fill_value=0
)
pivot.columns = [f"{agg.capitalize()} - {col}" for agg, col in pivot.columns]
st.dataframe(pivot, use_container_width=True)

st.markdown("---")
col_table, col_download = st.columns([3, 1])

with col_table:
    st.subheader("📋 Master Employee Data")

with col_download:
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Data (CSV)",
        data=csv_data,
        file_name="filtered_employee_data.csv",
        mime="text/csv",
        use_container_width=True
    )

# Safe Table Configuration (No Matplotlib Dependency)
st.dataframe(
    filtered_df,
    use_container_width=True,
    column_config={
        "Salary": st.column_config.NumberColumn("Salary", format="₹%d"),
        "Experience": st.column_config.NumberColumn("Experience (Yrs)", format="%d Yrs")
    }
)
