import customtkinter as ctk
from calendario_usuario import CalendarioUsuario

class TelaLogada:
    def __init__(self, janela, width, height, button_width, usuario_id, nome_usuario):
        self.janela = janela
        self.width = width
        self.height = height
        self.button_width = button_width
        self.usuario_id = usuario_id
        self.nome_usuario = nome_usuario
        

    def exibir_tela_logada(self):
        # Oculta a Tela Inicial
        self.janela.withdraw()
        # Exibe a Tela Logada
        self.janela_logada = ctk.CTk()
        self.janela_logada._set_appearance_mode("dark")
        self.janela_logada.geometry(f"{self.width}x{self.height}")
        self.janela_logada.minsize(height=self.height, width=self.width)
        
        # Adiciona o frame_titulo à Tela Logada
        self.frame_titulo()

        self.botao_confirmar_login = ctk.CTkButton(self.janela_logada, text="Agendar/Consultar horários", command=self.exibir_calendario).pack(pady=10)

        # Inicia o loop principal da janela logada
        self.janela_logada.mainloop()

    def exibir_calendario(self):
        with CalendarioUsuario(self.janela, self.usuario_id, database_name="dbbarbearia.db") as calendario:
            # Use métodos e atributos de 'calendario' conforme necessário
            calendario.adicionar_horario()
            calendario.exibir_horarios()

    def frame_titulo(self):
        # Frame acima da Tabview
        frame_superior = ctk.CTkFrame(self.janela_logada, corner_radius=20)
        frame_superior.pack(side="top", expand=False, fill="none")

        # Texto (título) e Subtitulo no Frame Superior
        texto_titulo = ctk.CTkLabel(frame_superior, text=f"Olá, {self.nome_usuario}", font=("Helvetica", 26, "bold"))
        texto_titulo.pack(pady=20, padx=100)