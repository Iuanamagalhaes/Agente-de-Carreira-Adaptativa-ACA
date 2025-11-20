# Agente de Carreira Adaptativa (ACA)

> Projeto: Agente-de-Carreira-Adaptativa-ACA

## Visão Geral

O **Agente de Carreira Adaptativa (ACA)** é uma aplicação em Python que atua como um assistente inteligente para apoio de carreira. Ele pode receber informações do usuário, processar via prompts e gerar recomendações adaptativas de trajetória, sugestões de cursos, planos de ação e outros insights para desenvolvimento profissional.

Este repositório contém o backend da solução, com endpoints de API, lógica de agente inteligente, prompts configuráveis e utilitários de apoio.

---

## Funcionalidades Principais

* Interface de API para interação com o agente (arquivo `api.py`).
* Lógica principal de execução do agente no módulo `main.py`.
* Arquivo `prompts.py` onde estão definidos os prompts e templates de interação.
* Utilitários auxiliares em `utils.py` para tratamento de dados, formatação de respostas, etc.
* Arquivo `.env` para configuração de variáveis de ambiente.
* Dependências listadas em `requirements.txt`.

---

## Pré-requisitos

Antes de rodar o projeto localmente, certifique-se de ter:

* Python 3.8 ou superior.
* Uma chave de API válida para o modelo de linguagem (Google Gemini).
* Um ambiente virtual (recomendado) para isolar as dependências.
* Git (caso queira clonar o repositório).

---

## Instalação e Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/Iuanamagalhaes/Agente-de-Carreira-Adaptativa-ACA.git
   cd Agente-de-Carreira-Adaptativa-ACA
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente:

   * No arquivo `.env`, defina a chave do modelo, por exemplo:

     ```env
     OPENAI_API_KEY="sua_chave_aqui"
     ```

---

## Execução

Para executar diretamente o módulo principal (modo console):

```bash
python main.py
```
