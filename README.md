# Business Insights Agent

An intelligent business analytics platform powered by LLMs that translates natural language questions into SQL queries, creates visualizations, and provides actionable insights.

![Business Insights Agent Demo](demo_screenshot.png)

## Features

- 💬 **Natural Language Interface**: Ask questions in plain English about your business data
- 📊 **Automatic Visualizations**: Generates appropriate charts based on query results
- 🔍 **Root Cause Analysis**: Identifies underlying factors contributing to business trends
- 📈 **Actionable Recommendations**: Suggests next steps based on data insights
- 🔄 **Follow-up Questions**: Recommends additional queries to deepen your analysis

## Tech Stack

- **Backend**: Python, MySQL, LangChain
- **LLM Integration**: OpenAI GPT-4
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Frontend**: Streamlit

## How It Works

1. User asks a business question in natural language
2. LLM agent interprets the question and generates appropriate SQL queries
3. Queries are executed against the MySQL database
4. Results are processed and visualized
5. LLM provides insights, analyses, and recommendations based on the data

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL database with your business data
- OpenAI API key

### Installation

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/business-insights-agent.git
   cd business-insights-agent
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration
   ```
   OPENAI_API_KEY=your_openai_api_key 
   DB_HOST=your_db_host
   DB_PORT=your_db_host
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   ```

### Running the Application

#### Streamlit Web Interface
```bash
streamlit run app.py
```

#### Command Line Interface
```bash
python main.py
```

## Project Structure

```
├── app.py              # Streamlit web interface
├── main.py             # Command line interface
├── tools.py            # Core functionality, SQL processing, visualization
├── prompt.txt          # System prompt for the LLM agent
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Demo

Soon to be implemented

## Future Improvements

- Support for additional databases (PostgreSQL, SQLite, etc.)
- Custom visualization options
- Data export functionality
- User authentication and access controls
- Multi-tenant support for multiple databases

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Nicholas Tarazi - Nicholas.Tarazo7@gmail.com

Project Link: [https://github.com/tnickster/ai-analyst-agent](https://github.com/tnickster/ai-analyst-agent)