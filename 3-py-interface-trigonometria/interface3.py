# Calculadora Trigonométrica — versão orientada a objetos
# Calcula seno, cosseno e tangente de um ângulo entre 0 e 90 graus.

import tkinter as tk
import math
from PIL import Image, ImageTk
import os
import sys

# Obtém o caminho absoluto para um recurso, funcionando tanto rodando
# o py. normalmente quanto depois de ser empacotado com PyInstaller.
def resource_path(relative_path):
    try:  # PyInstaller cria uma pasta temporária e guarda o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:  # Se não estiver rodando via PyInstaller, usa a pasta do arquivo
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class TrigCalculator:
    
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora Trigonométrica")
        self.janela.geometry("400x550")
        self.janela.configure(bg="#f0f0f0")
        
        self.carregar_icone()
        self.criar_widgets()
        
    # Define o ícone da janela
    def carregar_icone(self):
        try:
            icone = Image.open(resource_path("seno.png"))
            self.icone_foto = ImageTk.PhotoImage(icone)
            self.janela.iconphoto(True, self.icone_foto)
        except FileNotFoundError:
            print("Imagem 'seno.png' não encontrada para o ícone da janela.")
            
    # Monta todos os widgets da tela
    def criar_widgets(self):
        self.criar_imagem_topo()
        self.criar_campo_entrada()
        self.criar_botoes()
        self.criar_resultados()
        
    # Imagem ilustrativa no topo da janela
    def criar_imagem_topo(self):
        try:
            imagem = Image.open(resource_path("seno2.png"))
            imagem = imagem.resize((380, 200), Image.Resampling.LANCZOS)
            self.foto_topo = ImageTk.PhotoImage(imagem) # guarda a referência
            
            label_imagem = tk.Label(self.janela, image=self.foto_topo, bg="#f0f0f0", borderwidth=0)
            label_imagem.pack(pady=20)
        except FileNotFoundError:
            tk.Label(self.janela, text="Imagem 'seno2.png' não encontrada.", bg="#f0f0f0").pack(pady=20)
            
    # Campo onde o usuário digita o ângulo
    def criar_campo_entrada(self):
        frame_entrada = tk.Frame(self.janela, bg="#f0f0f0")
        frame_entrada.pack(pady=10)
        
        tk.Label(frame_entrada, text="Ângulo (0 à 90):", font=("Times New Roman", 16), bg="#f0f0f0").pack(pady=(0, 5))
        
        # register() conecta a função Python validar_entrada ao mecanismo de validação nativo do Tkinter
        validacao = self.janela.register(self.validar_entrada)
        self.entrada_angulo = tk.Entry(
            frame_entrada,
            width=3,
            justify="center",
            font=("Times New Roman", 16),
            bd=0,
            highlightthickness=0,
            relief="flat",
            fg="red",
            validate="key",
            validatecommand=(validacao, "%P"),
        )  
        self.entrada_angulo.pack()
        
        #Linha decorativa abaixo do campo de entrada
        tk.Frame(frame_entrada, bg="black", height=1, width=40).pack(pady=(0, 5))
        
    # Botões de calcular e limpar
    def criar_botoes(self):
        frame_botoes = tk.Frame(self.janela, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        tk.Button(
            frame_botoes,
            text="Calcular",
            command=self.calcular,
            font=("Times New Roman", 16),
            bg="#d9d9d9",
            relief="flat",
            bd=0,
            highlightthickness=0,
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            frame_botoes,
            text="Limpar",
            command=self.limpar,
            font=("Times New Roman", 16),
            bg="#d9d9d9",
            relief="flat",
            bd=0,
            highlightthickness=0,
        ).pack(side=tk.LEFT, padx=10)
        
    # Labels que mostram os resultados de seno, cosseno e tangente
    def criar_resultados(self):
        frame_resultados = tk.Frame(self.janela, bg="#f0f0f0")
        frame_resultados.pack(pady=10)
        
        self.resultado_seno = self._criar_linha_resultado(frame_resultados, 0, "Seno: ")
        self.resultado_cosseno = self._criar_linha_resultado(frame_resultados, 1, "Cosseno: ")
        self.resultado_tangente = self._criar_linha_resultado(frame_resultados, 2, "Tangente: ")
        
    # Criar um par (label descritiva + label de resultado) numa linha do grid
    # Método auxiliar para não repetir o mesmo bloco 3 vezes
    def _criar_linha_resultado(self, frame, linha, texto):
        tk.Label(frame, text=texto, font=("Times New Roman", 16), bg="#f0f0f0").grid(
        row=linha, column=0, padx=10, pady=5, sticky="e")
        resultado = tk.Label(frame, text="", font=("Times New Roman", 16), fg="red", bg="#f0f0f0")
        resultado.grid(row=linha, column=1, padx=10, pady=5, sticky="w")
        return resultado
    
    # Calcula seno, cosseno e tangente do ângulo digitado
    def calcular(self):
        try:
            angulo = float(self.entrada_angulo.get())
            
            radiano= math.radians(angulo)
            seno = math.sin(radiano)
            cosseno = math.cos(radiano)
            
            self.resultado_seno.config(text=f"{seno:.3f}")
            self.resultado_cosseno.config(text=f"{cosseno:.3f}")
            
            # Tangente de 90° é indefinida (divisão por zero)
            if angulo == 90:
                self.resultado_tangente.config(text="Indefinido")
            else:
                tangente = math.tan(radiano)
                self.resultado_tangente.config(text=f"{tangente:.3f}")
        except ValueError:
            self.resultado_seno.config(text="Erro")
            self.resultado_cosseno.config(text="Erro")
            self.resultado_tangente.config(text="Erro")
            
    # Limpa o campo de entrada e os resultados
    def limpar(self):
        self.entrada_angulo.delete(0, tk.END)
        self.resultado_seno.config(text="")
        self.resultado_cosseno.config(text="")
        self.resultado_tangente.config(text="")
        
    # Só permite números de 0 a 90 no campo de ângulo (chamado a tecla)
    def validar_entrada(self, texto):
        if texto == "":
            return True
        try:
            valor = float(texto)
            return 0 <= valor <= 90
        except ValueError:
            return False
    
    def executar(self):
        self.janela.mainloop()
        
if __name__ == "__main__":
    app = TrigCalculator()
    app.executar()