# AI Analyst Agent 🤖📊

![AI Analyst Agent](https://img.shields.io/badge/Release-v1.0.0-blue.svg)  
[![GitHub Releases](https://img.shields.io/badge/Check%20Releases-Here-brightgreen)](https://github.com/sorin177/ai-analyst-agent/releases)

Welcome to the **AI Analyst Agent** repository! This project aims to simplify business data analysis by allowing users to ask questions in plain English. With the power of AI, you can generate SQL queries, create visualizations, and receive insights—all without needing any SQL knowledge.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Natural Language Queries**: Ask questions about your business data in plain English.
- **Automatic SQL Generation**: Receive SQL queries generated based on your questions.
- **Visualizations**: Get graphical representations of your data with ease.
- **AI Insights**: Benefit from AI-powered recommendations to enhance decision-making.
- **User-Friendly Interface**: No technical expertise required to get started.

## Technologies Used

This project incorporates a range of technologies to deliver its features effectively:

- **Python**: The primary programming language for backend development.
- **MySQL**: The database management system used for data storage and retrieval.
- **Streamlit**: A framework for creating interactive web applications.
- **Plotly**: A library for generating dynamic visualizations.
- **OpenAI's GPT-4**: The AI model that powers natural language processing.
- **LangChain**: A framework that helps manage and chain together different language models.

## Installation

To get started with the AI Analyst Agent, follow these steps:

1. **Clone the Repository**: Use the following command to clone the repository to your local machine.
   ```bash
   git clone https://github.com/sorin177/ai-analyst-agent.git
   ```

2. **Navigate to the Directory**: Change to the project directory.
   ```bash
   cd ai-analyst-agent
   ```

3. **Install Requirements**: Install the necessary packages using pip.
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**: Configure your MySQL database and update the connection settings in the `config.py` file.

5. **Run the Application**: Start the Streamlit application with the following command.
   ```bash
   streamlit run app.py
   ```

Now, you can access the application at `http://localhost:8501`.

## Usage

Once the application is running, you will see a user-friendly interface. Here's how to use it:

1. **Ask a Question**: Type your question in the input box. For example, "What are my sales for the last quarter?"

2. **Receive SQL Query**: The system will generate the SQL query based on your question.

3. **View Visualizations**: After executing the query, you will see visualizations that represent your data.

4. **Get Insights**: The AI will provide insights and recommendations based on the analysis.

## Examples

Here are some examples of questions you can ask:

- "What is the average revenue per customer?"
- "Show me the sales trend over the last year."
- "Which products are the best sellers this month?"

The AI Analyst Agent will interpret these questions and generate the necessary SQL queries and visualizations.

## Contributing

We welcome contributions to improve the AI Analyst Agent. To contribute:

1. **Fork the Repository**: Click the "Fork" button at the top right of the page.

2. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Make Changes**: Implement your changes.

4. **Commit Your Changes**: Commit your changes with a clear message.
   ```bash
   git commit -m "Add your message here"
   ```

5. **Push to Your Fork**: Push your changes to your forked repository.
   ```bash
   git push origin feature/YourFeature
   ```

6. **Create a Pull Request**: Go to the original repository and click "New Pull Request."

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to reach out:

- **GitHub**: [sorin177](https://github.com/sorin177)
- **Email**: your-email@example.com

Check the [Releases](https://github.com/sorin177/ai-analyst-agent/releases) section for the latest updates and downloads.

Thank you for your interest in the AI Analyst Agent! We hope this tool helps you make data-driven decisions effortlessly.