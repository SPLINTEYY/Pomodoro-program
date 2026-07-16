#Python

from logging import root
import tkinter as tk

#--- CONFIGURACOES DE TEMPO E CORES ----

WORK_MIN = 25
SHORT_BREAK_MIN = 5
BG_COLOR = "#2c3e50"     # cor de fundo escura
WORK_COLOR = "#e74c3c"   #vermelho para o foco
BREAK_COLOR = "#2ecc71"  #verde para o foco
TEXT_COLOR = "#ecf0f1"   # Texto claro

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("350x250")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False) # Obs.: Impede o redimensionamento da janela

        #Variaveis de Estado

        self.timer_running = False
        self.timer_id = None
        self.is_work_time = True
        self.time_left = WORK_MIN * 60 # Converte minutos para segundos

        # ----- Constução do Front-end -----

        self.title_label = tk.Label(
            text="Foco Total",
            fg=WORK_COLOR,
            bg=BG_COLOR,
            font=("Helvetica", 28, "bold")
        )
        self.title_label.pack(pady=(20, 10))

        # 2. Display do Timer
        self.timer_label = tk.Label(
            text=f"{WORK_MIN:02d}:00",
            fg=TEXT_COLOR,
            bg=BG_COLOR,
            font=("Helvetica", 45, "bold")
        )
        self.timer_label.pack(pady=10)

        # 3. Frame para alinhar os botões lado a lado
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=15)

        # 4. Botões
        self.start_button = tk.Button(
            button_frame,
            text="Iniciar",
            command=self.start_timer,
            font=("Helvetica", 12, "bold"),
            width=8,
            cursor="hand2",

        )
        self.start_button.grid(row=0, column=0, padx=15)

        self.reset_button = tk.Button(
            button_frame,
            text="Reiniciar",
            command=self.reset_timer,
            font=("Helvetica", 12, "bold"),
            width=8,
            cursor="hand2",
        )
        self.reset_button.grid(row=0, column=1, padx=15)

        # ----- logica do programa ------

    def start_timer(self):
        # ---- inicia o cronometro apenas se ele ja não estiver rodando ----
        if not self.timer_running:
            self.timer_running = True
            self.count_down()

    def reset_timer(self):
        # ---- para o cronometro e reseta as variaveis de estado ----
        self.timer_running = False

        #--- cancela o evento agendado do count_down, se existir ---
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.is_work_time = True
        self.time_left = WORK_MIN * 60
        self.title_label.config(text="Foco Total", fg=WORK_COLOR)
        self.timer_label.config(text=f"{WORK_MIN:02d}:00")

    def count_down(self):
        # ---- gerencia a contagem regressiva e alterna entre foco e descanso ----
        if self.timer_running and self.time_left > 0:
            minutos = self.time_left // 60
            segundos = self.time_left % 60

            #formata o tempo para exibir no formato MM:SS
            time_string = f"{minutos:02d}:{segundos:02d}"
            self.timer_label.config(text=time_string)

            self.time_left -= 1
            # o tkinter agenda a execução da função count_down após 1000ms (1 segundo)
            self.timer_id = self.root.after(1000, self.count_down)

        elif self.timer_left == 0:
            #----- quando o tempo acaba, alterna entre foco e descanso ----
            self.timer_running = False
            self.switch_mode()

    def switch_mode(self):
        # ---- alterna as fases entre trabalho e pausa ----
        if self.is_work_time:
            self.is_work_time = False
            self.time_left = SHORT_BREAK_MIN * 60
            self.title_label.config(text="Pausa", fg=BREAK_COLOR)
        else:
            self.is_work_time = True
            self.time_left = WORK_MIN * 60
            self.title_label.config(text="Foco Total", fg=WORK_COLOR)

        #reinicia a contagem para a nova fase
        self.start_timer()

# ---- inicialização do aplicativo ----
if __name__ == "__main__":
    janela_princiapl = tk.Tk()
    app = PomodoroApp(janela_princiapl)
    janela_princiapl.mainloop()
