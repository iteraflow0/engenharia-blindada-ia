# Checklist Rápido de Pré-Voo: Trava Zero & Gates de Concepção

Copie este checklist no início de qualquer plano de implementação ou Pull Request (PR) para garantir blindagem operacional antes de tocar no código:

---

### 1. Trava Zero: Raio de Impacto (Tríade A-B-C)

- [ ] **[A] Jusante Direto (Downstream):** Mapeado quem consome o retorno deste nó ou função. Campos adicionados/removidos explicitados nominalmente.
- [ ] **[B] Contratos Inter-Módulos:** Verificado se afeta chamadores externos, webhooks, subworkflows ou integrações parceiras.
- [ ] **[C] Banco de Dados & Estado Físico:** Verificado se altera tabelas com triggers, índices pesados, regras de segurança ou filas assíncronas.

---

### 2. Checklist dos Gates Anti-Frágeis

| Gate | Requisito Obrigatório | Status |
| :--- | :--- | :---: |
| **G1 - Anti-Mock** | Testado com payload estrutural idêntico ao de produção (sem dados inventados) | [ ] PASS |
| **G2 - Idempotência** | Operações de escrita protegidas contra duplicidade em reexecuções | [ ] PASS |
| **G3 - Anti-Overload SQL** | Assinaturas de funções/rotas verificadas para evitar ambiguidade (HTTP 300) | [ ] PASS |
| **G4 - Concorrência** | Transações protegidas contra condições de corrida (*race conditions*) | [ ] PASS |
| **G5 - Observabilidade** | Logs estruturados implementados para diagnósticos de falha | [ ] PASS |
| **G6 - Secrets Isolados** | Zero chaves de API, tokens ou credenciais expostas no código | [ ] PASS |
| **G7 - Dupla de Auditoria** | Solução revisada de forma cega por pelo menos 2 modelos independentes | [ ] PASS |
