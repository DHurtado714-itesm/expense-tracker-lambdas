import os
from handler import NotionManager, NotionProperties


def update_income_handler(event, context):
    notion_manager = NotionManager()

    database_id = os.getenv("NOTION_DB_ID_INCOME")
    properties_to_retrieve = {
        "id": NotionProperties.ID,
        "Local Amount": NotionProperties.NUMBER,
        "Currencies": NotionProperties.SELECT,
    }
    filter_body = {
        "filter": {
            "or": [
                {
                    "property": "Date",
                    "date": {"equals": notion_manager.today_iso},
                }
            ]
        }
    }

    notion_manager.update_pages(
        database_id=database_id,
        properties_to_retrieve=properties_to_retrieve,
        filter_body=filter_body,
        update_field="Amount",
    )
