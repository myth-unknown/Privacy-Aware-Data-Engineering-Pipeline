"""
Method comparison page with side-by-side analysis.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.comparison import compare_detection_methods
from src.utils.logger import get_logger

logger = get_logger(__name__)


def render():
    """Render the method comparison page."""
    st.title("⚖️ Method Comparison")

    # Check if data is uploaded
    if "uploaded_data" not in st.session_state or st.session_state.uploaded_data is None:
        st.warning("⚠️ No data uploaded. Please go to the **Upload Data** page first.")
        return

    df = st.session_state.uploaded_data
    file_name = st.session_state.get("uploaded_file_name", "dataset")

    st.markdown(f"**Dataset:** `{file_name}`")
    st.markdown(
        "Compare different PII detection methods to understand their strengths and trade-offs."
    )
    st.markdown("---")

    # Configuration
    st.subheader("⚙️ Comparison Configuration")
    _render_config()

    st.markdown("---")

    # Run comparison
    if "comparison_result" not in st.session_state or st.button(
        "🔄 Run Comparison", type="primary", use_container_width=True
    ):
        with st.spinner("🔍 Running comparison..."):
            _run_comparison(df)

    # Display results
    if "comparison_result" in st.session_state:
        result = st.session_state.comparison_result
        _render_results(result)


def _render_config():
    """Render comparison configuration."""
    col1, col2, col3 = st.columns(3)

    with col1:
        methods = st.multiselect(
            "Methods to Compare",
            ["rule_based", "nlp", "hybrid"],
            default=["rule_based", "nlp"],
            format_func=lambda x: {
                "rule_based": "Rule-Based (Regex)",
                "nlp": "NLP (Presidio)",
                "hybrid": "Hybrid (Both)",
            }[x],
        )
        st.session_state.comparison_methods = methods

    with col2:
        confidence = st.slider(
            "Confidence Threshold",
            0.0,
            1.0,
            0.5,
            0.05,
            help="Minimum confidence for detections",
        )
        st.session_state.comparison_confidence = confidence

    with col3:
        all_cols = st.session_state.uploaded_data.columns.tolist()
        selected_cols = st.multiselect(
            "Columns to Compare",
            all_cols,
            default=all_cols[:10] if len(all_cols) > 10 else all_cols,
        )
        st.session_state.comparison_columns = selected_cols if selected_cols else None


def _run_comparison(df: pd.DataFrame):
    """Run method comparison and cache results."""
    methods = st.session_state.get("comparison_methods", ["rule_based", "nlp"])
    confidence = st.session_state.get("comparison_confidence", 0.5)
    columns = st.session_state.get("comparison_columns", None)

    if not methods:
        st.error("Please select at least one method to compare.")
        return

    result = compare_detection_methods(
        df, methods=methods, confidence_threshold=confidence, columns=columns
    )

    st.session_state.comparison_result = result
    logger.info(f"Comparison complete: {len(result.methods_compared)} methods")
    st.success(f"✅ Comparison complete! Analyzed {len(methods)} method(s).")


def _render_results(result):
    """Render comparison results."""
    # Overview
    st.subheader("📊 Overview")
    _render_overview(result)

    st.markdown("---")

    # Side-by-side metrics
    st.subheader("📈 Performance Metrics")
    _render_metrics_comparison(result)

    st.markdown("---")

    # Detection counts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Detection Counts")
        _render_detection_counts(result)

    with col2:
        st.subheader("⚡ Execution Time")
        _render_execution_times(result)

    st.markdown("---")

    # Agreement/Disagreement analysis
    if len(result.methods_compared) >= 2:
        st.subheader("🤝 Agreement Analysis")
        _render_agreement_analysis(result)

        st.markdown("---")

    # PII Type Breakdown
    st.subheader("📋 PII Type Breakdown")
    _render_pii_type_breakdown(result)

    st.markdown("---")

    # Recommendation
    st.subheader("💡 Recommendation")
    _render_recommendation(result)


def _render_overview(result):
    """Render overview metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Methods Compared", len(result.methods_compared))

    with col2:
        st.metric("Rows Scanned", f"{result.total_rows:,}")

    with col3:
        st.metric("Columns Scanned", result.total_columns)

    with col4:
        total_detections = sum(
            m.total_detections for m in result.method_metrics.values()
        )
        st.metric("Total Detections", f"{total_detections:,}")


def _render_metrics_comparison(result):
    """Render side-by-side metrics table."""
    metrics_data = []

    for method_name, metrics in result.method_metrics.items():
        metrics_data.append(
            {
                "Method": method_name.replace("_", " ").title(),
                "Detections": f"{metrics.total_detections:,}",
                "Execution Time": f"{metrics.execution_time_seconds:.2f}s",
                "Throughput": f"{metrics.throughput_rows_per_second:.0f} rows/s",
                "Avg Confidence": f"{metrics.avg_confidence:.2f}",
                "Coverage %": f"{metrics.pii_percentage:.1f}%",
            }
        )

    df_metrics = pd.DataFrame(metrics_data)
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)


def _render_detection_counts(result):
    """Render detection counts bar chart."""
    methods = []
    counts = []

    for method_name, metrics in result.method_metrics.items():
        methods.append(method_name.replace("_", " ").title())
        counts.append(metrics.total_detections)

    fig = go.Figure(
        data=[
            go.Bar(
                x=methods,
                y=counts,
                text=counts,
                textposition="auto",
                marker={
                    "color": counts, "colorscale": "Blues", "showscale": False
                },
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Method",
        yaxis_title="Detection Count",
        showlegend=False,
        height=300,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_execution_times(result):
    """Render execution time comparison."""
    methods = []
    times = []

    for method_name, metrics in result.method_metrics.items():
        methods.append(method_name.replace("_", " ").title())
        times.append(metrics.execution_time_seconds)

    fig = go.Figure(
        data=[
            go.Bar(
                x=methods,
                y=times,
                text=[f"{t:.2f}s" for t in times],
                textposition="auto",
                marker={
                    "color": times, "colorscale": "Reds", "showscale": False
                },
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Method",
        yaxis_title="Execution Time (seconds)",
        showlegend=False,
        height=300,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_agreement_analysis(result):
    """Render agreement/disagreement analysis."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Agreement", f"{result.agreement_count:,}", help="Detected by all methods")

    with col2:
        st.metric("Disagreement", f"{result.disagreement_count:,}", help="Detected by some methods")

    with col3:
        total = result.agreement_count + result.disagreement_count
        agreement_pct = (result.agreement_count / total * 100) if total > 0 else 0
        st.metric("Agreement %", f"{agreement_pct:.1f}%")

    # Unique detections
    if result.unique_to_rule_based or result.unique_to_nlp or result.unique_to_hybrid:
        st.markdown("**Unique Detections:**")
        unique_data = []
        if result.unique_to_rule_based:
            unique_data.append({"Method": "Rule-Based", "Unique": result.unique_to_rule_based})
        if result.unique_to_nlp:
            unique_data.append({"Method": "NLP", "Unique": result.unique_to_nlp})
        if result.unique_to_hybrid:
            unique_data.append({"Method": "Hybrid", "Unique": result.unique_to_hybrid})

        df_unique = pd.DataFrame(unique_data)
        st.dataframe(df_unique, use_container_width=True, hide_index=True)


def _render_pii_type_breakdown(result):
    """Render PII type breakdown for each method."""
    # Collect all PII types
    all_types = set()
    for metrics in result.method_metrics.values():
        all_types.update(metrics.detections_by_type.keys())

    # Build data for heatmap
    methods = []
    types_list = sorted(all_types)
    data_matrix = []

    for method_name, metrics in result.method_metrics.items():
        methods.append(method_name.replace("_", " ").title())
        row = [metrics.detections_by_type.get(pii_type, 0) for pii_type in types_list]
        data_matrix.append(row)

    if data_matrix:
        fig = go.Figure(
            data=go.Heatmap(
                z=data_matrix,
                x=types_list,
                y=methods,
                colorscale="Blues",
                text=data_matrix,
                texttemplate="%{text}",
                textfont={"size": 10},
            )
        )

        fig.update_layout(
            xaxis_title="PII Type",
            yaxis_title="Method",
            height=200 + len(methods) * 50,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        st.plotly_chart(fig, use_container_width=True)


def _render_recommendation(result):
    """Render method recommendation."""
    if result.recommended_method:
        st.success(f"**Recommended Method:** {result.recommended_method.replace('_', ' ').title()}")
        st.info(f"**Reason:** {result.recommendation_reason}")
    else:
        st.warning("No recommendation available")

    # Summary insights
    with st.expander("📝 Summary Insights"):
        st.markdown(f"**Fastest Method:** {result.fastest_method.replace('_', ' ').title()}")
        st.markdown(
            f"**Most Detections:** {result.most_detections_method.replace('_', ' ').title()}"
        )
        st.markdown(
            f"**Highest Confidence:** {result.highest_confidence_method.replace('_', ' ').title()}"
        )


if __name__ == "__main__":
    render()
