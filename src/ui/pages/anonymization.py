"""
Anonymization page with strategy configuration and preview.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.anonymization import anonymize_dataframe
from src.utils.error_handler import (
    ANONYMIZATION_ERROR,
    get_user_friendly_error,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def render():
    """Render the anonymization page."""
    st.title("🎭 PII Anonymization")

    # Scroll to top if flagged
    if st.session_state.get('scroll_to_top', False):
        st.session_state['scroll_to_top'] = False

    # Check if data and detections are available
    if "uploaded_data" not in st.session_state or st.session_state.uploaded_data is None:
        st.warning("⚠️ No data uploaded. Please go to the **Upload Data** page first.")
        return

    if "detection_results" not in st.session_state:
        st.warning("⚠️ No PII detections available. Please run **PII Detection** first.")
        return

    df = st.session_state.uploaded_data
    detections = st.session_state.detection_results

    file_name = st.session_state.get("uploaded_file_name", "dataset")

    st.markdown(f"**Dataset:** `{file_name}` | **Detections:** {len(detections)}")
    st.markdown("---")

    # Configuration
    st.subheader("⚙️ Anonymization Configuration")
    _render_config()

    st.markdown("---")

    # Apply anonymization or show cached results
    if "anonymization_result" not in st.session_state or st.button(
        "🔄 Re-apply Anonymization", use_container_width=True
    ):
        with st.spinner("🎭 Applying anonymization..."):
            _apply_anonymization(df, detections)

    # Display results
    if "anonymization_result" in st.session_state:
        result = st.session_state.anonymization_result

        if result.success:
            _render_results(df, result)
        else:
            st.error("❌ Anonymization failed!")
            for error in result.errors:
                st.error(error)


def _render_config():
    """Render configuration form."""
    col1, col2, col3 = st.columns(3)

    with col1:
        strategy = st.selectbox(
            "Strategy",
            ["mask", "redact", "pseudonymize", "generalize"],
            format_func=lambda x: {
                "mask": "Mask (e.g., ***-**-6789)",
                "redact": "Redact ([REDACTED])",
                "pseudonymize": "Pseudonymize (consistent hash)",
                "generalize": "Generalize (broader category)",
            }[x],
            help="Choose anonymization method",
        )
        st.session_state.anon_strategy = strategy

    with col2:
        # Get unique PII types from detections
        if "detection_summary" in st.session_state:
            pii_types = ["ALL"] + list(
                st.session_state.detection_summary.detections_by_type.keys()
            )
        else:
            pii_types = ["ALL"]

        pii_type = st.selectbox(
            "PII Type",
            pii_types,
            help="Which PII type to anonymize",
        )
        st.session_state.anon_pii_type = pii_type

    with col3:
        # Strategy-specific parameters
        if strategy == "mask":
            mask_char = st.text_input("Mask Character", value="*", max_chars=1)
            st.session_state.anon_mask_char = mask_char
        elif strategy == "generalize":
            level = st.selectbox(
                "Generalization Level",
                ["low", "medium", "high"],
                help="How much to generalize",
            )
            st.session_state.anon_gen_level = level
        elif strategy == "pseudonymize":
            seed = st.text_input("Seed (optional)", value="", help="For consistent pseudonyms")
            st.session_state.anon_seed = seed if seed else None


def _apply_anonymization(df: pd.DataFrame, detections):
    """Apply anonymization and cache result."""
    strategy = st.session_state.get("anon_strategy", "mask")
    pii_type = st.session_state.get("anon_pii_type", "ALL")

    kwargs = {}
    if strategy == "mask":
        kwargs["mask_char"] = st.session_state.get("anon_mask_char", "*")
    elif strategy == "generalize":
        kwargs["generalization_level"] = st.session_state.get("anon_gen_level", "medium")
    elif strategy == "pseudonymize":
        kwargs["pseudonym_seed"] = st.session_state.get("anon_seed", None)

    try:
        result = anonymize_dataframe(
            df, detections, strategy=strategy, pii_type=pii_type, **kwargs
        )

        st.session_state.anonymization_result = result

        if result.success:
            st.success(
                f"✅ Anonymization complete! {result.audit.total_transformations} transformations applied."
            )
        else:
            st.warning("⚠️ Anonymization completed with errors.")

    except Exception as e:
        error_msg = get_user_friendly_error(e, ANONYMIZATION_ERROR)
        st.error(f"❌ {error_msg}")


def _render_results(original_df: pd.DataFrame, result):
    """Render anonymization results."""
    # Audit summary
    st.subheader("📊 Transformation Summary")
    _render_audit_summary(result.audit)

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Transformations by Type")
        _render_transformations_by_type(result.audit)

    with col2:
        st.subheader("📍 Transformations by Column")
        _render_transformations_by_column(result.audit)

    st.markdown("---")

    # Before/After Comparison
    st.subheader("🔄 Before / After Comparison")
    _render_comparison(original_df, result.data)

    st.markdown("---")

    # Action buttons
    _render_action_buttons(result)


def _render_audit_summary(audit):
    """Render audit summary metrics."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Transformations", f"{audit.total_transformations:,}")

    with col2:
        st.metric("Affected Columns", len(audit.transformations_by_column))

    with col3:
        st.metric("PII Types", len(audit.transformations_by_type))

    with col4:
        duration = audit.duration_seconds
        st.metric("Duration", f"{duration:.2f}s" if duration else "N/A")


def _render_transformations_by_type(audit):
    """Render transformations by PII type chart."""
    if not audit.transformations_by_type:
        st.info("No transformations")
        return

    sorted_types = sorted(
        audit.transformations_by_type.items(), key=lambda x: x[1], reverse=True
    )

    df_types = pd.DataFrame(sorted_types, columns=["Type", "Count"])

    fig = px.bar(
        df_types,
        x="Count",
        y="Type",
        orientation="h",
        color="Count",
        color_continuous_scale="Greens",
    )
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


def _render_transformations_by_column(audit):
    """Render transformations by column chart."""
    if not audit.transformations_by_column:
        st.info("No transformations")
        return

    sorted_cols = sorted(
        audit.transformations_by_column.items(), key=lambda x: x[1], reverse=True
    )[:10]

    df_cols = pd.DataFrame(sorted_cols, columns=["Column", "Transformations"])

    fig = px.bar(
        df_cols,
        x="Transformations",
        y="Column",
        orientation="h",
        color="Transformations",
        color_continuous_scale="Purples",
    )
    fig.update_layout(showlegend=False, height=300, margin={"l": 0, "r": 0, "t": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)


def _render_comparison(original_df: pd.DataFrame, anonymized_df: pd.DataFrame):
    """Render before/after comparison."""
    tab1, tab2 = st.tabs(["📋 Original Data", "🎭 Anonymized Data"])

    with tab1:
        st.dataframe(original_df.head(10), use_container_width=True)

    with tab2:
        st.dataframe(anonymized_df.head(10), use_container_width=True)

    # Highlight changes
    st.info(
        "💡 **Tip:** Compare the data above to see the anonymization effects. "
        "PII values have been transformed while maintaining data structure."
    )


def _render_action_buttons(result):
    """Render action buttons."""
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Accept Anonymized Data", type="primary", use_container_width=True):
            st.session_state.anonymized_data = result.data
            st.success("✅ Anonymized data accepted!")
            st.info("📌 Next: Go to **Method Comparison** to compare detection methods.")

    with col2:
        if st.button("📥 Download Anonymized CSV", use_container_width=True):
            csv = result.data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="anonymized_data.csv",
                mime="text/csv",
            )

    with col3:
        if st.button("📊 Download Audit Report", use_container_width=True):
            # Create audit report
            audit_data = []
            for record in result.audit.records[:100]:  # Limit to 100
                audit_data.append(
                    {
                        "column": record.column,
                        "row_index": record.row_index,
                        "pii_type": record.pii_type,
                        "strategy": record.strategy,
                        "timestamp": record.timestamp.isoformat(),
                    }
                )

            df_audit = pd.DataFrame(audit_data)
            csv = df_audit.to_csv(index=False)

            st.download_button(
                label="Download Audit CSV",
                data=csv,
                file_name="transformation_audit.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    render()
