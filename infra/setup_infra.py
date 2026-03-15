import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import ResourceNotFoundError

# Configuration
SUBSCRIPTION_ID = "ee0be9cf-1cd4-4e1c-8f43-5bbec3127b77"
RESOURCE_GROUP = "rushi-azure-infra-rg"
LOCATION = "centralindia"
STORAGE_ACCOUNT = "rushitfstate4559"
CONTAINER_NAME = "tfstate"

# Initialize Clients
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
storage_client = StorageManagementClient(credential, SUBSCRIPTION_ID)

def delete_resources():
    confirm = input(f"Confirm deletion of RG '{RESOURCE_GROUP}' and all its resources? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion aborted.")
        return

    print(f"Deleting Resource Group: {RESOURCE_GROUP}...")
    try:
        poller = resource_client.resource_groups.begin_delete(RESOURCE_GROUP)
        poller.result()
        print("Resource Group deleted successfully.")
    except ResourceNotFoundError:
        print("Resource Group not found.")

def create_resources():
    # 1. Ensure Resource Group exists
    print(f"Checking Resource Group: {RESOURCE_GROUP}...")
    resource_client.resource_groups.create_or_update(RESOURCE_GROUP, {"location": LOCATION})

    # 2. Ensure Storage Account exists
    try:
        storage_client.storage_accounts.get_properties(RESOURCE_GROUP, STORAGE_ACCOUNT)
        print(f"Storage Account '{STORAGE_ACCOUNT}' already exists.")
    except ResourceNotFoundError:
        print(f"Creating Storage Account: {STORAGE_ACCOUNT}...")
        storage_async_operation = storage_client.storage_accounts.begin_create(
            RESOURCE_GROUP,
            STORAGE_ACCOUNT,
            {
                "location": LOCATION,
                "kind": "StorageV2",
                "sku": {"name": "Standard_LRS"},
                "properties": {
                    "allow_blob_public_access": False,
                    "minimum_tls_version": "TLS1_2"
                }
            }
        )
        storage_async_operation.result()

    # 3. Ensure Blob Container exists
    try:
        storage_client.blob_containers.get(RESOURCE_GROUP, STORAGE_ACCOUNT, CONTAINER_NAME)
        print(f"Container '{CONTAINER_NAME}' already exists.")
    except ResourceNotFoundError:
        print(f"Creating Container: {CONTAINER_NAME}...")
        storage_client.blob_containers.create(RESOURCE_GROUP, STORAGE_ACCOUNT, CONTAINER_NAME, {})
    
    print("Infrastructure ready for Terraform.")

if __name__ == "__main__":
    # Check if RG exists to decide between Delete or Run
    try:
        resource_client.resource_groups.get(RESOURCE_GROUP)
        choice = input(f"Resource Group '{RESOURCE_GROUP}' exists. (D)elete or (C)ontinue check? ").lower()
        if choice == 'd':
            delete_resources()
        else:
            create_resources()
    except ResourceNotFoundError:
        create_resources()