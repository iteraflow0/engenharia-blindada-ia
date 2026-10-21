# 🛡️ Engenharia Blindada para IA & Economia de Tokens

Framework universal de engenharia anti-frágil para desenvolvimento com IA, focado em **economia extrema de tokens na IDE**, **dupla de auditoria independente** e **conexão blindada a gateways de LLM**.

[![Licença MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Produção-success.svg)](#)
[![Arquitetura](https://img.shields.io/badge/Arquitetura-Desacoplada-orange.svg)](#)

---

## ⚡ Por que este Framework Existe?

A maioria dos fluxos com IA (Codex, Cursor, Claude Code, Antigravity) sofre de duas falhas críticas:
1. **Derretimento da Janela de Contexto:** Acoplar múltiplos MCPs no cliente e injetar arquivos inteiros drena a cota semanal em 20 minutos (saltando de 2% para 98% de consumo rapidamente).
2. **Auto-Aprovação e Alucinações Silenciosas:** Confiar em uma única IA para gerar e validar o próprio código resulta em quebras recorrentes em produção, erros de concorrência e quebra de contratos.

Este ecossistema resolve ambos os problemas através do **desacoplamento físico entre Orquestrador e Workers** e da **Dupla de Auditoria Obrigatória**.

---

## 🏛️ Arquitetura de Alto Nível

```
┌────────────────────────────────────────────────────────┐
│      ORQUESTRADOR (Codex / Antigravity / IDE)         │  ──> Contexto Leve (< 2% cota)
│      Apenas planeja, despacha e analisa diffs          │
└───────────────────────────┬────────────────────────────┘
                            │ Briefing isolado via Script Local / CLI
                            ▼
┌────────────────────────────────────────────────────────┐
│     WORKERS EXTERNOS & GATEWAYS DE ALTO VOLUME         │  ──> Roteamento em Franquias
│     (Execução bruta de código e refatoração)           │      de Baixo Custo (15M-20M/dia)
└───────────────────────────┬────────────────────────────┘
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│    AUDITOR 1 (Independente) │ │    AUDITOR 2 (Independente) │
│  Ex: GPT-6 / Reasoning Pro  │ │  Ex: Claude Opus / Gemini   │
└──────────────┬──────────────┘ └──────────────┬──────────────┘
               │                               │
               └────────────┬──────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│      VEREDITO BINÁRIO: [APROVADO] / [REPROVADO]        │  ──> Orquestrador recebe apenas
└────────────────────────────────────────────────────────┘      o Diff final validado!
```

---

## 📂 Estrutura do Repositório

```text
├── skills/
│   ├── 01_engenharia_blindada_qualidade.md         # Skill de governança, Trava Zero e auditoria
│   └── 02_conexao_gateways_maximo_aproveitamento.md # 5 blindagens contra falhas em proxies
├── docs/
│   ├── 01_arquitetura_desacoplada_economia.md      # Como manter o Codex/IDE em 2% de consumo
│   ├── 02_bateria_teste_autenticidade_modelos.md   # 7 testes para detectar modelos falsos/spoofing
│   └── 03_checklist_trava_zero_e_gates.md          # Checklist rápido de pré-voo para PRs
├── scripts/
│   └── conector_api_blindado.py                    # Script Python universal pronto para uso
└── LICENSE                                         # Licença MIT
```

---

## 🚀 Como Utilizar

### 1. Conexão Blindada a Gateways (Python)
Para usar modelos externos sem risco de colisão de cache (CCR) ou timeouts:
```bash
python scripts/conector_api_blindado.py
```

### 2. Importar as Skills na sua IDE
Copie o conteúdo da pasta `skills/` para a pasta de regras ou skills do seu assistente (`.agents/skills`, `.codex/skills` ou `.claude/skills`).

---

## 📜 Licença
Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.
