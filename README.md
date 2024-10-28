# 📈 Exchange Rate Tracker Lambda Project

This project tracks exchange rates and updates expense and income databases in Notion using AWS Lambda functions, triggered on daily and bi-weekly schedules via the Serverless framework.

## 📝 Project Overview

The **Exchange Rate Tracker** Lambda functions fetch the latest exchange rates and update values in the specified Notion databases. The project uses `Python 3.9`, `AWS Lambda`, `Serverless Framework`, and integrates with the Notion API to update values automatically.

## 🚀 Features

- 🕒 **Automated Updates**: Tracks and updates expense and income databases on scheduled intervals.
- 💹 **Real-Time Exchange Rates**: Fetches up-to-date exchange rates to calculate currency equivalencies.
- 💻 **Serverless Deployment**: Easily deploy, update, and manage AWS Lambda functions with the Serverless framework.
- 📒 **Notion Integration**: Writes calculated values directly to your Notion databases.

## 📦 Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/exchange-rate-tracker
    cd exchange-rate-tracker
    ```

2. **Set up virtual environment and dependencies**:

    ```bash
    python3.9 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure AWS Credentials**:

   Ensure you have the necessary AWS credentials and Notion API token.

## ⚙️ Configuration

1. **Set up Notion Secrets**: 

    Update your `.env` file with your Notion API token and Database IDs:

    ```env
    NOTION_TOKEN=your_notion_token
    NOTION_DB_ID_EXPENSES=your_expenses_db_id
    NOTION_DB_ID_INCOMES=your_incomes_db_id
    ```

2. **AWS Lambda Permissions**:

   Ensure your AWS IAM Role has permissions for Lambda, CloudWatch, and Serverless deployments.

## 🚀 Deployment

1. **Deploy with Serverless**:

    ```bash
    sls deploy
    ```

2. **Invoke Locally**:

    Test each function locally with:

    ```bash
    sls invoke local -f updateExpense
    sls invoke local -f updateIncome
    ```

## 🛠️ Usage

This project includes two Lambda functions:
  
- **updateExpense**: Updates the Notion expense database daily with current exchange rates.
- **updateIncome**: Updates the Notion income database every 15 days with current exchange rates.

## 📆 Scheduling

The functions are scheduled as follows:

- **Expenses**: Every day.
- **Incomes**: Every day.

## 💡 Troubleshooting

- If encountering `No module named 'requests'`, be sure to deploy dependencies packaged with your function.
- For **Python version errors**, verify that Python 3.9 is in your PATH and configured in Serverless.

## 🖊️ Notes

Remember to keep your AWS and Notion credentials secure and rotate them regularly.

---

Enjoy using the **Exchange Rate Tracker** and making currency updates effortless! 😊