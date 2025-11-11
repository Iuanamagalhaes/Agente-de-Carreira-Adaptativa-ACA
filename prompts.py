# definindo o comportamento do modelo
SYSTEM_PROMPT = """
Você é o "ACA — Agente de Carreira Adaptativa", um assistente profissional especializado em avaliar risco de automação,
sugerir planos de upskilling e reskilling, e realizar simulações de entrevistas. Sempre responda em JSON quando explicitado,
com campos claros, concisos e no máximo 300-500 palavras totais. Use linguagem profissional, amigável e focada em ação.
"""

# F1
PROMPT_F1 = """
F1 - Análise de Perfil e Risco de Automação.

Entrada:
- profissao: "{profissao}"
- tarefas: "{tarefas}"

Tarefa:
1) Avalie o risco de automação da profissão em 3 níveis: "Baixo", "Médio", "Alto".
2) Liste de 4 a 6 habilidades críticas (separar entre soft e hard), indicando por cada uma: nome e por que é importante.
3) Sugira 2 quick wins (ações rápidas) para reduzir risco de automação.

Saída esperada (JSON):
{{
  "profissao": "...",
  "risco_automacao": "Baixo|Médio|Alto",
  "habilidades": [
     {{ "tipo": "Hard|Soft", "nome": "...", "justificativa": "..." }},
     ...
  ],
  "quick_wins": ["...", "..."]
}}
"""

# F2
PROMPT_F2 = """
F2 - Plano de Upskilling.

Entrada:
- profissao: "{profissao}"
- habilidades_atuais: "{habilidades_atuais}"

Tarefa:
1) Sugira 3 a 5 áreas de aprimoramento (nome da área).
2) Para cada área, sugira 1 recurso de aprendizado prático (curso / certificação / tutorial) com uma breve justificativa e estimativa de tempo (em semanas).

Saída (JSON):
{{
 "profissao": "...",
 "plano_upskilling": [
   {{ "area": "...", "recurso": "...", "justificativa": "...", "tempo_semanas": 4 }},
   ...
 ]
}}
"""

# F3
PROMPT_F3 = """
F3 - Caminho de Reskilling.

Entrada:
- profissao_origem: "{origem}"
- profissao_destino: "{destino}"
- habilidades_atuais: "{habilidades_atuais}"

Tarefa:
1) Liste até 5 habilidades transferíveis (com explicação).
2) Liste 3 a 5 habilidades novas a serem aprendidas (com recursos sugeridos).
3) Sugira uma ordem de aprendizagem (passo-a-passo em 3 a 6 passos).

Saída (JSON):
{{
 "origem": "...",
 "destino": "...",
 "transferiveis": [ {{ "nome":"...", "por_que":"..." }}, ... ],
 "novas_habilidades":[ {{ "nome":"...", "recurso":"...", "tempo_semanas":... }}, ... ],
 "plano_passos":[ "...", "..." ]
}}
"""

# F4
PROMPT_F4 = """
F4 - Simulação de Entrevista.

Entrada:
- vaga_alvo: "{vaga}"
- niveis_competencia_esperado: "{nivel}"  # e.g., Junior, Pleno, Senior

Tarefa:
1) Gere 3 perguntas de entrevista específicas para a vaga_alvo e nivel.
2) Para cada pergunta, forneça critérios de avaliação (clareza, relevância, profundidade) e uma resposta exemplo bem elaborada.
3) Quando o usuário submeter sua resposta, o agente deve comparar com os critérios e dar uma nota de 0-10 e feedback conciso.

Saída (fase 1 - geracao perguntas) (JSON):
{{
 "vaga": "...",
 "nivel": "...",
 "perguntas": [
   {{ "pergunta":"...", "criterios":["clareza","relevancia","profundidade"], "exemplo_resposta":"..." }},
   ...
 ]
}}

-- Quando for avaliar a resposta do usuário, envie um prompt de avaliação que inclua a pergunta e a resposta do usuário. O LLM deve retornar:
{{ "nota": number, "feedback":"..." }}
"""