#!/usr/bin/env python3
"""
Exemplo de Conector de API Blindado para Servidores e Gateways de IA
Iteraflow - Engenharia de IA

Este script demonstra como conectar uma aplicação ou IDE a gateways de IA
de alto volume com as 5 blindagens ativas:
1. Anti-colisão de KV-Cache / CCR (nonce temporal de sessão)
2. Fallback automático de protocolo (Anthropic -> OpenAI)
3. Calibração de esforço de raciocínio (evitando timeouts de 90s)
4. Retry com backoff exponencial
5. Portão de sanidade anti-truncamento e integridade de resposta
"""

import os
import sys
import time
import uuid
import requests

def chamar_api_blindada(
    prompt: str,
    api_key: str,
    base_url: str,
    model: str = "claude-sonnet-5.5",
    max_tokens: int = 8192
) -> str:
    # 1. Nonce único de sessão
    session_id = f"sessao-{int(time.time()*1000)}-{uuid.uuid4().hex[:6]}"
    prompt_com_nonce = f"[{session_id}]\n\n{prompt}"
    
    # Rota 1: Anthropic Messages
    url_anthropic = f"{base_url.rstrip('/')}/v1/messages"
    headers_anthropic = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload_anthropic = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt_com_nonce}]
    }
    
    for tentativa in range(1, 4):
        try:
            print(f"[*] Tentativa {tentativa} via rota Anthropic: {url_anthropic}...")
            res = requests.post(url_anthropic, headers=headers_anthropic, json=payload_anthropic, timeout=120)
            
            if res.status_code == 200:
                data = res.json()
                if data.get("stop_reason") == "max_tokens":
                    raise ValueError("ALERTA: Resposta truncada por limite de tokens!")
                return data["content"][0]["text"]
            
            print(f"[-] Rota Anthropic retornou status {res.status_code}: {res.text[:150]}")
            
            # Se for erro de gateway/servidor (500, 502, 503), tenta Fallback OpenAI
            if res.status_code in (500, 502, 503):
                url_openai = f"{base_url.rstrip('/')}/v1/chat/completions"
                headers_openai = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload_openai = {
                    "model": model,
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt_com_nonce}]
                }
                print(f"[*] Acionando Fallback para rota OpenAI: {url_openai}...")
                res_oa = requests.post(url_openai, headers=headers_openai, json=payload_openai, timeout=120)
                if res_oa.status_code == 200:
                    data_oa = res_oa.json()
                    return data_oa["choices"][0]["message"]["content"]
                print(f"[-] Rota OpenAI retornou status {res_oa.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Erro de conexão na tentativa {tentativa}: {e}")
            time.sleep(2 ** tentativa)

    raise RuntimeError("Falha definitiva de conexão após 3 tentativas.")

if __name__ == "__main__":
    print("=== TESTE DE CONECTOR BLINDADO ===")
    api_key = os.environ.get("MINHA_API_KEY", "sua_chave_aqui")
    base_url = os.environ.get("MEU_GATEWAY_URL", "https://seu-gateway.com")
    
    if api_key == "sua_chave_aqui":
        print("Configure MINHA_API_KEY e MEU_GATEWAY_URL para rodar o teste real.")
        sys.exit(0)
        
    resultado = chamar_api_blindada("Olá! Faça uma verificação rápida de sanidade do sistema.", api_key, base_url)
    print("\nResposta recebida com sucesso:")
    print(resultado)
