"""
File upload page with data preview and validation.
"""

import os
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from src.ingestion import (
    load_csv,
    load_json,
    validate_dataframe,
    validate_file,
)
from src.ingestion.models import IssueSeverity
from src.utils.error_handler import (
    FILE_LOAD_ERROR,
    UNEXPECTED_ERROR,
    get_user_friendly_error,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def render():
    """Render the file upload page."""
    st.title("📤 Upload Data")
    st.markdown(
        """
        Upload your dataset to begin the privacy-aware data engineering pipeline.
        Supported formats: **CSV** and **JSON**.
        """
    )

    # File uploader
    st.subheader("1️⃣ Select File")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "json"],
        help="Maximum file size: 100 MB",
    )

    if uploaded_file is None:
        st.info("👆 Upload a file to get started")
        _render_sample_data_section()
        return

    # Save uploaded file to temp location
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=Path(uploaded_file.name).suffix
        ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        logger.info(f"Uploaded file saved to {tmp_path}")

        # File validation
        st.subheader("2️⃣ File Validation")
        with st.spinner("Validating file..."):
            file_result = validate_file(tmp_path)

        _display_validation_result(file_result)

        if not file_result.success:
            st.error("❌ File validation failed. Please fix the issues and try again.")
            os.unlink(tmp_path)  # Clean up temp file
            return

        # Load data
        st.subheader("3️⃣ Load Data")
        with st.spinner("Loading data..."):
            try:
                file_ext = Path(uploaded_file.name).suffix.lower()

                if file_ext == ".csv":
                    # CSV delimiter selection
                    delimiter = st.selectbox(
                        "CSV Delimiter",
                        [",", ";", "\t", "|"],
                        format_func=lambda x: {"," : "Comma (,)", ";": "Semicolon (;)", "\t": "Tab", "|": "Pipe (|)"}[x],
                        help="Select the delimiter used in your CSV file",
                    )
                    df = load_csv(tmp_path, delimiter=delimiter)
                elif file_ext == ".json":
                    df = load_json(tmp_path)
                else:
                    st.error(f"Unsupported file format: {file_ext}")
                    os.unlink(tmp_path)
                    return

                logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")

            except Exception as e:
                error_msg = get_user_friendly_error(e, FILE_LOAD_ERROR)
                st.error(f"❌ {error_msg}")
                os.unlink(tmp_path)
                return

        # DataFrame validation
        st.subheader("4️⃣ Data Validation")
        with st.spinner("Validating data..."):
            df_result = validate_dataframe(df, file_name=uploaded_file.name)

        _display_validation_result(df_result)

        # Data preview
        st.subheader("5️⃣ Data Preview")
        _display_data_preview(df, df_result)

        # Save to session state
        if st.button("✅ Accept and Continue", type="primary", use_container_width=True):
            with st.spinner("💾 Saving data to session..."):
                st.session_state["uploaded_data"] = df
                st.session_state["uploaded_file_name"] = uploaded_file.name
                st.session_state["ingestion_result"] = df_result
                st.session_state["scroll_to_top"] = True  # Flag to scroll to top on next page

                # Clear downstream cached results when new data is uploaded
                for key in ["quality_profile", "pii_detections", "anonymized_data"]:
                    if key in st.session_state:
                        del st.session_state[key]

                logger.info(f"Data saved to session state: {uploaded_file.name}")

            st.success("✅ Data uploaded successfully!")
            st.info("📌 Next: Go to **Data Quality** page to analyze your dataset.")

        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except Exception as e:
            logger.warning(f"Failed to delete temp file: {e}")

    except Exception as e:
        error_msg = get_user_friendly_error(e, UNEXPECTED_ERROR)
        st.error(f"❌ {error_msg}")


def _display_validation_result(result):
    """Display validation result with issues grouped by severity."""
    if not result.issues:
        st.success("✅ No issues detected")
        return

    # Count issues by severity
    error_count = sum(1 for issue in result.issues if issue.severity == IssueSeverity.ERROR)
    warning_count = sum(1 for issue in result.issues if issue.severity == IssueSeverity.WARNING)
    info_count = sum(1 for issue in result.issues if issue.severity == IssueSeverity.INFO)

    # Display summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Errors", error_count)
    with col2:
        st.metric("Warnings", warning_count)
    with col3:
        st.metric("Info", info_count)

    # Display issues
    if error_count > 0:
        with st.expander("❌ Errors", expanded=True):
            for issue in result.issues:
                if issue.severity == IssueSeverity.ERROR:
                    st.error(f"**{issue.message}**")

    if warning_count > 0:
        with st.expander("⚠️ Warnings"):
            for issue in result.issues:
                if issue.severity == IssueSeverity.WARNING:
                    st.warning(issue.message)

    if info_count > 0:
        with st.expander("ℹ️ Info"):
            for issue in result.issues:
                if issue.severity == IssueSeverity.INFO:
                    st.info(issue.message)


def _display_data_preview(df: pd.DataFrame, result):
    """Display data preview with metadata."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        st.metric("Memory", f"{memory_mb:.2f} MB")
    with col4:
        null_count = df.isnull().sum().sum()
        st.metric("Null Values", f"{null_count:,}")

    # Display first and last rows
    tab1, tab2, tab3 = st.tabs(["First Rows", "Last Rows", "Column Info"])

    with tab1:
        st.dataframe(df.head(10), use_container_width=True)

    with tab2:
        st.dataframe(df.tail(10), use_container_width=True)

    with tab3:
        col_info = pd.DataFrame(
            {
                "Column": df.columns,
                "Type": df.dtypes.astype(str),
                "Non-Null": df.notnull().sum(),
                "Null": df.isnull().sum(),
                "Null %": (df.isnull().sum() / len(df) * 100).round(2),
            }
        )
        st.dataframe(col_info, use_container_width=True)


def _render_sample_data_section():
    """Render section with download buttons for sample data."""
    st.markdown("---")
    st.subheader("📁 Sample Data")
    st.markdown(
        """
        Don't have a dataset ready? Download our sample datasets to explore the pipeline:
        """
    )
    
    # Check if sample files exist
    import os
    from pathlib import Path
    
    sample_dir = Path("data/samples")
    
    # Sample files with descriptions
    samples = [
        {
            "file": "test_employee_data.csv",
            "name": "Employee Data (Recommended)",
            "icon": "👥",
            "description": "15 employees with 14 columns including SSN, emails, phones, salary (90 PII instances)",
        },
        {
            "file": "customers.csv",
            "name": "Customer Information",
            "icon": "🛒",
            "description": "Customer data with PII (email, phone, address)",
        },
        {
            "file": "orders.json",
            "name": "Order Data (JSON)",
            "icon": "📦",
            "description": "Order data in JSON format with various PII types",
        },
        {
            "file": "malformed.csv",
            "name": "Malformed Data",
            "icon": "⚠️",
            "description": "Dataset with quality issues for testing validation",
        },
    ]
    
    # Create download buttons for each sample
    for sample in samples:
        file_path = sample_dir / sample["file"]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{sample['icon']} {sample['name']}**")
            st.caption(sample["description"])
        
        with col2:
            if file_path.exists():
                # Read file data
                with open(file_path, "rb") as f:
                    file_data = f.read()
                
                st.download_button(
                    label="📥 Download",
                    data=file_data,
                    file_name=sample["file"],
                    mime="text/csv" if sample["file"].endswith(".csv") else "application/json",
                    key=f"download_{sample['file']}",
                    use_container_width=True,
                )
            else:
                st.button(
                    "❌ Not Found",
                    disabled=True,
                    use_container_width=True,
                    key=f"missing_{sample['file']}",
                )
        
        st.markdown("")  # Add spacing


if __name__ == "__main__":
    render()
