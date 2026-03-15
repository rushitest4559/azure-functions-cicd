data "azurerm_client_config" "current" {}

resource "azuread_application" "github_oidc" {
  display_name = "github-actions-oidc-app"
}

resource "azuread_service_principal" "github_sp" {
  client_id = azuread_application.github_oidc.client_id
}

resource "azuread_application_federated_identity_credential" "github_federated" {
  application_id = azuread_application.github_oidc.id
  display_name   = "github-actions-deploy"
  description    = "Deploy to Azure Functions from GitHub Actions"
  audiences      = ["api://AzureADTokenExchange"]
  issuer         = "https://token.actions.githubusercontent.com"

  # This limits access to ONLY your specific repo and branch
  subject = "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${var.github_branch}"
}

resource "azurerm_role_assignment" "deploy_role" {
  scope                = "/subscriptions/${data.azurerm_client_config.current.subscription_id}/resourceGroups/${var.resource_group_name}"
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.github_sp.object_id
}
