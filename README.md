# AI CV → Job Matcher

An explainable LLM-powered application that analyzes a CV against a job description using structured information extraction, semantic matching, and evidence-based recommendations.

## 🎯 Project Goal

The goal of this project is to help candidates understand how well their CV matches a specific job opportunity and identify areas that could be improved.

Unlike a simple keyword-based ATS checker, the application uses an LLM to extract structured information from both the CV and job description, then performs explainable matching.

## 🚀 Planned Features

- [x] PDF text extraction
- [ ] Structured CV information extraction
- [ ] Structured job requirement extraction
- [ ] Semantic skill matching
- [ ] Match score
- [ ] Strong / Partial / Missing classification
- [ ] Evidence for each match
- [ ] CV improvement recommendations
- [ ] Streamlit interface
- [ ] Evaluation of matching accuracy

## 🏗️ Architecture

```text
CV PDF ───────────────┐
                      │
                      ▼
                PDF Extraction
                      │
                      ▼
              LLM Information
                 Extraction
                      │
                      ▼
             Candidate Profile
                      │
                      ▼
              Matching Engine
                      ▲
                      │
               Job Requirements
                      ▲
                      │
                LLM Extraction
                      ▲
                      │
               Job Description


