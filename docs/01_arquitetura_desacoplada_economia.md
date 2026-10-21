# Guia de Arquitetura: Desacoplamento, Alta Performance e Economia de Tokens

Este documento explica como estruturar um ecossistema com múltiplos modelos de IA e ferramentas (MCPs) sem esgotar as cotas da janela de contexto do orquestrador.

---

## 1. O Problema Comum: Acoplamento Monolítico no Client

Quando você conecta múltiplos servidores MCP diretamente na interface do assistente (Codex, Antigravity, Cursor, etc.):
- O schema JSON de **todas as ferramentas** de cada MCP é enviado a **cada turno** de conversa.
- O histórico de mensagens armazena saídas brutas de arquivos e payloads JSON gigantes.
- **Resultado:** A janela de contexto atinge 80k-120k tokens em poucos minutos, esgotando cotas de planos de desenvolvedor em 20 minutos.

```
[❌ ARQUITETURA ACOPLADA - VAZAMENTO DE TOKENS]
Chat/IDE ────> Envia System Prompt + 30 Schemas de MCPs (30k tokens)
            └─> Executa ferramenta e recebe 50k tokens de JSON no histórico
            └─> Próximo turno: envia 80k tokens ➔ COTA ZERADA RAPIDAMENTE!
```

---

## 2. A Solução: Arquitetura Desacoplada com Workers Externos

```
[✅ ARQUITETURA DESACOPLADA - CONSUMO < 3% NA JANELA PRINCIPAL]

┌──────────────────────────────────────────────┐
│  ORQUESTRADOR (Codex / IDE / Antigravity)   │  ──> Contexto Leve (< 2.000 tokens)
│  Apenas planeja, despacha e analisa diffs    │
└──────────────────────┬───────────────────────┘
                       │ Briefing isolado via Script Local / CLI
                       ▼
┌──────────────────────────────────────────────┐
│    WORKERS EXTERNOS & GATEWAYS DE VOLUME     │  ──> APIs de Alto Volume / Baixo Custo
│    (Execução bruta de código e refatoração)  │
└──────────────────────┬───────────────────────┘
                       │ Retorno estrito (Diff ou Resumo Sintético)
                       ▼
┌──────────────────────────────────────────────┐
│  ORQUESTRADOR RECEBE O RESULTADO LIMPO       │  ──> Histórico limpo, zero inchaço.
└──────────────────────────────────────────────┘
```

### Princípios Técnicos:

1. **Orquestrador Cego para Schemas Desnecessários:**
   - O orquestrador não precisa conhecer dezenas de ferramentas ao mesmo tempo. Use MCPs sob demanda (*lazy-loading*) ou despache comandos via scripts CLI locais.
2. **Workers em APIs de Custo Irrisório:**
   - O processamento massivo de arquivos, análises estáticas e geração de código pesado rodam em provedores de alto volume (ex: franquias de 15M a 20M tokens dedicadas).
3. **Graphify (Grafo de Conhecimento AST):**
   - Em vez de forçar o assistente a ler arquivos inteiros do repositório para achar uma função, mantenha um grafo de AST local. O assistente consulta apenas as linhas e nós necessários.
4. **Modo Caveman (Compressão de Resposta):**
   - Elimina o excesso de formalidades e prolixidade corporativa nas respostas dos modelos. Uma comunicação técnica e direta reduz em média **65% dos tokens gerados de saída**.
