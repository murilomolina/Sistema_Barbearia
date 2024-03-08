import sqlite3
import customtkinter as ctk
from tkinter import ttk

from tela_logada import TelaLogada


class TelaInicial:
    def __init__(self, janela, width, heigth, botao_width):
        self.janela = janela
        self.width = width
        self.heigth = heigth
        self.botao_width = botao_width

        self.frame_titulo()

    def exibir_tela_inicial(self):
        # CTkTabview
        self.tabview = ctk.CTkTabview(self.janela,width=self.width, corner_radius = 20)
        self.tabview.pack()
        self.tabview.add("Login")
        self.tabview.add("Cadastro")
        self.tabview.add("Usuários")
        self.tabview.tab("Login").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Cadastro").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Usuários").grid_columnconfigure(0, weight=1)

        # elementos na Tab (login)
        self.text_login_usuario = ctk.CTkLabel(self.tabview.tab("Login"), text="\nUsuário", font=("Arial", 12, "bold")).pack()
        self.caixa_usuario = ctk.CTkEntry(self.tabview.tab("Login"))
        self.caixa_usuario.pack()

        self.text_senha = ctk.CTkLabel(self.tabview.tab("Login"), text="\nSenha", font=("Arial", 12, "bold")).pack()
        self.caixa_senha = ctk.CTkEntry(self.tabview.tab("Login"))
        self.caixa_senha.pack()

        #confirmar login
        self.botao_confirmar_login = ctk.CTkButton(self.tabview.tab("Login"), text="Confirmar", command=self.tratar_login).pack(pady=10)
        
        #pergunta de segurança (esqueci minha senha)
        self.texto_esqueci_senha = ctk.CTkButton(self.tabview.tab("Login"), text="Esqueci minha senha", font=("Arial", 12), command=self.pergunta_seguranca, width=self.botao_width/0.6, height= self.botao_width/4, corner_radius= self.botao_width/4).pack(pady=10)


        # elementos na Tab (cadastro)
        self.text_cadastro = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Nome do novo usuário", font=("Arial", 12, "bold")).pack(pady=1, side="top")
        self.caixa_cadastro_nome = ctk.CTkEntry(self.tabview.tab("Cadastro"))
        self.caixa_cadastro_nome.pack(pady=1, side="top")

        self.text_senha_cadastro = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Crie uma senha de até 8 digitos", font=("Arial", 12, "bold")).pack(pady=1, side="top")
        self.caixa_senha_cadastro = ctk.CTkEntry(self.tabview.tab("Cadastro"))
        self.caixa_senha_cadastro.pack(pady=1, side="top")

        self.text_funcao_cadastro = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Função do usuario", font=("Arial", 12, "bold")).pack(pady=1, side="top")
        self.caixa_funcao_cadastro = ctk.CTkEntry(self.tabview.tab("Cadastro"))
        self.caixa_funcao_cadastro.pack(pady=1, side="top")

        # Labels e Entry para a Pergunta de Segurança
        self.text_pergunta_seg_cadastro = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Pergunta de segurança", font=("Arial", 12, "bold"))
        self.text_pergunta_seg_cadastro.pack(pady=1, side="top")

        self.caixa_pergunta_seg_cadastro = ctk.CTkEntry(self.tabview.tab("Cadastro"))
        self.caixa_pergunta_seg_cadastro.pack(pady=1, side="top")

        # Labels e Entry para a Resposta de Segurança
        self.text_resposta_seg_cadastro = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Resposta:", font=("Arial", 12, "bold"))
        self.text_resposta_seg_cadastro.pack(pady=1, side="top")

        self.caixa_resposta_seg_cadastro = ctk.CTkEntry(self.tabview.tab("Cadastro"))
        self.caixa_resposta_seg_cadastro.pack(pady=1, side="top")

        # Botão de Cadastrar Usuário (Centralizado)
        self.botao_criar_usuario = ctk.CTkButton(self.tabview.tab("Cadastro"), text="Cadastrar usuário", command=self.cadastrar_usuario)
        self.botao_criar_usuario.pack(pady=10, padx=10, side="top")

        # elementos na Tab (cadastro)
        self.text_usuarios = ctk.CTkLabel(self.tabview.tab("Usuários"), text="\nTodos os usuários já cadastrados no sistema:", font=("Arial", 12, "bold")).pack(pady=10)

    # Adicionar elementos na Tab (Usuários)
        self.exibir_tabela_usuarios()
        #botao excluir usuario na Tab (usuários)
        self.botao_excluir_usuarios = ctk.CTkButton(self.tabview.tab("Usuários"), text="Excluir usuário", command=self.verif_senha_admin, fg_color="red", hover_color = "dark red")
        self.botao_excluir_usuarios.pack(pady = 2)
        
################################## LOGICA BANCO DE DADOS ##################################################################
        
    def get_connection(self):
        return sqlite3.connect('dbbarbearia.db')

    def get_id_usuario(self, nome_usuario):
        try:
           # Criar uma conexão com o banco de dados
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE nomeusuario=?', (nome_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Erro ao obter o ID do usuário: {e}")
            return None
        finally:
            conn.commit()
            conn.close()

    def exibir_tabela_usuarios(self):
        # Criar e exibir a tabela de usuários usando ttk.Treeview
        tabela_frame = ctk.CTkFrame(self.tabview.tab("Usuários"))
        tabela_frame.pack(expand=True, fill="both", pady=0)

        # self.tabela_usuarios = ttk.Treeview(tabela_frame, columns=('id', 'nomeusuario', 'senhausuario', 'funcaousuario'), show='headings')
        self.tabela_usuarios = ttk.Treeview(tabela_frame, columns=('id', 'nomeusuario', 'funcaousuario'), show='headings')

        self.tabela_usuarios.pack(expand=True, fill="both", pady=0)

        # Tentar aplicar um tema escuro
        estilo = ttk.Style()
        estilo.theme_use("clam")
        # Configurar cores para um esquema de cores mais escuro
        estilo.configure("TFrame", background="#333", foregroun="black")
        estilo.configure("TLabel", background="#333", foreground="white")
        estilo.configure("Treeview", background="#444", foreground="white")
        estilo.configure("Treeview.Heading", background="#444", foreground="light blue")
        estilo.configure("Treeview.Row", background="#444", foreground="white")
        # Configurar cores de seleção
        estilo.map("Treeview", background=[("selected", "#333")], foreground=[("selected", "light blue")])

        # Definir cabeçalhos da tabela
        self.tabela_usuarios.heading('id', text='ID')
        self.tabela_usuarios.heading('nomeusuario', text='usuario')
        # self.tabela_usuarios.heading('senhausuario', text='senha')
        self.tabela_usuarios.heading('funcaousuario', text='função')

        # Preencher a tabela com dados
        self.atualizar_tabela_usuarios()

    def atualizar_tabela_usuarios(self):
        try:
            # Verifica se a tabela de usuários está definida
            if self.tabela_usuarios:
                # Limpa a tabela antes de atualizar
                for item in self.tabela_usuarios.get_children():
                    self.tabela_usuarios.delete(item)

                # Preenche novamente com os dados atualizados
                dados_usuarios = self.get_usuarios()[0]
                for usuario in dados_usuarios:
                    if usuario[1] and usuario[2]:
                        # Convertendo a senha para "*" antes de inserir na tabela
                        # usuario_with_masked_senha = (usuario[0], usuario[1], self.mask_senha(usuario[2]), usuario[3])
                        usuario_with_masked_senha = (usuario[0], usuario[1], usuario[3])
                        self.tabela_usuarios.insert('', 'end', values=usuario_with_masked_senha)

        except Exception as e:
            print(f"Erro ao atualizar a tabela de usuários: {e}")

    def get_usuarios(self):
        # Criar uma conexão com o banco de dados
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Criar a tabela se ela não existir
            cursor.execute('CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, nomeusuario TEXT UNIQUE NOT NULL, senhausuario TEXT NOT NULL, funcaousuario TEXT)')

            # Executar a consulta SELECT
            cursor.execute('SELECT * FROM usuarios')
            dados_usuarios = cursor.fetchall()

            cursor.execute('SELECT nomeusuario FROM usuarios')
            resultados = cursor.fetchall()

            nomes_usuarios = [resultado[0] for resultado in resultados]
        finally:
            # Commit e fechar a conexão
            conn.commit()
            conn.close()

        return dados_usuarios, nomes_usuarios

    def usuario_existe(self, novo_usuario):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Consultar se o usuário já existe
        cursor.execute('SELECT * FROM usuarios WHERE nomeusuario = ?', (novo_usuario,))
        usuario_existente = cursor.fetchone() is not None
        # Fechar a conexão
        conn.close()

        return usuario_existente

    def cadastrar_usuario(self):
        novo_usuario = self.caixa_cadastro_nome.get().strip().lower()
        nova_senha = self.caixa_senha_cadastro.get().lower()
        nova_funcao = self.caixa_funcao_cadastro.get().lower()
        pergunta_seguranca = self.caixa_pergunta_seg_cadastro.get().lower()
        resposta_seguranca = self.caixa_resposta_seg_cadastro.get().lower()
        admin_existente = self.verificar_admin_existe()
        # verificar se todos os campos foram preenchidos
        if not all([novo_usuario, nova_senha, nova_funcao, pergunta_seguranca, resposta_seguranca]):
            aviso_label = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Todos os campos devem ser preenchidos!", text_color="red", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            # Agendar a remoção do aviso
            self.tabview.tab("Cadastro").after(5000, lambda: aviso_label.pack_forget())
            return

        #verificar se o nome de usuario atende a pelo menos 2 letras
        if not (len(novo_usuario)>=2):
            aviso_label = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="o nome de usuario deve ter mais que 2 caracteres!", text_color="red", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            # Agendar a remoção do aviso
            self.tabview.tab("Cadastro").after(5000, lambda: aviso_label.pack_forget())
            return
        
        # verificar se já existe um adm
        if novo_usuario == "administrador":
            if admin_existente == True:
                aviso_label = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Usuario Administrador já existe", text_color="red", font=("Arial", 12, "bold"))
                aviso_label.pack(pady=10)
                # Agendar a remoção do aviso
                self.tabview.tab("Cadastro").after(5000, lambda: aviso_label.pack_forget())
                return

        # Verificar se a senha atende aos requisitos
        if not (4 <= len(nova_senha) <= 8):
            aviso_label = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="A senha deve ter entre 4 e 8 caracteres!", text_color="red", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            # Agendar a remoção do aviso
            self.tabview.tab("Cadastro").after(5000, lambda: aviso_label.pack_forget())
            return
        

        # Criar a tabela de perguntas_respostas se não existir
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS perguntas_respostas(id INTEGER PRIMARY KEY AUTOINCREMENT, nomeusuario TEXT UNIQUE NOT NULL, pergunta TEXT NOT NULL, resposta TEXT NOT NULL)')
        conn.commit()
        conn.close()

        
        if not self.usuario_existe(novo_usuario):
            conn = self.get_connection()
            cursor = conn.cursor()

            # Inserir usuário no banco de dados
            cursor.execute('INSERT INTO usuarios (nomeusuario, senhausuario, funcaousuario) VALUES (?, ?, ?)',
                           (novo_usuario, nova_senha, nova_funcao))

            cursor.execute('INSERT INTO perguntas_respostas (pergunta, resposta, nomeusuario) VALUES (?,?,?)', (pergunta_seguranca, resposta_seguranca,novo_usuario))

            conn.commit()
            conn.close()

            # Usuário cadastrado com sucesso, atualiza a tabela na Tabview de Usuários
            self.atualizar_tabela_usuarios()

            aviso_label = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Usuário cadastrado com sucesso", text_color="green", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            # Agendar a remoção do aviso
            self.tabview.tab("Cadastro").after(5000, lambda: aviso_label.pack_forget())

            return novo_usuario, nova_senha
        
        else:
            # Usuário já existe, exibir aviso na Tabview de Cadastro
            aviso_label = ctk.CTkLabel(self.tabview.tab("Cadastro"), text="Nome de usuário já existe!", text_color="red", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            # Agendar a remoção do aviso
            self.tabview.tab("Cadastro").after(5000, lambda: aviso_label.pack_forget())

    def tratar_login(self):
        nome_usuario, senha = self.caixa_usuario.get(), self.caixa_senha.get()
        usuario_id = self.get_id_usuario(nome_usuario=nome_usuario)
        

        if self.verificar_credenciais(nome_usuario, senha):
            aviso_label = ctk.CTkLabel(self.tabview.tab("Login"), text="Credenciais válidas!", text_color="green", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            self.tabview.tab("Login").after(5000, lambda: aviso_label.pack_forget())
            # Cria e exibe a Tela Logada
            tela_logada = TelaLogada(self.janela, self.width, self.heigth, self.botao_width, usuario_id=usuario_id, nome_usuario=nome_usuario)
            tela_logada.exibir_tela_logada()
        else:
            # Credenciais inválidas, exibir mensagem de aviso
            aviso_label = ctk.CTkLabel(self.tabview.tab("Login"), text="Credenciais inválidas!", text_color="red", font=("Arial", 12, "bold"))
            aviso_label.pack(pady=10)
            # Agendar a remoção do aviso
            self.tabview.tab("Login").after(5000, lambda: aviso_label.pack_forget())

    def verificar_credenciais(self, usuario, senha):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Executar a consulta SELECT
            cursor.execute('SELECT * FROM usuarios WHERE nomeusuario=? AND senhausuario=?', (usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                return True
        finally:
            conn.close()

        # Se não houver um resultado, as credenciais são inválidas
        return False
    
    def mask_senha(self, senha):
        # Função para mascarar a senha com "*"
        senha_mascarada = '*' * len(senha)
        return senha_mascarada
    
    #### Pergunta e resposta de segurança ####

    def get_pergunta_resposta(self, nome_usuario):
        # Criar uma conexão com o banco de dados
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Criar a tabela se ela não existir
            cursor.execute('CREATE TABLE IF NOT EXISTS perguntas_respostas(id INTEGER PRIMARY KEY AUTOINCREMENT, nomeusuario TEXT UNIQUE NOT NULL, pergunta TEXT NOT NULL, resposta TEXT NOT NULL)')

            # Executar a consulta SELECT
            cursor.execute('SELECT pergunta, resposta FROM perguntas_respostas WHERE nomeusuario = ?', (nome_usuario,))
            pergunta_resposta = cursor.fetchone()
        finally:
            # Commit e fechar a conexão
            conn.commit()
            conn.close()

        return pergunta_resposta
    
    def get_senha(self, nome_usuario):
        conn = self.get_connection()
        cursor = conn.cursor()
        try: 
            cursor.execute('SELECT senhausuario FROM usuarios WHERE nomeusuario = ?', (nome_usuario,))
            senha_recuperada = cursor.fetchone()
        finally:
            conn.commit()
            conn.close()
        return senha_recuperada
    
    #### Exclusão por admin de usuarios ###

    def get_senha_admin(self, funcao_admin):
        conn = self.get_connection()
        cursor = conn.cursor()
        try: 
            cursor.execute('SELECT senhausuario FROM usuarios WHERE funcaousuario = ?', (funcao_admin,))
            senha_admin = cursor.fetchone()
            if senha_admin == None:
                aviso = ctk.CTkLabel(self.tabview.tab("Usuários"), text="Nenhum admin cadastrado!!!", font=("Arial", 12), text_color="red").pack()
                self.tabview.tab("Usuários").after(5000, lambda: aviso.pack_forget())
                return aviso
        finally:
            conn.commit()
            conn.close()
        return senha_admin[0]
    

    def verificar_admin_existe(self): 
        conn = self.get_connection()
        cursor = conn.cursor()

        # Consultar se o usuário já existe
        cursor.execute('SELECT * FROM usuarios WHERE funcaousuario = "administrador"')
        if cursor.fetchone() is not None:
            # Fechar a conexão
            conn.close()
            return True
        else: 
            conn.close()
            return False 


    def verif_senha_admin(self):
        senha_inserida = ctk.CTkInputDialog( title="Login de administrador", text=f"Adiministrador, insira a sua senha:\n").get_input()
        # Verificar se o usuário logado é administrador
        if self.get_senha_admin("administrador") != senha_inserida:
            aviso = ctk.CTkLabel(self.tabview.tab("Usuários"), text="Apenas administradores podem excluir usuários.\nSenha errada!", font=("Arial", 12), text_color="red")
            aviso.pack(pady=2)
            self.tabview.tab("Usuários").after(5000, lambda: aviso.pack_forget())
            return
        return self.abrir_janela_exclusao_usuarios()

    def abrir_janela_exclusao_usuarios(self):
        # Crie uma nova janela para a exclusão de usuários
        janela_exclusao = ctk.CTkToplevel(self.janela)
        janela_exclusao.title("Exclusão de Usuários")
        janela_exclusao.geometry(f"{400}x{300}")
        janela_exclusao.minsize(height=300, width=400)
    
        # Preencha a lista de usuários
        dados_usuarios = self.get_usuarios()[1]

        if not dados_usuarios:
            # Se não houver usuários, exiba uma mensagem de aviso
            ctk.CTkLabel(janela_exclusao, text="Não há usuários para excluir.", font=("Arial", 12), text_color="red").pack(pady=10)
            return

        # Certifique-se de que dados_usuarios seja uma lista de strings
        dados_usuarios = [str(usuario) for usuario in dados_usuarios]

        # Adicione um Combobox para exibir a lista de usuários
        usuario_para_excluir_combobox = ctk.CTkComboBox(janela_exclusao, values=dados_usuarios)
        usuario_para_excluir_combobox.pack(pady=10)

        # Adicione um botão para executar a exclusão
        ctk.CTkButton(
            janela_exclusao,
            text="Excluir Usuário",
            command=lambda: self.excluir_usuario(usuario_para_excluir_combobox.get()), fg_color='red', hover_color="dark red"
        ).pack(pady=10)

    def excluir_usuario(self, usuario_para_excluir):
        # Conectar ao banco de dados
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Verificar se o usuário a ser excluído existe
            cursor.execute('SELECT * FROM usuarios WHERE nomeusuario=?', (usuario_para_excluir,))
            usuario = cursor.fetchone()

            if usuario:
                # Excluir o usuário
                cursor.execute('DELETE FROM usuarios WHERE nomeusuario=?', (usuario_para_excluir,))
                conn.commit()

                # Exclusão bem-sucedida
                aviso = ctk.CTkLabel(
                    self.tabview.tab("Usuários"),
                    text=f"Usuário {usuario_para_excluir} excluído com sucesso.",
                    font=("Arial", 12),
                    text_color="green"
                )
                aviso.pack(pady=2)

                self.tabview.tab("Usuários").after(5000, lambda: aviso.pack_forget())

            else:
                # Usuário não encontrado
                aviso = ctk.CTkLabel(
                    self.tabview.tab("Usuários"),
                    text=f"Usuário {usuario_para_excluir} não encontrado.",
                    font=("Arial", 12),
                    text_color="red"
                ).pack()
                self.tabview.tab("Usuários").after(5000, lambda: aviso.pack_forget())

        finally:
            # Fechar a conexão com o banco de dados
            conn.close()
            self.atualizar_tabela_usuarios()


##########################################################################################################################################

    def frame_titulo(self):
        # Frame acima da Tabview
        frame_superior = ctk.CTkFrame(self.janela, corner_radius=20)
        frame_superior.pack(side="top", expand=False, fill="none")

        # Texto (título) e Subtitulo no Frame Superior
        texto_titulo = ctk.CTkLabel(frame_superior, text="Barbearia EQUIPE 05", font=("Helvetica", 26, "bold"))
        texto_titulo.pack(pady=20, padx=100)

        subtitulo = ctk.CTkLabel(frame_superior, text="Bem-vindo à Barbearia Equipe 05", font=("Arial", 14))
        subtitulo.pack(pady=10)

    def pergunta_seguranca(self):
        nome_usuario = ctk.CTkInputDialog(title="Nome de Usuário", text="Digite seu nome de usuário:")
        nome_usuario_input = nome_usuario.get_input()

        # Verificar se o nome de usuário é válido (já existente no banco de dados)
        if self.usuario_existe(nome_usuario_input):
            # Recuperar pergunta e resposta associadas ao nome de usuário
            pergunta_resposta = self.get_pergunta_resposta(nome_usuario_input)

            if pergunta_resposta:
                pergunta = pergunta_resposta[0]
                resposta_correta = pergunta_resposta[1]

                # Perguntar a pergunta de segurança
                resposta_usuario = ctk.CTkInputDialog(title="Pergunta de Segurança", text=f"Responda para ter acesso a sua senha:\n{pergunta}").get_input()

                # Verificar se a resposta do usuário está correta
                if resposta_usuario == resposta_correta:
                    senha_perdida = self.get_senha(nome_usuario_input)
                    resp = ctk.CTkLabel(self.tabview.tab("Login"), text=f"Sua senha é: {senha_perdida[0]}", font=("Arial", 12), text_color="green")
                    resp.pack()
                    self.tabview.tab("Login").after(15000, lambda: resp.pack_forget())
                else:
                    erro_pergunta_seguranca = ctk.CTkLabel(self.janela, text="Resposta incorreta!", font=("Arial", 12), text_color="red")
                    erro_pergunta_seguranca.pack()
                    self.tabview.tab("Login").after(5000, lambda: erro_pergunta_seguranca.pack_forget())
            else:
                erro_pergunta_seguranca = ctk.CTkLabel(self.janela, text="Pergunta e resposta não encontradas.", font=("Arial", 12), text_color="red")
                erro_pergunta_seguranca.pack()
                self.tabview.tab("Login").after(5000, lambda: erro_pergunta_seguranca.pack_forget())
        else:
            erro_pergunta_seguranca = ctk.CTkLabel(self.janela, text="Nome de usuário incorreto.", font=("Arial", 12), text_color="red")
            erro_pergunta_seguranca.pack()
            self.tabview.tab("Login").after(5000, lambda: erro_pergunta_seguranca.pack_forget())
