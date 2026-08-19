import streamlit as st

from parser import extract_text
from extractor import (
    extract_candidate_profile,
    extract_job_requirements
)
from matcher import match_candidate_to_job


st.set_page_config(
    page_title="CV Job Matcher",
    page_icon="📄",
    layout="wide"
)


st.title("📄 CV Job Matcher")
st.write(
    "Upload your CV and a job description to analyze "
    "your compatibility using LLMs and semantic matching."
)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Your CV")
    cv_file = st.file_uploader(
        "Upload your CV",
        type=["pdf"],
        key="cv"
    )

with col2:
    st.subheader("Job Description")
    job_file = st.file_uploader(
        "Upload the job description",
        type=["pdf"],
        key="job"
    )


if st.button("🔍 Analyze Match", type="primary"):

    if cv_file is None or job_file is None:
        st.warning("Please upload both your CV and the job description.")

    else:

        with st.spinner("Analyzing your CV and the job description..."):

            # Save uploaded CV temporarily
            with open("temp_cv.pdf", "wb") as f:
                f.write(cv_file.getbuffer())

            # Save uploaded job temporarily
            with open("temp_job.pdf", "wb") as f:
                f.write(job_file.getbuffer())

            # Extract text
            cv_text = extract_text("temp_cv.pdf")
            job_text = extract_text("temp_job.pdf")

            # LLM extraction
            candidate = extract_candidate_profile(cv_text)
            job = extract_job_requirements(job_text)

            # Matching
            match = match_candidate_to_job(
                candidate,
                job
            )

        st.success("Analysis complete!")

        # Overall score
        st.subheader("Overall Match")

        score = match["overall_score"]

        st.metric(
            "Compatibility Score",
            f"{score}%"
        )

        # Required skills
        st.subheader("🎯 Required Skills")

        for item in match["required_skills"]:

            score_value = item["score"]

            if score_value >= 0.75:
                icon = "🟢"
            elif score_value >= 0.50:
                icon = "🟡"
            else:
                icon = "🔴"

            st.write(
                f"{icon} **{item['requirement']}** "
                f"→ {item['candidate_match']} "
                f"({score_value:.0%})"
            )

        # Experience
        st.subheader("💼 Experience")

        for item in match["experience"]:

            st.write(
                f"**{item['requirement']}** "
                f"→ {item['candidate_match']} "
                f"({item['score']:.0%})"
            )

        # Education
        st.subheader("🎓 Education")

        for item in match["education"]:

            st.write(
                f"**{item['requirement']}** "
                f"→ {item['candidate_match']} "
                f"({item['score']:.0%})"
            )

        # Languages
        st.subheader("🌐 Languages")

        for item in match["languages"]:

            st.write(
                f"**{item['requirement']}** "
                f"→ {item['candidate_match']} "
                f"({item['score']:.0%})"
            )

        # Preferred skills
        if match["preferred_skills"]:

            st.subheader("⭐ Preferred Skills")

            for item in match["preferred_skills"]:

                st.write(
                    f"**{item['requirement']}** "
                    f"→ {item['candidate_match']} "
                    f"({item['score']:.0%})"
                )
