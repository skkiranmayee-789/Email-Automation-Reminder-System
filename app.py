import streamlit as st
import pandas as pd
import os

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Email Automation Dashboard",
    page_icon="📧",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("📧 Email Automation & Reminder Dashboard")
st.write("Python-based Productivity Automation System")

# -----------------------------------
# LOAD REPORT
# -----------------------------------
report_path = "outputs/email_report.csv"

if os.path.exists(report_path):

    df = pd.read_csv(report_path)

    # -----------------------------------
    # METRICS
    # -----------------------------------
    total_emails = len(df)

    sent_count = len(df[df["Status"] == "Sent"])

    failed_count = len(df[df["Status"] == "Failed"])

    # -----------------------------------
    # DISPLAY METRICS
    # -----------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("📨 Total Emails", total_emails)

    col2.metric("✅ Sent Emails", sent_count)

    col3.metric("❌ Failed Emails", failed_count)

    st.divider()

    # -----------------------------------
    # REPORT TABLE
    # -----------------------------------
    st.subheader("📊 Email Report")

    st.dataframe(df, use_container_width=True)

    # -----------------------------------
    # DOWNLOAD BUTTON
    # -----------------------------------
    with open(report_path, "rb") as file:

        st.download_button(
            label="📥 Download CSV Report",
            data=file,
            file_name="email_report.csv",
            mime="text/csv"
        )

    st.divider()

    # -----------------------------------
    # LOG VIEWER
    # -----------------------------------
    st.subheader("📝 Email Logs")

    log_path = "logs/email_logs.log"

    if os.path.exists(log_path):

        with open(log_path, "r") as log_file:

            logs = log_file.read()

            st.text_area(
                "Logs",
                logs,
                height=300
            )

    else:
        st.warning("No log file found.")

else:

    st.warning("No email report found. Run main.py first.")