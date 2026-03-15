terraform {
  required_version = ">= 1.5.0"

  # 1. Backend Configuration (Storage created by your Python script)
  backend "azurerm" {
    resource_group_name  = "rushi-azure-infra-rg"
    storage_account_name = "rushitfstate4559"
    container_name       = "tfstate"
    key                  = "dev.terraform.tfstate"
  }

  # 2. Required Providers and Versions
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90" # Latest stable v3 features
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.47" # Latest for Entra ID management
    }
  }
}

# 3. Provider Configurations
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

provider "azuread" {
  # No extra config needed if you are logged in via Azure CLI
}