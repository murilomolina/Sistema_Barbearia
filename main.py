import customtkinter as ctk
from tela_inicial import TelaInicial
import os



janela_principal_width = 800
janela_principal_heigth = 500
botao_width = 100

#configuração da janela inicial
janela = ctk.CTk()
janela._set_appearance_mode("dark")
janela.geometry(f"{janela_principal_width}x{janela_principal_heigth}")
janela.minsize(height=janela_principal_heigth, width=janela_principal_width)

TelaInicial(janela, janela_principal_width, janela_principal_heigth, botao_width)

# Nome do arquivo (ocultar)
nome_arquivo = 'dbbarbearia.db'
# Caminho completo para o arquivo
caminho_arquivo = os.path.abspath(nome_arquivo)
# Comando para tornar o arquivo oculto no Windows
os.system(f'attrib +h "{caminho_arquivo}"')

janela.mainloop()