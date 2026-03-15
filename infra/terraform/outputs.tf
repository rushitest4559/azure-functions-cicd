output "function_url" {
  description = "The URL of the deployed Python function"
  value       = "https://${module.function_app.default_hostname}/api/discount"
}

output "function_app_name" {
  value = module.function_app.function_app_name
}

output "gh_oidc_client_id" {
  value = module.auth.client_id
}

output "gh_oidc_tenant_id" {
  value = module.auth.tenant_id
}

output "gh_oidc_subscription_id" {
  value = module.auth.subscription_id
}