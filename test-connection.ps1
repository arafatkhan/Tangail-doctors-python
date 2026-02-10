$password = 'arafat18843'
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ('root', $securePassword)

# Test SSH connection
Write-Host "Testing SSH connection..." -ForegroundColor Yellow
ssh root@217.216.73.118 "echo 'Connection successful'"
