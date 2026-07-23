# 📊 Workforce Analytics & HR Intelligence Dashboard

An interactive enterprise-grade HR Analytics Dashboard built using **Python, Streamlit, Pandas, and Plotly**. This application enables executives and HR leaders to analyze workforce demographics, compensation structures, experience trends, and payroll allocations through dynamic multi-criteria filtering and interactive visualizations.

---

## ✨ Key Features

- **Executive KPI Cards**: Real-time tracking of Total Headcount, Average Salary, Total Payroll Budget, and Average Experience with dynamic benchmark deltas.
- **Global Cascading Filters**: Multi-criteria sidebar filters (Department, City, Salary Range, Experience Range) for granular data analysis.
- **7 Interactive Plotly Visualizations**:
  - 🏢 **Donut Chart**: Department Workforce Share (%)
  - 🗺️ **Treemap Chart**: Total Payroll Allocation by Department
  - 💰 **Violin Plot**: Salary Density & Pay Range Distribution
  - 📈 **Bubble Scatter Chart**: Experience vs. Salary Growth (Bubble size = Age)
  - 📊 **Grouped Bar Chart**: Average Salary & Experience Depth Matrix
  - 📍 **Horizontal Bar Chart**: City-wise Employee Headcount Concentration
  - 🎂 **Histogram**: Employee Age Group Demographics
- **Automated Executive Insights**: Real-time AI-like insight engine highlighting top-paying departments and workforce coverage.
- **Cross-Tabulation Pivot Table**: Executive matrix showing Headcount, Average Salary, and Total Expense across Departments and Locations.
- **Conditional Styled Data Table**: Heatmap-style formatting (`Pandas Styler`) highlighting min/max salary brackets.
- **Data Export**: One-click export functionality to download filtered views in CSV format.

---

## 🛠️ Tech Stack & Tools

- **Programming Language**: Python
- **Libraries**: Streamlit, Pandas, Plotly Express, OpenPyXL
- **Data Analysis**: Data Wrangling, Aggregations, Pivot Tables, Conditional Styling
- **Business Intelligence**: Custom Metric KPIs, Advanced Visualizations

---

## 🚀 How to Run the Project Locally

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/kapilverma/employee_data_analysis.git](https://github.com/kapilverma/employee_data_analysis.git)
   cd employee_data_analysis