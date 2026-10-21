# Bateria Forense de Autenticidade de Modelos de IA (Anti-Spoofing)

Muitos revendedores terceiros e gateways de baixo custo utilizam práticas desonestas como:
- **Model Spoofing:** Vender modelos menores (ex: Haiku ou modelos mini) rotulados como modelos de ponta (Opus, Sonnet ou GPT-6).
- **Quantização Agressiva:** Reduzir modelos para formatos comprimidos (INT4) que perdem capacidade de raciocínio lógico e quebram em código complexo.

Para garantir que uma API externa está realmente entregando um modelo de fronteira autêntico, aplicamos esta bateria de testes de validação:

---

## 1. Sonda Térmica & Determinismo de Raciocínio
- **Objetivo:** Avaliar se o modelo possui raciocínio estendido (*thinking/reasoning tokens*) real ou se é uma resposta rasa com delay artificial.
- **Teste:** Submeter um problema combinatório complexo exigindo árvore de decisão explícita.
- **Detecção:** Modelos falsificados tentam responder em poucos segundos ou geram texto superficial sem expor etapas dedutivas sólidas.

---

## 2. Rastreamento Algorítmico Bitwise (Ground Truth)
- **Objetivo:** Medir a precisão estrita do interpretador interno do modelo sem capacidade de "adivinhação".
- **Prompt:** Executar operações de manipulação de bits (`XOR`, `AND`, rotação de bits) em cadeias numéricas e pedir o valor exato no final.
- **Detecção:** Modelos capados/pequenos erram operações bitwise acumuladas; modelos de raciocínio profundo de fronteira acertam 100%.

---

## 3. Anomalia de Concorrência & MVCC em Banco de Dados
- **Objetivo:** Avaliar conhecimento profundo de sistemas transacionais.
- **Cenário:** Simulação de duas transações concorrentes sob nível de isolamento `REPEATABLE READ` no PostgreSQL executando updates cruzados (*Write Skew*).
- **Pergunta:** Exigir o diagnóstico exato se o Postgres levantará erro de serialização (`40001`) ou se permitirá a anomalia.
- **Detecção:** Modelos inferiores confundem o comportamento de locks com o isolamento de snapshots.

---

## 4. Estresse de Restrições Negativas Combinadas
- **Objetivo:** Testar se o modelo segue 5 ou mais regras negativas simultâneas (ex: "Não use a letra E", "Não use condicionais IF", "Não utilize loops FOR/WHILE").
- **Detecção:** Modelos falsificados ou pequenos quebram pelo menos uma restrição negativa ao longo da resposta.

---

## 5. Estresse Extremo de Codificação de Sistemas (LSM-Tree)
- **Objetivo:** Solicitar a implementação completa de uma estrutura de dados de banco de alta performance (ex: MemTable + WAL + SSTable com bloom filter em memória).
- **Detecção:** Modelos pequenos alucinam métodos inexistentes ou entregam código incompleto e quebrado. Modelos de ponta entregam a estrutura perfeitamente tipada e funcional.
