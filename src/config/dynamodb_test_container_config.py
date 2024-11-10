# src/config/dynamodb_test_container_config.py

from testcontainers.core.container import DockerContainer
import boto3


class DynamoDBTestContainerConfig:
    def __init__(self):
        # Define container settings for DynamoDB Local
        self.container = (
            DockerContainer("amazon/dynamodb-local")
            .with_bind_ports(8000, 8000)
            .with_command("-jar DynamoDBLocal.jar -sharedDb")
        )

    def start(self):
        # Start the container
        self.container.start()
        self.endpoint_url = f"http://{self.container.get_container_host_ip()}:{self.container.get_exposed_port(8000)}"
        return self

    def create_dynamodb_client(self):
        # Create and return a DynamoDB client for the local container
        return boto3.client(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name="us-east-1",
            aws_access_key_id="dummy-access-key",
            aws_secret_access_key="dummy-secret-key",
        )

    def create_test_table(self, table_name, hash_key="Date"):
        """
        Creates a test table in DynamoDB for testing purposes.

        Args:
            table_name (str): The name of the table to create.
            hash_key (str): The name of the partition key.
        """
        client = self.create_dynamodb_client()
        client.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": hash_key, "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": hash_key, "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        client.get_waiter("table_exists").wait(TableName=table_name)
        return client

    def stop(self):
        # Stop the container
        self.container.stop()
