# InvoiceFlow

**Invoice Processing, Data Validation & Business Reporting**

InvoiceFlow is a Python-based invoice processing application designed to streamline invoice lookup, identify data quality issues, track manual verification, and generate business reports through an interactive Streamlit dashboard.

The project uses synthetic invoice data and demonstrates a workflow from raw data preparation to financial data analysis and application development.

## Features

### 1. Invoice Lookup
- Search invoice records using the last 1–4 digits of an invoice number.
- Display invoice details, payment status, and data validation results.
- Mark invoices as manually verified and prevent duplicate verification records.

### 2. Data Cleaning & Validation
- Standardize client names and date formats.
- Identify missing client information and amount discrepancies.
- Flag records requiring review without removing them from the dataset.
- Export exception reports.

### 3. SQL Business Reporting
- Invoice status summary
- Client-level invoice analysis
- Data quality and exception analysis
- Overdue invoice analysis
- Monthly invoice analysis

## Technology Stack

- **Python** — Data processing and application logic
- **pandas** — Data cleaning and validation
- **DuckDB / SQL** — Business analysis and reporting
- **Streamlit** — Interactive web application
- **Jupyter Notebook** — Development and analysis

## Dataset

The project uses synthetic invoice records for demonstration purposes. A subset of 5,000 records is used to demonstrate cleaning, validation, and reporting workflows.

## Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Project Scope

InvoiceFlow is a portfolio prototype developed for educational and demonstration purposes. It is not intended for production financial operations without further validation, access controls, and persistent storage.

## Author

GitHub: [Xiaooo469](https://github.com/Xiaooo469)
