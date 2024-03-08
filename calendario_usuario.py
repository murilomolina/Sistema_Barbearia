import customtkinter as ctk
from tkcalendar import Calendar
import sqlite3
from datetime import datetime


class CalendarioUsuario:
    def __init__(self, parent, usuario_id, database_name="dbbarbearia.db"):
        self.parent = parent
        self.database_name = database_name
        self.usuario_id = usuario_id
        self.conn = sqlite3.connect(self.database_name)
        self.create_table_if_not_exists()

        self.conn = sqlite3.connect(self.database_name)
        self.create_table_if_not_exists()

        janela_principal_width = 800
        janela_principal_heigth = 800
        # botao_width = 100

        # Criação da janela principal
        self.root = ctk.CTk()
        self.root.title("Agenda de Horários")
        self.root._set_appearance_mode("dark")
        self.root.geometry(f"{janela_principal_width}x{janela_principal_heigth}")
        self.root.minsize(height=janela_principal_heigth, width=janela_principal_width) 

        # Dicionário para armazenar horários associados a cada data
        self.horarios = {}

        # Widget de calendário
        ano, mes, dia = self.obter_ano_mes_dia()
        self.cal = Calendar(self.root, selectmode='day', year=ano, month=mes, day=dia, background = 'black')
        self.cal.pack(pady=20)

        # Entrada para horário
        self.label_horario = ctk.CTkLabel(self.root, text="Horário:")
        self.label_horario.pack()
        self.entry_horario = ctk.CTkEntry(self.root)
        self.entry_horario.pack(pady=10)

        # Entrada para texto
        self.label_texto = ctk.CTkLabel(self.root, text="Texto:")
        self.label_texto.pack()
        self.entry_texto = ctk.CTkEntry(self.root)
        self.entry_texto.pack(pady=10)

        # Botão para adicionar horário
        self.btn_adicionar = ctk.CTkButton(self.root, text="Adicionar Horário", command=self.adicionar_horario)
        self.btn_adicionar.pack(pady=10)

        # Widget de texto para exibir horários
        self.txt_horarios = ctk.CTkTextbox(self.root, height=40, width=200)
        self.txt_horarios.pack(pady=20)
        self.txt_horarios.configure(state=ctk.DISABLED)  # Inicialmente, desabilitar edição

        # Configurar um evento para atualizar os horários quando uma data for clicada
        self.cal.bind("<<CalendarSelected>>", lambda e: self.exibir_horarios())

        # Iniciar o loop principal do Tkinter
        self.root.mainloop()

    def create_table_if_not_exists(self):
        query = """
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY,
            data TEXT,
            horario TEXT,
            texto TEXT,
            FOREIGN KEY (id) REFERENCES usuarios(id)
        );
        """
        self.conn.execute(query)
        self.conn.commit()
 

    def adicionar_horario(self):
        data_selecionada = self.cal.get_date()
        horario = self.entry_horario.get()
        texto = self.entry_texto.get()

        # Adicionar o horário ao banco de dados
        self.adicionar_horario_no_bd(data_selecionada, horario, texto, self.usuario_id)

        # Atualizar a exibição dos horários
        self.exibir_horarios()

        # Limpar campos após adicionar
        self.entry_horario.delete(0, 'end')
        self.entry_texto.delete(0, 'end')

    def adicionar_horario_no_bd(self, data, horario, texto, usuario_id):
        try:
            # Inserir o horário no banco de dados
            query = "INSERT INTO horarios (data, horario, texto, id) VALUES (?, ?, ?, ?);"
            self.conn.execute(query, (data, horario, texto, usuario_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Se a data já existir, atualizar o horário e o texto
            query = "UPDATE horarios SET horario=?, texto=? WHERE data=? AND id=?;"
            self.conn.execute(query, (horario, texto, data, usuario_id))
            self.conn.commit()

    def exibir_horarios(self):
        usuario_id = self.usuario_id
        # Limpar o texto atual
        self.txt_horarios.configure(state=ctk.NORMAL)  # Habilitar edição
        self.txt_horarios.delete(1.0, 'end')

        # Obter a data selecionada
        data_selecionada = self.cal.get_date()

        # Consultar o banco de dados para obter os horários
        query = "SELECT horario, texto FROM horarios WHERE data=? AND id=?;"
        cursor = self.conn.execute(query, (data_selecionada, usuario_id))

        # Exibir os horários associados à data
        for horario_info in cursor.fetchall():
            horario, texto = horario_info
            self.txt_horarios.insert('end', f"Horário: {horario}, Texto: {texto}\n")

        self.txt_horarios.configure(state=ctk.DISABLED)  # Desabilitar edição após exibição

    def __del__(self):
        # Fechar a conexão com o banco de dados ao destruir a instância da classe
        self.conn.close()

    def criar_calendario_usuario(parent, usuario_id=1, database_name="dbbarbearia.db"):
        return CalendarioUsuario(parent, usuario_id, database_name)

    def obter_ano_mes_dia(self):
        hoje = datetime.now()
        return hoje.year, hoje.month, hoje.day