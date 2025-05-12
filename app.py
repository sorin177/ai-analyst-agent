import os
import streamlit as st
import logging
from dotenv import load_dotenv
import pandas as pd
import json

import mysql.connector

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import generate_schema_summary, run_sql_query, plot_data, AgentOutput

# ─── Setup ─────────────────────────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT") or 3306),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# initialize LLM & agent
llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)
with open("prompt.txt") as f:
    system_prompt = f.read().strip()
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}"),
    ("assistant", "{agent_scratchpad}")
])
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=[])
agent_executor = AgentExecutor(agent=agent, tools=[], verbose=False)

# ─── Initialize Session State ───────────────────────────────────────────────────
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []  # Store all analysis results
if 'new_analysis' not in st.session_state:
    st.session_state.new_analysis = False   # Flag for new analysis

# ─── Helper Functions ────────────────────────────────────────────────────────────
def process_question(question):
    """Process a question and return the results to be stored"""
    with st.spinner("Thinking…"):
        # 1) build schema + question
        schema_ctx = generate_schema_summary(DB_CONFIG)
        full_q = f"Schema:\n{schema_ctx}\n\nQuestion: {question}"

        # 2) run agent
        resp = agent_executor.invoke({"question": full_q})
        output = resp.get("output", "")
        try:
            result = AgentOutput.model_validate_json(output)
            
            # 3) Process SQL queries and generate plots
            viz_data = []
            for viz in result.visualizations:
                try:
                    df = run_sql_query(viz.sql, DB_CONFIG)
                    # Convert DataFrame to dictionary for storage
                    df_dict = df.to_dict('records')
                    
                    # Create and store figure
                    fig = plot_data(df, viz.chart_type, viz.chart_config.get("colors"))
                    
                    viz_data.append({
                        "chart_title": viz.chart_title,
                        "explanation": viz.explanation,
                        "dataframe": df_dict,
                        "chart_type": viz.chart_type,
                        "chart_config": viz.chart_config,
                        "has_figure": fig is not None
                    })
                except Exception as e:
                    logging.exception(e)
                    viz_data.append({
                        "chart_title": viz.chart_title,
                        "explanation": viz.explanation,
                        "error": str(e),
                        "has_figure": False
                    })
            
            # 4) Store all results
            analysis_result = {
                "question": question,
                "insight": result.insight,
                "root_cause_analysis": result.root_cause_analysis,
                "recommendations": result.recommendations,
                "follow_up_questions": result.follow_up_questions,
                "visualizations": viz_data
            }
            
            return analysis_result
            
        except Exception as e:
            logging.exception(e)
            return {
                "question": question,
                "error": str(e),
                "raw_output": output
            }

def display_analysis(analysis):
    """Display a single analysis result"""
    st.markdown(f"## Question: {analysis['question']}")
    
    # Display insight
    st.markdown(f"### 💡 Insight\n{analysis['insight']}")
    if analysis.get('root_cause_analysis'):
        st.markdown(f"**Why?** {analysis['root_cause_analysis']}")
    st.markdown("---")
    
    # Display visualizations
    for viz in analysis.get('visualizations', []):
        st.markdown(f"#### 📊 {viz['chart_title']}")
        st.markdown(f"*{viz['explanation']}*")
        
        if viz.get('error'):
            st.error(f"❌ Error: {viz['error']}")
            continue
            
        if viz.get('has_figure'):
            # Recreate the figure from stored data
            df = pd.DataFrame(viz['dataframe'])
            fig = plot_data(df, viz['chart_type'], viz['chart_config'].get('colors'))
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write(df)  # fallback to table
        else:
            # If no figure, just show the data
            df = pd.DataFrame(viz['dataframe'])
            st.write(df)
    
    # Display recommendations & follow-ups
    if analysis.get('recommendations'):
        st.markdown(f"### ✅ Recommendations\n{analysis['recommendations']}")
    
    if analysis.get('follow_up_questions'):
        st.markdown("### 🔄 Follow-Up Questions")
        for q in analysis['follow_up_questions']:
            st.write(f"- {q}")
    
    st.markdown("---")

# ─── Streamlit UI ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Business Insights Agent", layout="wide")
st.title("🧠 Business Insights Agent")

# Main input at the top
initial_question = st.text_area("Ask a business question about your Employees DB:", 
                               height=100, 
                               key="top_question_input")

if st.button("Analyze", key="top_analyze_button"):
    if not initial_question.strip():
        st.warning("Please enter a question.")
    else:
        # Process question and store results
        analysis = process_question(initial_question)
        st.session_state.analysis_results.append(analysis)
        st.session_state.new_analysis = True
        st.rerun()  # Changed from experimental_rerun() to rerun()

# Display all previous analyses
for analysis in st.session_state.analysis_results:
    display_analysis(analysis)

# Follow-up question input at the bottom (only shown after initial question is answered)
if st.session_state.analysis_results:
    # Add a follow-up question section at the bottom
    follow_up = st.text_area("Ask another question:", 
                           height=100, 
                           key="bottom_question_input")
    
    if st.button("Analyze", key="bottom_analyze_button"):
        if not follow_up.strip():
            st.warning("Please enter a question.")
        else:
            # Process follow-up and store results
            analysis = process_question(follow_up)
            st.session_state.analysis_results.append(analysis)
            st.session_state.new_analysis = True
            st.rerun()  # Changed from experimental_rerun() to rerun()