$ErrorActionPreference = "Stop"

# Uso:
# .\scripts\git_first_push.ps1 -RepoUrl "https://github.com/TU_USUARIO/decidecasa-agentos.git"

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

git init
git add .
git commit -m "Initial DecideCasa AgentOS"
git branch -M main
git remote add origin $RepoUrl
git push -u origin main
