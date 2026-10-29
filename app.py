"""
Privacy-Aware Data Engineering Pipeline
Main Streamlit Application Entry Point
"""

import streamlit as st
from pathlib import Path

# Import pages
from src.ui.pages import home, upload, quality, detection, anonymization, comparison
from src.utils.logger import get_logger
from src.utils.error_handler import get_user_friendly_error, UNEXPECTED_ERROR

logger = get_logger(__name__)


# spaCy model is now installed directly from requirements.txt
# No runtime download needed

# Configure page
st.set_page_config(
    page_title="Privacy-Aware Data Engineering Pipeline",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_page = "Home"
    st.session_state.uploaded_file = None
    st.session_state.dataframe = None
    st.session_state.quality_profile = None
    st.session_state.detections = None
    st.session_state.processed_data = None


def main():
    """Main application entry point with error handling."""
    
    try:
        _render_app()
    except Exception as e:
        # Global error handler - prevents showing stack traces to users
        error_msg = get_user_friendly_error(e, UNEXPECTED_ERROR)
        st.error(f"❌ {error_msg}")
        
        # Show a helpful message
        st.info(
            "💡 **Troubleshooting Tips:**\n"
            "- Try refreshing the page\n"
            "- Clear your session state from the sidebar\n"
            "- Check that your data file is valid\n"
            "- Ensure you have followed the workflow order: Upload → Quality → Detection → Anonymization"
        )
        
        # Option to show technical details for debugging (collapsed)
        with st.expander("🔧 Technical Details (for debugging)", expanded=False):
            st.code(f"Error Type: {type(e).__name__}")
            st.text("Check the application logs for full details.")


def _render_app():
    """Render the main application UI."""
    
    # Sidebar navigation
    st.sidebar.title("🔒 Privacy Pipeline")
    st.sidebar.markdown("---")
    
    # Page selection
    pages = {
        "🏠 Home": "Home",
        "📁 Upload Dataset": "Upload",
        "📊 Data Quality": "Quality",
        "🔍 PII Detection": "Detection",
        "🎭 Anonymization": "Anonymization",
        "⚖️ Method Comparison": "Comparison",
        "🔬 Experiments": "Experiments",
        "⚙️ Settings": "Settings",
    }
    
    # Check if current_page was set programmatically (e.g., from Get Started button)
    if 'current_page' in st.session_state:
        # Find the key that corresponds to this page
        page_key = None
        for key, value in pages.items():
            if value == st.session_state.current_page:
                page_key = key
                break
        
        if page_key:
            # Set the default for radio to match
            default_index = list(pages.keys()).index(page_key)
            selection = st.sidebar.radio(
                "Navigate",
                list(pages.keys()),
                index=default_index,
                key="navigation"
            )
        else:
            selection = st.sidebar.radio(
                "Navigate",
                list(pages.keys()),
                key="navigation"
            )
    else:
        selection = st.sidebar.radio(
            "Navigate",
            list(pages.keys()),
            key="navigation"
        )
    
    st.session_state.current_page = pages[selection]
    
    # Render selected page
    if st.session_state.current_page == "Home":
        home.render()
    elif st.session_state.current_page == "Upload":
        upload.render()
    elif st.session_state.current_page == "Quality":
        quality.render()
    elif st.session_state.current_page == "Detection":
        detection.render()
    elif st.session_state.current_page == "Anonymization":
        anonymization.render()
    elif st.session_state.current_page == "Comparison":
        comparison.render()
    else:
        st.info(f"📋 **{st.session_state.current_page}** page - Coming in future milestones!")
        st.markdown("This page will be implemented in upcoming milestones according to the development roadmap.")
    
    # Sidebar footer
    st.sidebar.markdown("---")
    
    # Session management
    if st.sidebar.button("🔄 Clear Session State", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != 'initialized':
                del st.session_state[key]
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 About")
    st.sidebar.info(
        "**Privacy-Aware Data Engineering Pipeline**\n\n"
        "A research-oriented system for PII detection, "
        "anonymization, and experimental evaluation.\n\n"
        "**Version:** 0.1.0 (Milestone 1)\n\n"
        "[GitHub Repository](https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline)"
    )


if __name__ == "__main__":
    main()
