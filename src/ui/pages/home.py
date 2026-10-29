"""
Home page - Overview and introduction.
"""

import streamlit as st


def render():
    """Render the home page."""

    # Hero section
    st.title("🔒 Privacy-Aware Data Engineering Pipeline")
    st.markdown(
        """
        ### Build • Detect • Anonymize • Evaluate

        A research-oriented data engineering and privacy preservation system that demonstrates
        PII detection, anonymization, and experimental comparison of detection methods.
        """
    )

    st.markdown("---")

    # What this application does
    st.header("📋 What This Application Does")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **📊 Data Engineering**
            - Ingest CSV and JSON files
            - Validate data quality
            - Profile and clean datasets
            - Handle missing values
            - Detect duplicates
            """
        )

    with col2:
        st.markdown(
            """
            **🔍 PII Detection**
            - Rule-based detection
            - NLP-assisted detection
            - Multiple PII categories
            - Configurable strategies
            - Confidence scoring
            """
        )

    with col3:
        st.markdown(
            """
            **🎭 Privacy Transformation**
            - Masking strategies
            - Redaction operations
            - Pseudonymization
            - Generalization
            - Audit trails
            """
        )

    st.markdown("---")

    # Features overview
    st.header("✨ Key Features")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.subheader("🔬 Research & Evaluation")
        st.markdown(
            """
            - Comparative evaluation of detection methods
            - Synthetic dataset generation with ground truth
            - Precision, recall, F1-score metrics
            - Confusion matrices and error analysis
            - Reproducible experimental protocol
            """
        )

        st.subheader("📈 Professional Interface")
        st.markdown(
            """
            - Interactive dashboards and visualizations
            - Multi-page workflow
            - Real-time processing feedback
            - Downloadable reports and datasets
            - Clean, intuitive design
            """
        )

    with feature_col2:
        st.subheader("🛡️ Privacy-First Design")
        st.markdown(
            """
            - No real PII used in development
            - No PII logged or persisted
            - Input validation and sanitization
            - Secure file handling
            - Transparent processing
            """
        )

        st.subheader("🧪 PII Categories Detected")
        st.markdown(
            """
            - **Rule-Based**: Email, Phone, SSN, Credit Card, IP Address
            - **NLP-Assisted**: Person Names, Organizations, Locations
            - Configurable detection thresholds
            - Method comparison and analysis
            """
        )

    st.markdown("---")

    # Quick start guide
    st.header("🚀 Quick Start Guide")

    st.markdown(
        """
        Follow these steps to process your dataset:

        1. **📁 Upload Dataset** - Navigate to Upload page and select your CSV or JSON file
        2. **📊 Review Quality** - Check data quality report and optionally clean data
        3. **🔍 Detect PII** - Choose detection method (rule-based or NLP) and run detection
        4. **🎭 Anonymize** - Configure transformation strategies and apply anonymization
        5. **📥 Export Results** - Download processed dataset and reports
        6. **⚖️ Compare Methods** - View side-by-side comparison of detection approaches
        7. **🔬 Run Experiments** - Execute controlled experiments with synthetic data
        """
    )

    # Get started button
    st.markdown("###  ")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📁 Get Started - Upload Dataset", use_container_width=True, type="primary", key="get_started_btn"):
            # Set the current page in session state
            st.session_state.current_page = "Upload"
            # Force rerun to navigate
            st.rerun()

    st.markdown("---")

    # Research contribution
    st.header("🔬 Research Contribution")

    st.markdown(
        """
        This project conducts a comparative evaluation of PII detection methods:

        **Research Question:**
        > How do rule-based and NLP-assisted PII detection methods compare in precision,
        > recall, F1-score, and processing efficiency on a controlled dataset containing
        > structured records and unstructured text?

        **Methodology:**
        - Synthetic dataset generation with ground truth labels
        - Quantitative metrics: precision, recall, F1-score, processing time
        - Fair comparison: same data, same evaluation criteria
        - Reproducible protocol: fixed seeds, versioned dependencies
        - Error analysis: qualitative insights into failure modes
        """
    )

    st.markdown("---")

    # Important disclaimers
    st.header("⚠️ Important Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.warning(
            """
            **⚠️ Research Tool - Not Production Ready**

            This application is designed for research and portfolio demonstration purposes.
            It is NOT intended for production use with real sensitive data without additional
            security review and compliance validation.
            """
        )

    with info_col2:
        st.info(
            """
            **ℹ️ Limitations**

            - English language only
            - Limited PII categories
            - <100K rows recommended
            - Not 100% detection accuracy
            - Local processing only
            """
        )

    st.markdown("---")

    # Footer
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p><strong>Privacy-Aware Data Engineering Pipeline</strong></p>
            <p>Version 0.1.0 (Milestone 1) | Built with Streamlit, pandas, Presidio, and spaCy</p>
            <p>
                <a href="https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline" target="_blank">
                    GitHub Repository
                </a> |
                <a href="https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline/blob/main/README.md" target="_blank">
                    Documentation
                </a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
