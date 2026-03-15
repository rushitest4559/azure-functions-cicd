output "client_id" {
  description = "The Application (client) ID for the GitHub Actions OIDC application"
  value       = azuread_application.github_oidc.client_id
}

output "tenant_id" {
  description = "The Directory (tenant) ID for the Azure account"
  value       = data.azurerm_client_config.current.tenant_id
}

output "subscription_id" {
  description = "The Subscription ID where the resources are deployed"
  value       = data.azurerm_client_config.current.subscription_id
}

output "service_principal_object_id" {
  description = "The Object ID of the Service Principal"
  value       = azuread_service_principal.github_sp.object_id
}