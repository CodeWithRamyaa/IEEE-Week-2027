import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Social Media Research Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 2. DASHBOARD TITLE
# =====================================================

st.title("📊 Social Media Usage and Academic Performance")

st.markdown(
    """
    ### Research Dashboard

    An Analytical Study of Social Media Usage Patterns
    and Their Influence on Academic Performance Among College Students.
    """
)

st.markdown("---")

# =====================================================
# 3. DATASET UPLOAD
# =====================================================

st.sidebar.title("Dataset Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload Research Dataset (CSV)",
    type=["csv"]
)

required_columns = [
    "Daily_Usage_Hours",
    "Platform",
    "Main_Purpose",
    "Study_Hours",
    "Academic_Impact"
]

# Load uploaded or demonstration dataset

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
        data_source = "Uploaded Dataset"

    except Exception:
        st.error("Unable to read the uploaded CSV file.")
        st.stop()

else:

    try:
        df = pd.read_csv("sample_data.csv")
        data_source = "Demonstration Dataset"

    except FileNotFoundError:
        st.error("sample_data.csv was not found in the Prototype folder.")
        st.stop()

# =====================================================
# 4. DATA VALIDATION
# =====================================================

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"The dataset is missing these columns: {missing_columns}"
    )

    st.info(
        "Required columns: " + ", ".join(required_columns)
    )

    st.stop()

original_count = len(df)

# Clean numerical columns

numeric_columns = [
    "Daily_Usage_Hours",
    "Study_Hours"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# Remove missing values and blank categories

for col in ["Platform", "Main_Purpose", "Academic_Impact"]:

    df[col] = df[col].astype("string").str.strip()

    df[col] = df[col].replace("", pd.NA)

df = df.dropna(subset=required_columns)

# Validate hour values

valid_hours = (
    df["Daily_Usage_Hours"].between(0, 24) &
    df["Study_Hours"].between(0, 24)
)

df = df[valid_hours].copy()

removed_records = original_count - len(df)

if df.empty:

    st.error(
        "No valid records are available for analysis. "
        "Please upload a valid dataset."
    )

    st.stop()

# =====================================================
# 5. DATA SOURCE NOTICE
# =====================================================

if data_source == "Demonstration Dataset":

    st.warning(
        "You are viewing fictional demonstration data. "
        "These records are not actual research responses "
        "and must not be presented as research findings."
    )

else:

    st.success(
        "Uploaded dataset loaded and validated successfully."
    )

st.caption(f"Data source: {data_source}")

if removed_records > 0:

    st.info(
        f"{removed_records} invalid or incomplete records "
        "were removed during data cleaning."
    )

st.markdown("---")

# =====================================================
# 6. DATASET INFORMATION
# =====================================================

st.header("1. Dataset Information")

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Total Valid Records",
    len(df)
)

info_col2.metric(
    "Total Platforms",
    df["Platform"].nunique()
)

info_col3.metric(
    "Usage Purposes",
    df["Main_Purpose"].nunique()
)

with st.expander("View Dataset Details"):

    st.write("Dataset Columns:")

    st.write(list(df.columns))

    st.write("Dataset Shape:")

    st.write(df.shape)

    st.write("First Five Records:")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# 7. INTERACTIVE FILTERS
# =====================================================

st.sidebar.header("Dashboard Filters")

platform_options = sorted(
    df["Platform"].unique().tolist()
)

purpose_options = sorted(
    df["Main_Purpose"].unique().tolist()
)

selected_platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=platform_options,
    default=platform_options
)

selected_purposes = st.sidebar.multiselect(
    "Select Usage Purpose",
    options=purpose_options,
    default=purpose_options
)

filtered_df = df[
    (df["Platform"].isin(selected_platforms)) &
    (df["Main_Purpose"].isin(selected_purposes))
].copy()

# =====================================================
# 8. DASHBOARD OVERVIEW
# =====================================================

st.header("2. Dashboard Overview")

if filtered_df.empty:

    st.info(
        "No records match your selected filters. "
        "Please select at least one platform and purpose."
    )

    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Students",
    len(filtered_df)
)

col2.metric(
    "Average Daily Usage",
    f"{filtered_df['Daily_Usage_Hours'].mean():.2f} hours"
)

col3.metric(
    "Average Study Hours",
    f"{filtered_df['Study_Hours'].mean():.2f} hours"
)

st.markdown("---")

# =====================================================
# 9. SOCIAL MEDIA PLATFORM ANALYSIS
# =====================================================

st.header("3. Social Media Platform Analysis")

platform_counts = filtered_df["Platform"].value_counts()

fig, ax = plt.subplots(figsize=(8, 4))

platform_counts.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Social Media Platforms")
ax.set_ylabel("Number of Students")
ax.set_title("Popular Social Media Platforms")

plt.xticks(rotation=30)

st.pyplot(fig)
plt.close(fig)

st.write(
    f"Most commonly reported platform: **{platform_counts.idxmax()}**"
)

st.markdown("---")

# =====================================================
# 10. SOCIAL MEDIA USAGE PURPOSE
# =====================================================

st.header("4. Social Media Usage Purpose")

purpose_counts = filtered_df["Main_Purpose"].value_counts()

fig, ax = plt.subplots(figsize=(7, 5))

purpose_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")
ax.set_title("Purpose of Social Media Usage")

st.pyplot(fig)
plt.close(fig)

st.markdown("---")

# =====================================================
# 11. DAILY USAGE ANALYSIS
# =====================================================

st.header("5. Daily Social Media Usage Analysis")

fig, ax = plt.subplots(figsize=(8, 4))

filtered_df["Daily_Usage_Hours"].plot(
    kind="hist",
    bins=8,
    edgecolor="black",
    ax=ax
)

ax.set_xlabel("Daily Usage Hours")
ax.set_ylabel("Number of Students")
ax.set_title("Distribution of Daily Social Media Usage")

st.pyplot(fig)
plt.close(fig)

st.markdown("---")

# =====================================================
# 12. ACADEMIC IMPACT ANALYSIS
# =====================================================

st.header("6. Academic Impact Analysis")

impact_counts = filtered_df["Academic_Impact"].value_counts()

fig, ax = plt.subplots(figsize=(8, 4))

impact_counts.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Self-Reported Academic Impact")
ax.set_ylabel("Number of Students")
ax.set_title("Reported Academic Impact")

plt.xticks(rotation=0)

st.pyplot(fig)
plt.close(fig)

st.markdown("---")

# =====================================================
# 13. STUDY HOURS ANALYSIS
# =====================================================

st.header("7. Study Hours Analysis")

average_study_hours = (
    filtered_df.groupby("Platform")["Study_Hours"].mean()
)

fig, ax = plt.subplots(figsize=(8, 4))

average_study_hours.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Social Media Platform")
ax.set_ylabel("Average Study Hours")
ax.set_title("Average Study Hours by Platform")

plt.xticks(rotation=30)

st.pyplot(fig)
plt.close(fig)

st.markdown("---")

# =====================================================
# 14. USAGE VS STUDY HOURS
# =====================================================

st.header("8. Social Media Usage vs Study Hours")

fig, ax = plt.subplots(figsize=(8, 5))

ax.scatter(
    filtered_df["Daily_Usage_Hours"],
    filtered_df["Study_Hours"]
)

ax.set_xlabel("Daily Social Media Usage (Hours)")
ax.set_ylabel("Daily Study Hours")

ax.set_title(
    "Relationship Between Social Media Usage and Study Hours"
)

st.pyplot(fig)
plt.close(fig)

# =====================================================
# 15. CORRELATION ANALYSIS
# =====================================================

st.header("9. Correlation Analysis")

correlation = filtered_df[
    ["Daily_Usage_Hours", "Study_Hours"]
].corr().iloc[0, 1]

if pd.isna(correlation):

    st.info(
        "Correlation cannot be calculated because "
        "the selected data has insufficient variation."
    )

else:

    st.metric(
        "Correlation Coefficient",
        f"{correlation:.3f}"
    )

    if correlation > 0:

        st.write(
            "The selected data shows a positive linear association."
        )

    elif correlation < 0:

        st.write(
            "The selected data shows a negative linear association."
        )

    else:

        st.write(
            "The selected data shows no linear association."
        )

st.caption(
    "Correlation indicates association, not proof of cause and effect."
)

st.markdown("---")

# =====================================================
# 16. SUMMARY OF SELECTED DATA
# =====================================================

st.header("10. Research Summary")

average_usage = filtered_df["Daily_Usage_Hours"].mean()

average_study = filtered_df["Study_Hours"].mean()

most_used_platform = filtered_df["Platform"].mode().iloc[0]

most_common_purpose = filtered_df["Main_Purpose"].mode().iloc[0]

st.write(
    f"""
    - Number of valid student records: **{len(filtered_df)}**
    - Average daily social media usage: **{average_usage:.2f} hours**
    - Average daily study hours: **{average_study:.2f} hours**
    - Most commonly reported platform: **{most_used_platform}**
    - Most common usage purpose: **{most_common_purpose}**
    """
)

st.markdown("---")

# =====================================================
# 17. FILTERED DATASET
# =====================================================

st.header("11. Filtered Research Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================================
# 18. DOWNLOAD RESEARCH DATA
# =====================================================

st.header("12. Download Research Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Research Dataset (CSV)",
    data=csv_data,
    file_name="social_media_research_data.csv",
    mime="text/csv"
)

# =====================================================
# 19. DOWNLOAD RESEARCH SUMMARY REPORT
# =====================================================

report = f"""
SOCIAL MEDIA RESEARCH SUMMARY REPORT

Research Title:
An Analytical Study of Social Media Usage Patterns
and Their Influence on Academic Performance Among College Students.

Data Source: {data_source}

Total Valid Student Records: {len(filtered_df)}

Average Daily Social Media Usage:
{average_usage:.2f} hours

Average Daily Study Hours:
{average_study:.2f} hours

Most Commonly Reported Platform:
{most_used_platform}

Most Common Usage Purpose:
{most_common_purpose}

Correlation Coefficient:
{correlation:.3f}

Note:
This report is generated from the currently selected dataset.
Correlation does not establish causation.

If the dataset is fictional demonstration data,
these statistics must not be presented as actual research findings.
"""

st.download_button(
    label="Download Research Summary Report (TXT)",
    data=report,
    file_name="research_summary_report.txt",
    mime="text/plain"
)

# =====================================================
# 20. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    **IEEE Week 2027 Research Project**

    Developed using Python, Streamlit, Pandas and Matplotlib.

    Research Domain: Data Science and Social Computing.
    """
)