import os

from src.libs.notion_manager_provider import NotionManager, NotionProperties


def update_expenses_handler(event, context):
    notion_manager = NotionManager()

    database_id = os.getenv("NOTION_DB_ID_EXPENSES")
    properties_to_retrieve = {
        "id": NotionProperties.ID,
        "Local Amount": NotionProperties.NUMBER,
        "Currencies": NotionProperties.SELECT,
        "Date": NotionProperties.DATE,
        "Amount": NotionProperties.NUMBER,
    }
    filter_body = {
        "filter": {
            "property": "Amount",
            "number": {
                "is_empty": True,
            },
        }
    }

    notion_manager.update_pages(
        database_id=database_id,
        properties_to_retrieve=properties_to_retrieve,
        filter_body=filter_body,
        update_field="Amount",
    )
