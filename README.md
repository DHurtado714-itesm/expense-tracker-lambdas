# 📈 Exchange Rate Tracker Lambda Project

This project tracks exchange rates, updates expense and income databases in Notion, and saves historical exchange rates in DynamoDB using AWS Lambda functions, triggered on daily and bi-weekly schedules via the Serverless framework.

## 📝 Project Overview

The **Exchange Rate Tracker** Lambda functions fetch the latest exchange rates, update values in the specified Notion databases, and store historical exchange rates in DynamoDB for reference. The project uses `Python 3.9`, `AWS Lambda`, `DynamoDB`, `Serverless Framework`, and integrates with the Notion API to update values automatically.

## 🚀 Features

- 🕒 **Automated Updates**: Tracks and updates expense and income databases on scheduled intervals.
- 💹 **Real-Time Exchange Rates**: Fetches up-to-date exchange rates to calculate currency equivalencies.
- 🗃️ **Historical Storage in DynamoDB**: Stores daily exchange rates for future reference or analysis.
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

1. **Set up Notion and DynamoDB Secrets**:

   Update your `.env` file with your Notion API token, Database IDs, and DynamoDB configuration:

   ```env
   NOTION_TOKEN=your_notion_token
   NOTION_DB_ID_EXPENSES=your_expenses_db_id
   NOTION_DB_ID_INCOMES=your_incomes_db_id
   EXCHANGE_RATE_TABLE_NAME=your_dynamodb_table_name
   ```

2. **AWS Lambda Permissions**:

   Ensure your AWS IAM Role has permissions for Lambda, CloudWatch, DynamoDB, and Serverless deployments.

3. **Set Up DynamoDB Table**:

   Create a DynamoDB table for storing exchange rates. For example:

   - **Table Name**: `ExchangeRates` (or as defined in `EXCHANGE_RATE_TABLE_NAME`)
   - **Primary Key**: `Date` (String type, in `YYYY-MM-DD` format)

   This table will store historical exchange rates as `Date` keys, with rates stored as a dictionary of currency pairs.

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
   sls invoke local -f createExchangeRateEntry  # For storing exchange rates in DynamoDB
   ```

## 🛠️ Usage

This project includes three Lambda functions:

- **updateExpense**: Updates the Notion expense database daily with current exchange rates.
- **updateIncome**: Updates the Notion income database every 15 days with current exchange rates.
- **createExchangeRateEntry**: Fetches and stores the latest exchange rates in DynamoDB, enabling historical access to exchange rates.

## 📆 Scheduling

The functions are scheduled as follows:

- **Expenses**: Every day.
- **Incomes**: Every 15 days.
- **Exchange Rate Entry**: Every day.

## 🔄 DynamoDB Storage and Retrieval

The `createExchangeRateEntry` function saves exchange rates to DynamoDB daily. Other functions (such as `updateExpense` and `updateIncome`) can retrieve historical exchange rates from DynamoDB to update Notion with accurate currency values based on prior exchange rates.

- **Storing Rates**: The function stores exchange rates in DynamoDB with the `Date` as the primary key and currency rates in a nested dictionary format.
- **Retrieving Rates**: Lambda functions retrieve exchange rates by date and currency, ensuring data consistency for past expense and income entries.

## 💡 Troubleshooting

- If encountering `No module named 'requests'`, be sure to deploy dependencies packaged with your function.
- For **Python version errors**, verify that Python 3.9 is in your PATH and configured in Serverless.
- Ensure that the DynamoDB table is correctly set up with `Date` as the primary key for successful data storage and retrieval.

## 🖊️ Notes

Remember to keep your AWS and Notion credentials secure and rotate them regularly. Regularly monitor DynamoDB usage to manage costs effectively, especially if historical rates are stored for extended periods.

---

Enjoy using the **Exchange Rate Tracker** and making currency updates effortless! 😊
