# Auditoria de Seguranca — Varredura de Secrets

**Data:** 2026-08-20
**Realizado por:** Claude Fable 5 (Anthropic), via Claude Code, a pedido de Ewerton Uchoa
**Escopo:** este repositorio, como parte de uma auditoria abrangendo os 14 repositorios da conta `Uchoavf` no GitHub

## Metodologia

- [gitleaks](https://github.com/gitleaks/gitleaks) 8.30.1 sobre **todo o historico de commits** deste repositorio (`git log --all`), nao apenas os arquivos na branch atual
- Busca por nomes de arquivos sensiveis versionados em qualquer commit do historico (`.env`, `*.pem`, `*.key`, `credentials*.json`, `.npmrc`, `.aws/`, chaves SSH privadas), mesmo que removidos depois
- Regex de alta precisao para padroes conhecidos de credenciais: AWS (`AKIA...`), GitHub PAT (`ghp_`/`gho_`/`github_pat_`), OpenAI/Anthropic (`sk-...`), Slack (`xox...`), Google (`AIza...`), chaves privadas PEM/SSH, connection strings com senha embutida (`postgres://`, `mongodb://` etc.)
- Verificacao de credenciais hardcoded em arquivos de configuracao (`.yml`, `.json`, `.toml`, `.ini`, `docker-compose*`, etc.)

## Resultado

Nenhum secret encontrado no historico completo do repositorio.

## Medidas preventivas aplicadas

- `.gitignore` criado (o repositorio nao tinha nenhum), bloqueando `.env`, `.env.*`, `*.pem`, `*.key`, `*.jks`, `*.keystore` e `credentials*.json`

## Recomendacoes adicionais (acao do usuario)

- Ativar o [GitHub Push Protection](https://github.com/settings/security_analysis) ("Push protection for yourself") — bloqueia qualquer push com secrets conhecidos em todos os repositorios, publicos e privados
- Instalar o pre-commit localmente nos clones de uso diario: `pipx install pre-commit` e depois `pre-commit install` dentro do repositorio

---
*Este documento registra uma auditoria pontual realizada em 2026-08-20. Para o estado de seguranca atual do repositorio, consulte o historico de commits e as execucoes de CI mais recentes.*
