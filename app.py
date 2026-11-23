
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

# ==========================================
# STEP 5: STREAMLIT WEB APPLICATION
# ==========================================

data_dir = Path(__file__).resolve().parent
log_path = data_dir / "verification_log.csv"

st.set_page_config(
    page_title="InvoiceFlow",
    page_icon="📄",
    layout="wide"
)

# 1. Load invoice data
@st.cache_data
def load_invoices():
    return pd.read_csv(
        data_dir / "invoices_cleaned.csv",
        dtype={"invoice_number": str}
    )


def load_verification_log():
    if log_path.exists():
        return pd.read_csv(log_path)

    return pd.DataFrame(
        columns=["record_id", "invoice_number", "verified_at"]
    )


def mark_as_verified(record):
    log = load_verification_log()
    record_id = int(record["record_id"])

    # Prevent duplicate verification
    verified_ids = set(
        pd.to_numeric(log["record_id"], errors="coerce")
        .dropna()
        .astype(int)
    )

    if record_id in verified_ids:
        return False

    new_entry = pd.DataFrame([{
        "record_id": record_id,
        "invoice_number": record["invoice_number"],
        "verified_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }])

    log = pd.concat([log, new_entry], ignore_index=True)
    log.to_csv(log_path, index=False)
    return True


invoices = load_invoices()
verification_log = load_verification_log()

verified_ids = set(
    pd.to_numeric(
        verification_log["record_id"],
        errors="coerce"
    ).dropna().astype(int)
)

# 2. Page header
st.title("InvoiceFlow")
st.caption("Invoice Lookup, Validation & Business Reporting")

page = st.sidebar.radio(
    "Navigation",
    ["Invoice Lookup", "Data Validation", "Business Reports"]
)

# ==========================================
# PAGE 1: INVOICE LOOKUP
# ==========================================

if page == "Invoice Lookup":

    st.header("Invoice Lookup by Tail Number")

    tail_number = st.text_input(
        "Enter the last 4 digits of the invoice number",
        placeholder="e.g. 0125 (1–4 digits accepted)"
    ).strip()

    if tail_number:

        if not tail_number.isdigit() or len(tail_number) > 4:
            st.warning("Please enter 1 to 4 digits.")

        else:
            results = invoices[
                invoices["invoice_number"].str.endswith(
                    tail_number, na=False
                )
            ]

            st.write(f"Found {len(results)} matching records.")

            if results.empty:
                st.info("No matching invoices found.")

            else:
                for _, record in results.iterrows():

                    record_id = int(record["record_id"])
                    already_verified = record_id in verified_ids

                    with st.container(border=True):
                        st.subheader(record["invoice_number"])

                        col1, col2, col3 = st.columns(3)

                        col1.write(f"Client: {record['client']}")
                        col2.write(f"Amount: {record['balance']}")
                        col3.write(
                            f"Invoice Status: {record['invoiceStatus']}"
                        )

                        st.write(
                            "Data Validation:",
                            record["validation_status"]
                        )

                        if already_verified:
                            st.success("Already Verified")

                        else:
                            st.info("Not Yet Verified")

                            if st.button(
                                "Mark as Verified",
                                key=f"verify_{record_id}"
                            ):
                                if mark_as_verified(record):
                                    st.rerun()
                                else:
                                    st.warning(
                                        "This invoice is already verified."
                                    )

    st.divider()
    st.metric("Verified Invoices", len(verified_ids))


# ==========================================
# PAGE 2: DATA VALIDATION
# ==========================================

elif page == "Data Validation":

    st.header("Data Validation Summary")

    total = len(invoices)
    review_count = (
        invoices["validation_status"] == "Review Required"
    ).sum()

    valid_count = (
        invoices["validation_status"] == "Valid"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", total)
    col2.metric("Valid Records", valid_count)
    col3.metric("Review Required", review_count)

    st.subheader("Records Requiring Review")

    exceptions = invoices[
        invoices["validation_status"] == "Review Required"
    ]

    st.dataframe(exceptions, use_container_width=True)

    st.download_button(
        "Download Exception Report",
        data=exceptions.to_csv(index=False),
        file_name="exception_report.csv",
        mime="text/csv"
    )


# ==========================================
# PAGE 3: BUSINESS REPORTS
# ==========================================

elif page == "Business Reports":

    st.header("SQL Business Reports")

    reports = {
        "Invoice Status Summary": "status_summary.csv",
        "Top Clients": "client_summary.csv",
        "Review Summary": "review_summary.csv",
        "Overdue Invoice Analysis": "overdue_summary.csv",
        "Monthly Invoice Analysis": "monthly_summary.csv",
        "Data Quality Summary": "quality_summary.csv"
    }

    selected_report = st.selectbox(
        "Select a report",
        list(reports.keys())
    )

    report_path = data_dir / reports[selected_report]

    if report_path.exists():
        report = pd.read_csv(report_path)

        st.dataframe(report, use_container_width=True)

        st.download_button(
            "Download Report",
            data=report.to_csv(index=False),
            file_name=reports[selected_report],
            mime="text/csv"
        )

    else:
        st.warning("Report file not found. Run Step 4 first.")
