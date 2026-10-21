---
name: engenharia-blindada-qualidade-ia
description: Protocolo de engenharia anti-frágil, dupla de auditoria independente e concepção segura para desenvolvimento com IA. Elimina auto-aprovação de código, alucinações silenciosas e quebras em produção.
---

# Protocolo Universal de Qualidade e Engenharia Blindada com IA

> **Princípio Central:** Uma IA nunca deve aprovar o próprio código. Toda alteração estrutural deve mapear seu raio de impacto antes de ser executada e passar por validação cruzada entre modelos independentes.

---

## 1. Dupla de Auditoria Independente (Consenso Multi-Modelo)

Para garantir máxima qualidade de código e eliminar o viés de auto-aprovação:

```
                  ┌──────────────────────────────┐
                  │    Demanda / Tarefa Técnica  │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │      IA 1: EXECUTOR          │
                  │   (Gera a Solução/Código)    │
                  └──────────────┬───────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
  ┌─────────────────────────────┐ ┌─────────────────────────────┐
  │      IA 2: AUDITOR A        │ │      IA 3: AUDITOR B        │
  │ (Auditoria Lógica e Casos   │ │ (Auditoria de Concorrência, │
  │        de Borda)            │ │   Topologia e Contratos)    │
  └──────────────┬──────────────┘ └──────────────┬──────────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                  ┌──────────────────────────────┐
                  │   Veredito Binário Final:    │
                  │   [APROVADO] / [REPROVADO]   │
                  └──────────────────────────────┘
```

- **Regra:** O modelo que implementou **NÃO** audita. Dois modelos de famílias diferentes (ex: motor Claude + motor GPT/Gemini) avaliam a proposta de forma cega.
- Se houver divergência entre os auditores, a tarefa volta para correção com os apontamentos objetivos.

---

## 2. Trava Zero: Mapeamento de Raio de Impacto (A-B-C)

Antes de alterar qualquer linha de código, função, endpoint ou banco de dados, o desenvolvedor ou IA deve mapear formalmente a **Tríade A-B-C**:

1. **[A] Jusante Direto (Downstream):**
   - Quem consome a saída deste módulo/função/nó?
   - O diff de retorno adiciona (`+`), remove (`-`) ou altera tipos de campos existentes?
2. **[B] Contratos Inter-Módulos / Inter-Workflows:**
   - Quais serviços externos, webhooks ou chamadores esperam o formato anterior?
   - As configurações de timeout, retries ou headers permanecem compatíveis?
3. **[C] Banco de Dados & Estado Físico:**
   - A alteração dispara triggers, regras de negócio ou mutações em cascata?
   - Há criação de índices, locks concorrentes ou risco de deadlock em alta carga?

> **Regra Anti-Blefe:** É proibido escrever respostas vagas como "sem impactos colaterais". É obrigatório citar os nomes nominais das funções dependentes e tabelas afetadas.

---

## 3. Os Gates Anti-Frágeis de Concepção

Todo código produzido deve ser aprovado nos seguintes gates essenciais:

1. **Gate Anti-Mock:** Proibido homologar código testando apenas com payloads fictícios locais. O teste deve validar a estrutura exata do payload de produção.
2. **Idempotência Real:** Toda operação de escrita em fila, webhook ou banco de dados deve ser segura contra reexecuções acidentais.
3. **Tratamento de Concorrência:** Garantir isolamento transacional seguro contra condições de corrida (*race conditions* e *write skew*).
4. **Anti-Sobrecarga de Assinatura:** Em bancos SQL ou APIs, alterações de parâmetros devem ser retrocompatíveis para evitar erros de resolução de rotas (como `Multiple Choices 300`).
5. **Observabilidade e Dead Letter:** Falhas devem ser capturadas com logs estruturados e alertas, sem silenciamento passivo de exceções.
