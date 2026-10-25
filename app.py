
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Student Dashboard", layout="wide")

# Create student dataset
df = pd.DataFrame({
    "Student": ["Ritesh", "Asha", "Rahul", "Priya", "Arun",
                "Neha", "Vijay", "Kavi", "Riya", "Ajay"],
    "Department": ["IT", "CS", "IT", "CS", "IT",
                   "CS", "IT", "CS", "IT", "CS"],
    "Maths": [85, 72, 90, 65, 78, 55, 88, 92, 60, 81],
    "Python": [90, 75, 95, 70, 82, 60, 91, 89, 65, 85],
    "English": [78, 80, 88, 75, 85, 58, 90, 94, 70, 79]
})

df["Total"] = df[["Maths", "Python", "English"]].sum(axis=1)
df["Percentage"] = (df["Total"] / 3).round(2)
df["Result"] = df["Percentage"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)

# Save Excel dataset
df.to_excel("student_data.xlsx", index=False)

st.title("Student Performance Analysis Dashboard")
st.write("Analyze student marks and academic performance.")

# Department filter
st.sidebar.header("Dashboard Filters")
departments = st.sidebar.multiselect(
    "Select Department",
    options=df["Department"].unique(),
    default=list(df["Department"].unique())
)

data = df[df["Department"].isin(departments)]

# Statistics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", len(data))
c2.metric("Average Percentage",
          f"{data['Percentage'].mean():.1f}%" if len(data) else "0%")
c3.metric("Highest Percentage",
          f"{data['Percentage'].max():.1f}%" if len(data) else "0%")
c4.metric("Students Passed",
          int((data["Result"] == "Pass").sum()))

st.divider()

# Subject marks chart
long_data = data.melt(
    id_vars=["Student"],
    value_vars=["Maths", "Python", "English"],
    var_name="Subject",
    value_name="Marks"
)

fig1 = px.bar(
    long_data, x="Student", y="Marks",
    color="Subject", barmode="group",
    title="Student Marks by Subject"
)
st.plotly_chart(fig1, use_container_width=True)

# Department chart
dept = data.groupby("Department", as_index=False)["Percentage"].mean()
fig2 = px.bar(
    dept, x="Department", y="Percentage",
    title="Average Percentage by Department"
)
st.plotly_chart(fig2, use_container_width=True)

# Excel dataset table
st.subheader("Student Dataset")
st.dataframe(data, use_container_width=True)

st.download_button(
    "Download Student Data as CSV",
    data=data.to_csv(index=False),
    file_name="student_data.csv",
    mime="text/csv"
)
