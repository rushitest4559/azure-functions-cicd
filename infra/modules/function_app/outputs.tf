output "function_app_name" {
  value = azurerm_linux_function_app.python_func.name
}

output "default_hostname" {
  value = azurerm_linux_function_app.python_func.default_hostname
}