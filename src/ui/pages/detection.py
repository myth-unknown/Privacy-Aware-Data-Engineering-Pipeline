"""
PII detection results page with visualization.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.detection import create_detection_summary, detect_pii
from src.utils.error_handler import (
    PII_DETECTION_ERROR,
    get_user_friendly_error,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def render():
    """Render the PII detection page."""
    st.title("🔍 PII Detection")

    # Scroll to top if flagged
    if st.session_state.get('scroll_to_top', False):
        st.session_state['scroll_to_top'] = False

    # Check if data is uploaded
    if "uploaded_data" not in st.session_state or st.session_state.uploaded_data is None:
        st.warning("⚠️ No data uploaded. Please go to the **Upload Data** page first.")
        return

    df = st.session_state.uploaded_data
    file_name = st.session_state.get("uploaded_file_name", "dataset")

    st.markdown(f"**Dataset:** `{file_name}`")
    st.markdown("---")

    # Detection configuration
    st.subheader("⚙️ Detection Configuration")
    _render_detection_config()

    st.markdown("---")

    # Run detection or show cached results
    if "detection_results" not in st.session_state or st.button(
        "🔄 Re-run Detection", use_container_width=True
    ):
        # Clear cached prepared export data
        if 'prepared_export' in st.session_state:
            del st.session_state['prepared_export']
            
        with st.spinner("🔍 Scanning for PII..."):
            _run_detection(df)

    # Display results
    if "detection_results" in st.session_state:
        detections = st.session_state.detection_results
        summary = st.session_state.detection_summary

        if summary.has_detections:
            _render_detection_results(df, detections, summary)
        else:
            st.success("✅ No PII detected in the dataset!")
            st.info(
                "This could mean:\n"
                "- The dataset is clean and contains no PII\n"
                "- The confidence threshold is too high\n"
                "- PII types need to be adjusted"
            )

        # Action buttons
        st.markdown("---")
        _render_action_buttons(detections)


def _render_detection_config():
    """Render detection configuration form."""
    col1, col2, col3 = st.columns(3)

    with col1:
        method = st.selectbox(
            "Detection Method",
            ["rule_based", "nlp", "hybrid"],
            format_func=lambda x: {
                "rule_based": "Rule-Based (Regex)",
                "nlp": "NLP (Presidio)",
                "hybrid": "Hybrid (Both)",
            }[x],
            help="Choose detection algorithm",
        )
        st.session_state.detection_method = method

    with col2:
        confidence = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Minimum confidence to report detection",
        )
        st.session_state.confidence_threshold = confidence

    with col3:
        # Column selection
        all_cols = st.session_state.uploaded_data.columns.tolist()
        selected_cols = st.multiselect(
            "Columns to Scan",
            all_cols,
            default=all_cols[:10] if len(all_cols) > 10 else all_cols,
            help="Select columns to scan (default: first 10)",
        )
        st.session_state.selected_columns = selected_cols if selected_cols else None


def _run_detection(df: pd.DataFrame):
    """Run PII detection and cache results."""
    method = st.session_state.get("detection_method", "rule_based")
    confidence = st.session_state.get("confidence_threshold", 0.5)
    columns = st.session_state.get("selected_columns", None)

    try:
        detections = detect_pii(
            df,
            method=method,
            confidence_threshold=confidence,
            columns=columns,
        )

        summary = create_detection_summary(detections)

        st.session_state.detection_results = detections
        st.session_state.detection_summary = summary

        logger.info(
            f"Detection complete: {len(detections)} instances, "
            f"{summary.affected_rows} rows, {summary.affected_columns} columns"
        )

        st.success(f"✅ Detection complete! Found {len(detections)} PII instances.")

    except Exception as e:
        error_msg = get_user_friendly_error(e, PII_DETECTION_ERROR)
        st.error(f"❌ {error_msg}")


def _render_detection_results(df: pd.DataFrame, detections, summary):
    """Render detection results with visualizations."""
    # Overview metrics
    st.subheader("📊 Detection Summary")
    _render_summary_metrics(summary)

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 PII Types Distribution")
        _render_pii_types_chart(summary)

    with col2:
        st.subheader("📍 Affected Columns")
        _render_affected_columns_chart(summary)

    st.markdown("---")

    # Confidence distribution
    st.subheader("🎯 Confidence Distribution")
    _render_confidence_chart(summary)

    st.markdown("---")

    # Detection details table
    st.subheader("🔎 Detection Details")
    _render_detections_table(detections, df)


def _render_summary_metrics(summary):
    """Render summary metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Detections", f"{summary.total_detections:,}")

    with col2:
        st.metric("Affected Rows", f"{summary.affected_rows:,}")

    with col3:
        st.metric("Affected Columns", summary.affected_columns)

    with col4:
        st.metric("PII Types", len(summary.detections_by_type))

    # Method breakdown
    if summary.detection_methods:
        st.markdown("**Detection Methods:**")
        method_cols = st.columns(len(summary.detection_methods))
        for idx, (method, count) in enumerate(summary.detection_methods.items()):
            with method_cols[idx]:
                st.metric(method.replace("_", " ").title(), count)


def _render_pii_types_chart(summary):
    """Render PII types distribution chart."""
    if not summary.detections_by_type:
        st.info("No PII types detected")
        return

    # Sort by count
    sorted_types = sorted(
        summary.detections_by_type.items(), key=lambda x: x[1], reverse=True
    )

    df_types = pd.DataFrame(sorted_types, columns=["Type", "Count"])

    fig = px.bar(
        df_types,
        x="Count",
        y="Type",
        orientation="h",
        color="Count",
        color_continuous_scale="Reds",
    )
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


def _render_affected_columns_chart(summary):
    """Render affected columns chart."""
    if not summary.detections_by_column:
        st.info("No columns affected")
        return

    # Top 10 columns
    sorted_cols = sorted(
        summary.detections_by_column.items(), key=lambda x: x[1], reverse=True
    )[:10]

    df_cols = pd.DataFrame(sorted_cols, columns=["Column", "Detections"])

    fig = px.bar(
        df_cols,
        x="Detections",
        y="Column",
        orientation="h",
        color="Detections",
        color_continuous_scale="Blues",
    )
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


def _render_confidence_chart(summary):
    """Render confidence distribution chart."""
    if not summary.confidence_distribution:
        st.info("No confidence data")
        return

    # Create pie chart
    labels = []
    values = []
    colors = []

    for level in ["high", "medium", "low"]:
        if level in summary.confidence_distribution:
            labels.append(f"{level.title()} (≥{0.8 if level == 'high' else 0.5 if level == 'medium' else 0.0})")
            values.append(summary.confidence_distribution[level])
            colors.append("#28a745" if level == "high" else "#ffc107" if level == "medium" else "#dc3545")

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker={"colors": colors})])
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


def _render_detections_table(detections, df: pd.DataFrame):
    """Render detailed detections table."""
    if not detections:
        st.info("No detections to display")
        return

    # Convert to DataFrame
    table_data = []
    for d in detections[:100]:  # Limit to first 100
        table_data.append(
            {
                "Row": d.row_index,
                "Column": d.column,
                "PII Type": d.pii_type,
                "Value": d.value[:50] + "..." if len(d.value) > 50 else d.value,
                "Confidence": f"{d.confidence:.2%}",
                "Method": d.detection_method,
            }
        )

    df_table = pd.DataFrame(table_data)

    # Filter controls
    col1, col2 = st.columns(2)

    with col1:
        filter_type = st.multiselect(
            "Filter by PII Type",
            options=df_table["PII Type"].unique(),
            default=df_table["PII Type"].unique(),
        )

    with col2:
        filter_method = st.multiselect(
            "Filter by Method",
            options=df_table["Method"].unique(),
            default=df_table["Method"].unique(),
        )

    # Apply filters
    filtered = df_table[
        (df_table["PII Type"].isin(filter_type)) & (df_table["Method"].isin(filter_method))
    ]

    st.dataframe(filtered, use_container_width=True, hide_index=True, height=400)

    if len(detections) > 100:
        st.info(f"Showing first 100 of {len(detections)} detections")


def _render_action_buttons(detections):
    """Render action buttons."""
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Accept and Continue", type="primary", use_container_width=True):
            st.session_state["scroll_to_top"] = True  # Flag to scroll to top on next page
            st.success("✅ Detection results accepted!")
            st.info("📌 Next: Go to **Anonymization** page to transform PII.")

    with col2:
        # Button to trigger export preparation
        if st.button("📥 Export Results", use_container_width=True, key="prepare_export"):
            with st.spinner("🔄 Preparing export file..."):
                # Create export DataFrame
                export_data = []
                for d in detections:
                    export_data.append(
                        {
                            "row_index": d.row_index,
                            "column": d.column,
                            "pii_type": d.pii_type,
                            "value": d.value,
                            "confidence": d.confidence,
                            "method": d.detection_method,
                        }
                    )

                df_export = pd.DataFrame(export_data)
                csv = df_export.to_csv(index=False)
                st.session_state['prepared_export'] = csv
        
        # Show download button after preparation
        if 'prepared_export' in st.session_state:
            st.download_button(
                label="📥 Download CSV",
                data=st.session_state['prepared_export'],
                file_name="pii_detections.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True,
                key="download_export"
            )

    with col3:
        if st.button("🗑️ Clear Results", use_container_width=True):
            # Clear session state including prepared exports
            for key in ["detection_results", "detection_summary", "prepared_export"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    render()
