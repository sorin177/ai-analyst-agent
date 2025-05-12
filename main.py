import os
import logging
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import generate_schema_summary, plot_data, AgentOutput

# Logging
logging.basicConfig(level=logging.INFO)

# Load .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database config
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT") or 3306),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# LLM & Agent Setup
llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)

with open("prompt.txt") as f:
    system_prompt = f.read().strip()

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{question}"),
    ("assistant", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=[])
agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)

# Safe SQL runner
def run_sql_query(sql: str) -> pd.DataFrame:
    lowered = sql.lower()
    if any(cmd in lowered for cmd in ("drop ", "delete ", "alter ")):
        raise ValueError("Destructive commands are not allowed.")
    conn = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# Main
if __name__ == "__main__":
    print("Welcome to the Business Insights Agent.")
    while True:
        user_q = input("\n📥 Ask a business question (or 'exit' to quit): ")
        if user_q.strip().lower() == "exit":
            print("Goodbye!")
            break

        # 1) Inject schema context
        schema_ctx = generate_schema_summary(DB_CONFIG)
        full_q = f"Schema:\n{schema_ctx}\n\nQuestion: {user_q}"

        # 2) Send to agent
        resp = agent_executor.invoke({"question": full_q})
        output = resp.get("output", "")
        if not output:
            logging.warning("No output from agent.")
            continue

        # 3) Parse into our model
        try:
            result = AgentOutput.model_validate_json(output)
        except Exception:
            logging.exception("Failed to parse agent output")
            print("Couldn't interpret the agent response.")
            continue

        # 4) Show Insight
        logging.info("\n💡 Insight:\n%s", result.insight)

        # 5) For each viz run SQL and render
        for viz in result.visualizations:
            logging.info("\n📊 Running SQL:\n%s", viz.sql)
            try:
                df = run_sql_query(viz.sql)
            except Exception as e:
                logging.error("SQL error", exc_info=e)
                print("Error executing SQL:", e)
                continue

            logging.info("🔎 Explanation: %s", viz.explanation)
            fig = plot_data(df, viz.chart_type, colors=viz.chart_config.get("colors"))
            if fig:
                plt.figure(figsize=(10, 6))
                fig.show()  # For command line interface

        # 6) Recommendations and follow ups
        if result.recommendations:
            logging.info("\n✅ Recommendations:\n%s", result.recommendations)
        if result.follow_up_questions:
            logging.info("\n🔄 Follow-Up Questions:")
            for fq in result.follow_up_questions:
                logging.info("- %s", fq)