import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkinter.font import Font
from prompts import SYSTEM_PROMPT, PROMPT_F1, PROMPT_F2, PROMPT_F3, PROMPT_F4
from api import call_llm
from utils import try_parse_json
import threading
import re

PRIMARY = "#004C99"
SECONDARY = "#E9F0FA"
BG = "#F5F7FB"
BOT_BG = "#FFFFFF"
TEXT_COLOR = "#1C1C1C"
FONT_NAME = "Montserrant"

class ACAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ACA — Agente de Carreira Adaptativa")
        self.geometry("980x640")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.current_mode = None
        self.interview_questions = []
        self.last_question_index = 0
        self._build_ui()

    def _build_ui(self):
        self.sidebar = tk.Frame(self, width=230, bg=PRIMARY)
        self.sidebar.pack(side="left", fill="y")
        title = tk.Label(self.sidebar, text="ACA Assistant", bg=PRIMARY, fg="white", font=(FONT_NAME, 14, "bold"))
        title.pack(pady=20)
        style = ttk.Style()
        style.configure("TButton", font=(FONT_NAME, 10), padding=6)
        style.map("TButton", background=[("active", "#005FCC")])
        self.add_button("Análise de Perfil (F1)", "F1")
        self.add_button("Plano de Upskilling (F2)", "F2")
        self.add_button("Caminho de Reskilling (F3)", "F3")
        self.add_button("Simulação Entrevista (F4)", "F4")
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.mode_label = tk.Label(self.main, text="Escolha uma funcionalidade no menu à esquerda", bg=BG, font=(FONT_NAME, 12, "bold"))
        self.mode_label.pack(anchor="w", pady=(5, 5))
        self.chat_display = scrolledtext.ScrolledText(self.main, wrap=tk.WORD, state="disabled", bg=BOT_BG, fg=TEXT_COLOR, font=(FONT_NAME, 10), padx=10, pady=10)
        self.chat_display.pack(fill="both", expand=True, pady=5)
        self.chat_display.tag_configure("bold", font=(FONT_NAME, 10, "bold"))
        self.chat_display.tag_configure("title", font=(FONT_NAME, 11, "bold"))
        self.chat_display.tag_configure("list", lmargin1=25, lmargin2=45)
        self.input_frame = tk.Frame(self.main, bg=BG)
        self.input_frame.pack(fill="x", pady=(5, 5))
        self.input_text = tk.Text(self.input_frame, height=3, width=70, font=(FONT_NAME, 10))
        self.input_text.grid(row=0, column=0, padx=(0, 5), pady=5)
        send_btn = tk.Button(self.input_frame, text="Enviar", bg=PRIMARY, fg="white", font=(FONT_NAME, 10, "bold"), command=self.on_send)
        send_btn.grid(row=0, column=1, padx=(0, 5))
        clear_btn = tk.Button(self.input_frame, text="Limpar", bg="#CCCCCC", font=(FONT_NAME, 10), command=self.clear_chat)
        clear_btn.grid(row=0, column=2)

    def add_button(self, text, mode):
        btn = tk.Button(self.sidebar, text=text, bg="white", fg=PRIMARY, font=(FONT_NAME, 10, "bold"), relief="flat", width=25, command=lambda: self.set_mode(mode))
        btn.pack(pady=8, padx=10)

    def render_markdown(self, text):
        self.chat_display.configure(state="normal")
        lines = text.split("\n")
        for line in lines:
            if re.match(r"^#{1,3} ", line):
                resto = re.sub(r"^#{1,3} ", "", line)
                parts = re.split(r"(\*\*.*?\*\*)", resto)
                for p in parts:
                    if p.startswith("**") and p.endswith("**"):
                        self.chat_display.insert(tk.END, p[2:-2], ("title", "bold"))
                    else:
                        self.chat_display.insert(tk.END, p, "title")
                self.chat_display.insert(tk.END, "\n")
            elif re.match(r"^- ", line.strip()):
                resto = line.strip()[2:]
                self.chat_display.insert(tk.END, "• ", "list")
                parts = re.split(r"(\*\*.*?\*\*)", resto)
                for p in parts:
                    if p.startswith("**") and p.endswith("**"):
                        self.chat_display.insert(tk.END, p[2:-2], ("list", "bold"))
                    else:
                        self.chat_display.insert(tk.END, p, "list")
                self.chat_display.insert(tk.END, "\n")
            elif "**" in line:
                parts = re.split(r"(\*\*.*?\*\*)", line)
                for p in parts:
                    if p.startswith("**") and p.endswith("**"):
                        self.chat_display.insert(tk.END, p[2:-2], "bold")
                    else:
                        self.chat_display.insert(tk.END, p)
                self.chat_display.insert(tk.END, "\n")
            else:
                self.chat_display.insert(tk.END, line + "\n")
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)

    def append_user_message(self, text):
        self.render_markdown(f"**Você:** {text}")

    def append_bot_message(self, text):
        self.render_markdown(f"**ACA:** {text}")

    def set_mode(self, mode):
        self.current_mode = mode
        modes = {
            "F1": ("F1 — Análise de Perfil e Risco de Automação", "Exemplo:\nDesenvolvedor Full Stack\nTarefas: programar, testar, manter sistemas web."),
            "F2": ("F2 — Plano de Upskilling Personalizado", "Exemplo:\nEngenheiro de Produção\nHabilidades: Excel, Lean Manufacturing, Power BI."),
            "F3": ("F3 — Caminho de Reskilling", "Exemplo:\nProfissão atual: Professor de Matemática\nProfissão desejada: Cientista de Dados\nHabilidades: comunicação, análise lógica."),
            "F4": ("F4 — Simulação de Entrevista", "Exemplo:\nVaga: Analista de Dados\nNível: Júnior.")
        }
        title, example = modes[mode]
        self.mode_label.config(text=title)
        self.append_bot_message(f"{title}\nDigite as informações conforme o exemplo abaixo:\n\n{example}")

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.configure(state="disabled")
        self.append_bot_message("Chat limpo. Escolha uma nova funcionalidade à esquerda.")

    def on_send(self):
        content = self.input_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Aviso", "Digite algo antes de enviar.")
            return
        if not self.current_mode:
            messagebox.showwarning("Aviso", "Escolha uma funcionalidade primeiro.")
            return
        self.append_user_message(content)
        self.input_text.delete("1.0", tk.END)
        threading.Thread(target=self.process_input, args=(self.current_mode, content)).start()

    def process_input(self, mode, content):
        self.append_bot_message("Processando...")
        try:
            if mode == "F1":
                self.handle_f1(content)
            elif mode == "F2":
                self.handle_f2(content)
            elif mode == "F3":
                self.handle_f3(content)
            elif mode == "F4":
                if not self.interview_questions:
                    self.handle_f4_generate(content)
                else:
                    self.handle_f4_evaluate(content)
        except Exception as e:
            self.append_bot_message(f"Ocorreu um erro interno: {str(e)}")

    def handle_f1(self, content):
        parts = content.split("\n")
        profissao = parts[0]
        tarefas = " ".join(parts[1:]) if len(parts) > 1 else ""
        resp = call_llm(PROMPT_F1.format(profissao=profissao, tarefas=tarefas), system=SYSTEM_PROMPT)
        parsed, _ = try_parse_json(resp["text"])
        if parsed:
            out = f"**Profissão:** {parsed.get('profissao')}\n\n**Risco:** {parsed.get('risco_automacao')}\n\n### Habilidades"
            for h in parsed.get("habilidades", []):
                out += f"\n- [{h['tipo']}] **{h['nome']}**: {h['justificativa']}"
            out += "\n\n### Quick Wins\n" + "\n".join(f"- {q}" for q in parsed.get("quick_wins", []))
            self.append_bot_message(out)
        else:
            self.append_bot_message(resp["text"])

    def handle_f2(self, content):
        parts = content.split("\n")
        profissao = parts[0]
        habilidades = " ".join(parts[1:]) if len(parts) > 1 else ""
        resp = call_llm(PROMPT_F2.format(profissao=profissao, habilidades_atuais=habilidades), system=SYSTEM_PROMPT)
        parsed, _ = try_parse_json(resp["text"])
        if parsed:
            out = f"### Plano de Upskilling para {parsed.get('profissao')}"
            for p in parsed.get("plano_upskilling", []):
                out += f"\n\n### Área: {p['area']} ({p['tempo_semanas']} semanas)\n- **Recurso:** {p['recurso']}\n- **Justificativa:** {p['justificativa']}"
            self.append_bot_message(out)
        else:
            self.append_bot_message(resp["text"])

    def handle_f3(self, content):
        parts = content.split("\n")
        if len(parts) < 2:
            self.append_bot_message("Informe profissão atual e destino em linhas separadas.")
            return
        origem, destino = parts[0], parts[1]
        habilidades = " ".join(parts[2:]) if len(parts) > 2 else ""
        resp = call_llm(PROMPT_F3.format(origem=origem, destino=destino, habilidades_atuais=habilidades), system=SYSTEM_PROMPT)
        parsed, _ = try_parse_json(resp["text"])
        if parsed:
            out = f"### Transição {parsed['origem']} → {parsed['destino']}\n\n### Habilidades Transferíveis"
            for t in parsed.get("transferiveis", []):
                out += f"\n- **{t['nome']}**: {t['por_que']}"
            out += "\n\n### Novas Habilidades"
            for n in parsed.get("novas_habilidades", []):
                out += f"\n- **{n['nome']}** ({n['tempo_semanas']} semanas)\n  - Recurso: {n['recurso']}"
            out += "\n\n### Plano de Estudo\n" + "\n".join(f"- {p}" for p in parsed.get("plano_passos", []))
            self.append_bot_message(out)
        else:
            self.append_bot_message(resp["text"])

    def handle_f4_generate(self, content):
        parts = content.split("\n")
        vaga = parts[0]
        nivel = parts[1] if len(parts) > 1 else "Pleno"
        resp = call_llm(PROMPT_F4.format(vaga=vaga, nivel=nivel), system=SYSTEM_PROMPT)
        parsed, _ = try_parse_json(resp["text"])
        if parsed and "perguntas" in parsed:
            self.interview_questions = parsed["perguntas"]
            self.last_question_index = 0
            self.append_bot_message(f"Foram geradas **{len(self.interview_questions)} perguntas.**\nResponda à primeira para começar!\n\n### Pergunta 1:\n{self.interview_questions[0]['pergunta']}")
        else:
            self.append_bot_message(resp["text"])

    def handle_f4_evaluate(self, content):
        if not self.interview_questions:
            self.append_bot_message("Nenhuma pergunta gerada. Gere uma nova entrevista primeiro.")
            return
        if self.last_question_index >= len(self.interview_questions):
            self.append_bot_message("Entrevista finalizada! Gere uma nova vaga para começar outra simulação.")
            return
        pergunta = self.interview_questions[self.last_question_index]["pergunta"]
        avaliacao_prompt = f"""
Você é um recrutador experiente. Avalie a resposta de um candidato a uma pergunta de entrevista.

Pergunta: {pergunta}
Resposta do candidato: {content}

Dê uma nota entre 0 e 10.
Forneça um feedback de até 3 frases.

Formato JSON:
{{ "nota": number, "feedback": "texto" }}
"""
        resp = call_llm(avaliacao_prompt, system=SYSTEM_PROMPT)
        parsed, _ = try_parse_json(resp["text"])
        if not parsed:
            self.append_bot_message("Não consegui interpretar a resposta do avaliador.\n\n" + resp["text"])
        else:
            nota = parsed.get("nota")
            feedback = parsed.get("feedback") or "Sem feedback fornecido."
            if nota is None:
                self.append_bot_message(f"Feedback: {feedback}")
            else:
                self.append_bot_message(f"Avaliação da pergunta {self.last_question_index + 1}\n**Nota:** {nota}/10\n**Feedback:** {feedback}")
        self.last_question_index += 1
        if self.last_question_index < len(self.interview_questions):
            proxima = self.interview_questions[self.last_question_index]["pergunta"]
            self.append_bot_message(f"**Próxima pergunta ({self.last_question_index + 1}/{len(self.interview_questions)}):**\n{proxima}")
        else:
            self.append_bot_message("Entrevista concluída! Gere uma nova vaga para praticar novamente.")

if __name__ == "__main__":
    app = ACAApp()
    app.append_bot_message("**Bem-vinda ao ACA — Agente de Carreira Adaptativa**\n\nEscolha uma funcionalidade no menu à esquerda para começar.")
    app.mainloop()
