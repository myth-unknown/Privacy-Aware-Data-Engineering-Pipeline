"""
Data quality profiling and visualization page.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.utils.error_handler import (
    QUALITY_PROFILING_ERROR,
    get_user_friendly_error,
)
from src.utils.logger import get_logger
from src.validation import profile_dataframe

logger = get_logger(__name__)


def render():
    """Render the data quality page."""
    st.title("📊 Data Quality Profiling")

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

    # Generate quality profile with error handling
    profile = None
    if "quality_profile" not in st.session_state or st.session_state.quality_profile is None:
        with st.spinner("Analyzing data quality..."):
            try:
                profile = profile_dataframe(df)

                # Validate profile before storing
                if profile is None:
                    raise ValueError("Profile generation returned None")
                if not hasattr(profile, 'quality_score'):
                    raise ValueError("Profile missing quality_score attribute")
                if profile.quality_score is None:
                    raise ValueError("Profile quality_score is None")

                st.session_state.quality_profile = profile
                logger.info(f"Quality profile generated: score={profile.quality_score:.1f}")

            except Exception as e:
                error_msg = get_user_friendly_error(e, QUALITY_PROFILING_ERROR)
                st.error(f"❌ {error_msg}")

                # Show retry button
                if st.button("🔄 Retry Profiling"):
                    if "quality_profile" in st.session_state:
                        del st.session_state.quality_profile
                    st.rerun()
                return
    else:
        profile = st.session_state.quality_profile

        # Validate cached profile
        if profile is None or not hasattr(profile, 'quality_score') or profile.quality_score is None:
            st.error("❌ Cached quality profile is invalid")
            if st.button("🔄 Regenerate Profile"):
                if "quality_profile" in st.session_state:
                    del st.session_state.quality_profile
                st.rerun()
            return

    # Quality Score Card
    _render_quality_score(profile)

    st.markdown("---")

    # Overview Metrics
    st.subheader("📈 Overview")
    _render_overview_metrics(profile)

    st.markdown("---")

    # Quality Issues
    if profile.has_issues:
        st.subheader("⚠️ Quality Issues")
        _render_quality_issues(profile)
        st.markdown("---")

    # Column Analysis Tabs
    st.subheader("🔍 Column Analysis")
    _render_column_analysis(df, profile)

    st.markdown("---")

    # Data Type Distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Data Types")
        _render_data_type_distribution(profile)

    with col2:
        st.subheader("💾 Memory Usage")
        _render_memory_usage(df)

    st.markdown("---")

    # Action Buttons
    st.subheader("🛠️ Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Accept Quality Profile", type="primary", use_container_width=True, key="accept_quality"):
            with st.spinner("💾 Saving quality profile..."):
                # Scroll to top on next page load
                st.session_state['scroll_to_top'] = True
            st.success("✅ Quality profile accepted!")
            st.info("📌 Next: Go to **PII Detection** page to identify sensitive data.")

    with col2:
        if st.button("🔄 Regenerate Profile", use_container_width=True):
            with st.spinner("🔄 Clearing cache..."):
                del st.session_state.quality_profile
            st.rerun()

    with col3:
        if st.button("📥 Download Report", use_container_width=True):
            st.info("📊 Report download feature coming in Milestone 11")


def _render_quality_score(profile):
    """Render quality score with visual indicator."""
    score = profile.quality_score

    # Determine color and label
    if score >= 80:
        color = "green"
        label = "Excellent"
        emoji = "🟢"
    elif score >= 60:
        color = "orange"
        label = "Good"
        emoji = "🟡"
    elif score >= 40:
        color = "orange"
        label = "Fair"
        emoji = "🟠"
    else:
        color = "red"
        label = "Poor"
        emoji = "🔴"

    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Quality Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 40], "color": "lightgray"},
                {"range": [40, 60], "color": "lightgray"},
                {"range": [60, 80], "color": "lightgray"},
                {"range": [80, 100], "color": "lightgray"},
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": score,
            },
        },
    ))

    fig.update_layout(height=250, margin={"l": 20, "r": 20, "t": 50, "b": 20})

    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"### {emoji} {label}")
        st.metric("Score", f"{score:.1f}/100")
        st.metric("Issues", len(profile.issues))


def _render_overview_metrics(profile):
    """Render overview metrics in columns."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", f"{profile.num_rows:,}")
        st.metric("Columns", profile.num_columns)

    with col2:
        st.metric("Missing Values", f"{profile.total_nulls:,}")
        st.metric("Missing %", f"{profile.null_percentage:.1f}%")

    with col3:
        st.metric("Duplicate Rows", f"{profile.duplicate_rows:,}")
        st.metric("Duplicate %", f"{profile.duplicate_percentage:.1f}%")

    with col4:
        memory_mb = profile.memory_usage_bytes / (1024 * 1024)
        st.metric("Memory", f"{memory_mb:.2f} MB")
        st.metric("Complete Columns",
                  sum(1 for cp in profile.column_profiles.values() if cp.null_count == 0))


def _render_quality_issues(profile):
    """Render quality issues grouped by severity."""
    # Count by severity
    high_issues = profile.high_severity_issues
    medium_issues = profile.medium_severity_issues
    low_issues = profile.low_severity_issues

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 High", len(high_issues))
    with col2:
        st.metric("🟡 Medium", len(medium_issues))
    with col3:
        st.metric("🔵 Low", len(low_issues))

    # Issue tables
    if high_issues:
        with st.expander("🔴 High Severity Issues", expanded=True):
            _render_issue_table(high_issues)

    if medium_issues:
        with st.expander("🟡 Medium Severity Issues"):
            _render_issue_table(medium_issues)

    if low_issues:
        with st.expander("🔵 Low Severity Issues"):
            _render_issue_table(low_issues)


def _render_issue_table(issues):
    """Render issues as a table."""
    issue_data = []
    for issue in issues:
        issue_data.append({
            "Column": issue.column,
            "Type": issue.issue_type,
            "Count": f"{issue.count:,}",
            "Percentage": f"{issue.percentage:.1f}%",
            "Description": issue.description,
        })

    df_issues = pd.DataFrame(issue_data)
    st.dataframe(df_issues, use_container_width=True, hide_index=True, height=300)


def _render_column_analysis(df, profile):
    """Render detailed column analysis with tabs."""
    tabs = st.tabs(["Numeric Columns", "String Columns", "All Columns"])

    with tabs[0]:
        if profile.numeric_columns:
            _render_numeric_analysis(df, profile)
        else:
            st.info("No numeric columns found")

    with tabs[1]:
        if profile.string_columns:
            _render_string_analysis(df, profile)
        else:
            st.info("No string columns found")

    with tabs[2]:
        _render_all_columns_table(profile)


def _render_numeric_analysis(df, profile):
    """Render analysis for numeric columns."""
    numeric_data = []

    for col in profile.numeric_columns:
        col_profile = profile.column_profiles[col]
        numeric_data.append({
            "Column": col,
            "Mean": f"{col_profile.mean:.2f}" if col_profile.mean is not None else "N/A",
            "Median": f"{col_profile.median:.2f}" if col_profile.median is not None else "N/A",
            "Std": f"{col_profile.std:.2f}" if col_profile.std is not None else "N/A",
            "Min": f"{col_profile.min_value:.2f}" if col_profile.min_value is not None else "N/A",
            "Max": f"{col_profile.max_value:.2f}" if col_profile.max_value is not None else "N/A",
            "Nulls": f"{col_profile.null_count} ({col_profile.null_percentage:.1f}%)",
            "Unique": col_profile.unique_count,
        })

    df_numeric = pd.DataFrame(numeric_data)
    st.dataframe(df_numeric, use_container_width=True, hide_index=True, height=400)


def _render_string_analysis(df, profile):
    """Render analysis for string columns."""
    string_data = []

    for col in profile.string_columns:
        col_profile = profile.column_profiles[col]
        string_data.append({
            "Column": col,
            "Unique": col_profile.unique_count,
            "Nulls": f"{col_profile.null_count} ({col_profile.null_percentage:.1f}%)",
            "Min Length": col_profile.min_length if col_profile.min_length is not None else "N/A",
            "Max Length": col_profile.max_length if col_profile.max_length is not None else "N/A",
            "Avg Length": f"{col_profile.avg_length:.1f}" if col_profile.avg_length is not None else "N/A",
            "Top Value": list(col_profile.top_values.keys())[0] if col_profile.top_values else "N/A",
        })

    df_string = pd.DataFrame(string_data)
    st.dataframe(df_string, use_container_width=True, hide_index=True, height=400)


def _render_all_columns_table(profile):
    """Render summary table for all columns."""
    all_cols_data = []

    for col_name, col_profile in profile.column_profiles.items():
        all_cols_data.append({
            "Column": col_name,
            "Type": col_profile.dtype,
            "Non-Null": f"{col_profile.non_null_count:,}",
            "Null": f"{col_profile.null_count:,}",
            "Null %": f"{col_profile.null_percentage:.1f}%",
            "Unique": f"{col_profile.unique_count:,}",
            "Duplicates": f"{col_profile.duplicate_count:,}",
        })

    df_all = pd.DataFrame(all_cols_data)
    st.dataframe(df_all, use_container_width=True, hide_index=True, height=400)


def _render_data_type_distribution(profile):
    """Render data type distribution chart."""
    type_counts = {
        "Numeric": len(profile.numeric_columns),
        "String": len(profile.string_columns),
        "DateTime": len(profile.datetime_columns),
        "Boolean": len(profile.boolean_columns),
    }

    # Filter out zero counts
    type_counts = {k: v for k, v in type_counts.items() if v > 0}

    fig = px.pie(
        values=list(type_counts.values()),
        names=list(type_counts.keys()),
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


def _render_memory_usage(df):
    """Render memory usage breakdown."""
    memory_by_col = df.memory_usage(deep=True)
    top_10 = memory_by_col.nlargest(10)

    # Convert to MB
    top_10_mb = top_10 / (1024 * 1024)

    fig = px.bar(
        x=top_10_mb.values,
        y=top_10_mb.index,
        orientation="h",
        labels={"x": "Memory (MB)", "y": "Column"},
    )
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    render()
