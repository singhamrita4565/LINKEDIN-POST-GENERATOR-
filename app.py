import streamlit as st

# Import the compiled LangGraph application
from iterative import app


# -----------------------------
# Streamlit Page Configuration
# -----------------------------

st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------

st.title("💼 LinkedIn Post Generator")

st.write(
    "This tool drafts a LinkedIn post, reviews it, and iterates "
    "until it is publish-ready."
)

st.divider()


# -----------------------------
# User Input
# -----------------------------

topic = st.text_area(
    "What topic do you want a LinkedIn post about?",
    placeholder="Example: The impact of AI on software developers",
    height=120
)


# -----------------------------
# Generate Button
# -----------------------------

generate = st.button(
    "Generate LinkedIn Post",
    type="primary",
    use_container_width=True
)


# -----------------------------
# Run LangGraph
# -----------------------------

if generate:

    if not topic.strip():

        st.warning("Please enter a topic first.")

    else:

        # Initial state required by State in iterative.py
        initial_state = {
            "topic": topic.strip(),
            "messages": [],
            "draft": "",
            "review_feedback": "",
            "is_approved": False,
            "attempt": 0
        }

        # Run LangGraph
        with st.spinner(
            "Writing, searching, and reviewing your LinkedIn post..."
        ):

            try:

                result = app.invoke(initial_state)

                # -----------------------------
                # Success
                # -----------------------------

                st.success("Generation completed!")

                st.divider()

                # -----------------------------
                # Final Post
                # -----------------------------

                st.subheader("📝 Final LinkedIn Post")

                st.text_area(
                    "Generated post",
                    value=result["draft"],
                    height=350,
                    disabled=True
                )

                # -----------------------------
                # Verdict + Attempts
                # -----------------------------

                st.divider()

                verdict = (
                    "APPROVED"
                    if result["is_approved"]
                    else "REJECTED"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Reviewer Verdict",
                        verdict
                    )

                with col2:
                    st.metric(
                        "Attempts",
                        result["attempt"]
                    )

                # -----------------------------
                # Reviewer Feedback
                # -----------------------------

                if not result["is_approved"]:

                    st.subheader("💬 Reviewer Feedback")

                    st.info(
                        result["review_feedback"]
                    )

            except Exception as e:

                st.error(
                    f"Error while generating the post: {e}"
                )

                st.exception(e)


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "Powered by LangGraph + Groq + Tavily + Streamlit"
)