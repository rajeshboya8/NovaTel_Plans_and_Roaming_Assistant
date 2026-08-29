"""Streamlit UI for NovaTel RAG assistant."""

from __future__ import annotations

import streamlit as st

from src.pipeline import RAGPipeline


@st.cache_resource
def get_pipeline() -> RAGPipeline:
    return RAGPipeline()


def main() -> None:
    st.set_page_config(page_title="NovaTel Plans & Roaming Assistant", layout="wide")
    st.title("NovaTel Plans & Roaming Assistant")

    question = st.text_area("Ask a question about plans, tariffs, or roaming:")
    ask = st.button("Ask")

    if ask:
        current_question = question.strip()
        if not current_question:
            st.warning("Please enter a question.")
            return

        with st.spinner("Searching corpus and generating answer..."):
            pipeline = get_pipeline()
            response = pipeline.ask(current_question)

        st.subheader("Answer")
        st.write(response.answer)

        st.subheader("Citations")
        if response.citations:
            for citation in response.citations:
                st.write(
                    f"- {citation.document_name} | {citation.section} | {citation.clause_id}"
                )
        else:
            st.write("No citations available.")

        st.subheader("Applicable Plan/Tariff")
        st.write(response.applicable_plan_or_tariff or "Not identified")

        st.subheader("Charge or Limit")
        st.write(response.charge_or_limit)

        st.subheader("Conditions")
        st.write(response.conditions or "None stated")

        st.subheader("Grounded")
        st.write(str(response.grounded))

        st.subheader("Confidence")
        st.write(response.confidence)


if __name__ == "__main__":
    main()
