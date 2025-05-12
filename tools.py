import pandas as pd
import plotly.express as px
import mysql.connector
from pydantic import BaseModel
from typing import List, Literal

# Generate schema summary
def generate_schema_summary(db_config: dict) -> str:
    """
    Connects to the MySQL database and returns a summary of tables and their columns.
    """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    summary = ""
    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = [col[0] for col in cursor.fetchall()]
        summary += f"Table `{table}`: {', '.join(columns)}\n"

    cursor.close()
    conn.close()
    return summary.strip()

# Run SQL query and return DataFrame
def run_sql_query(sql: str, db_config: dict) -> pd.DataFrame:
    """
    Executes the provided SQL query using the given DB config and returns the result as a DataFrame
    """
    conn = mysql.connector.connect(**db_config)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# Auto suggest visualization type
def choose_visualization(df: pd.DataFrame) -> str:
    """
    Chooses an appropriate chart type based on the DataFrame shape and content
    """
    if df.empty:
        return 'table'

    first_col = df.columns[0].lower()
    if 'date' in first_col or pd.api.types.is_datetime64_any_dtype(df[first_col]):
        return 'line'
    elif df.shape[1] == 2 and df.iloc[:,1].sum() <= 100:
        return 'pie'
    elif df.shape[1] == 2:
        return 'bar'
    elif df.shape[1] == 3:
        return 'grouped_bar'
    return 'table'

# Plot function using Plotly
def plot_data(df: pd.DataFrame, chart_type: str, colors: List[str] = None):
    """
    Creates and returns a Plotly figure object for the specified chart type.
    Supports 'line', 'bar', 'grouped_bar', 'pie', 'scatter', etc
    
    Returns:
        A Plotly figure object or None if chart type not supported or data empty
    """
    if df.empty:
        return None

    if colors is None:
        colors = px.colors.qualitative.Plotly

    fig = None
    if chart_type == 'line':
        # Handle multiple y columns by melting
        if df.shape[1] > 2:
            df_long = df.melt(id_vars=df.columns[0], var_name='variable', value_name='value')
            fig = px.line(df_long, x=df.columns[0], y='value', color='variable',
                          color_discrete_sequence=colors)
        else:
            fig = px.line(df, x=df.columns[0], y=df.columns[1],
                          color_discrete_sequence=colors)

    elif chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1],
                     color_discrete_sequence=[colors[0]])

    elif chart_type == 'grouped_bar':
        # Expects columns: [x, series, value]
        fig = px.bar(df, x=df.columns[0], y=df.columns[2], color=df.columns[1],
                     barmode='group', color_discrete_sequence=colors)

    elif chart_type == 'pie':
        fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                     color_discrete_sequence=colors)

    elif chart_type == 'scatter':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1],
                         color_discrete_sequence=colors)

    else:
        return None

    fig.update_layout(template='plotly_white')
    return fig  # Return the figure instead of showing it

# Pydantic models for agent output
class Visualization(BaseModel):
    sql: str
    chart_type: Literal[
        'bar', 'grouped_bar', 'line', 'pie', 'scatter',
        'histogram', 'box', 'heatmap', 'treemap',
        'sunburst', 'waterfall', 'gantt', 'table'
    ]
    chart_title: str
    chart_config: dict
    explanation: str

class AgentOutput(BaseModel):
    visualizations: List[Visualization]
    insight: str
    root_cause_analysis: str = ''
    recommendations: str = ''
    follow_up_questions: List[str] = []