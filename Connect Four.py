import random #Para PvE
import os     #Chamando o sistema operacional para colocar cor nos círculos

class Tabuleiro:
    def __init__(self):#Definições básicas de tamanho
        self.linhas = 6
        self.colunas = 7
        #Lista de letras para mapear a entrada do usuário
        self.letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        
        #Códigos de cor para o terminal
        self.peca_azul = '\033[94mO\033[0m'     #Círculo azul 
        self.peca_vermelha = '\033[91mO\033[0m' #Círculo vermelho
        self.vazio = ' '
        
        #Tabuleiro privado (Encapsulamento) ninguém fora da classe deve mexer diretamente
        self.__tab = [[self.vazio for _ in range(self.colunas)] for _ in range(self.linhas)]

    # --- MÉTODOS VISUAIS ---
    def exibir(self):
        #Cabeçalho com letras (a - g)
        print('\n   a   b   c   d   e   f   g', end='') 
        print('\n  ' + '+---'*self.colunas+'+') #Desenha o teto do tabuleiro
        for linha in range(self.linhas):#Laço para percorrer cada linha (de 0 a 5)
            print(f'{linha} |', end='') #Mostra o número da linha na esquerda
            for coluna in range(self.colunas): #Laço para percorrer cada coluna dentro daquela linha
                celula = self.__tab[linha][coluna] #linha+coluna=célula
                print(f' {celula} ', end='|')
            print('\n  '+'+---'*self.colunas+'+') #Desenha o "chão" de cada linha

    #--- LÓGICA DO TABULEIRO ---

    def coluna_cheia(self, coluna_idx): #Verifica se o topo da coluna já tem peça
        return self.__tab[0][coluna_idx] != self.vazio

    def inserir_peca(self, coluna_idx, jogador_tipo):#Define qual cor usar baseado no jogador 
        peca = self.peca_azul if jogador_tipo == "Azul" else self.peca_vermelha
        for linha in range(self.linhas - 1, -1, -1):#Procura a primeira linha vazia de baixo para cima
            if self.__tab[linha][coluna_idx] == self.vazio:
                self.__tab[linha][coluna_idx] = peca
                return True #Sucesso
        return False #Não achou espaço

#Verificar vencedor
    def verificar_vitoria(self, jogador_tipo):
        peca = self.peca_azul if jogador_tipo == "Azul" else self.peca_vermelha
        
        # Checagem Horizontal
        #l=linha
        #c=coluna
        for l in range(self.linhas):#Para cada linha
            for c in range(self.colunas - 3):#Para cada coluna dessa linha, vai até -3 para não acessar índices fora da lista
                if (self.__tab[l][c] == peca and self.__tab[l][c+1] == peca and self.__tab[l][c+2] == peca and self.__tab[l][c+3] == peca):
                    return True
        
        # Checagem Vertical
        for c in range(self.colunas):
            for l in range(self.linhas - 3):
                if (self.__tab[l][c] == peca and self.__tab[l+1][c] == peca and 
                    self.__tab[l+2][c] == peca and self.__tab[l+3][c] == peca):
                    return True
        
        # Diagonal Descendo
        for l in range(self.linhas - 3):
            for c in range(self.colunas - 3):
                if (self.__tab[l][c] == peca and self.__tab[l+1][c+1] == peca and self.__tab[l+2][c+2] == peca and self.__tab[l+3][c+3] == peca):
                    return True
        
        # Diagonal Subindo
        for l in range(self.linhas - 3):
            for c in range(3, self.colunas):
                if (self.__tab[l][c] == peca and self.__tab[l+1][c-1] == peca and self.__tab[l+2][c-2] == peca and self.__tab[l+3][c-3] == peca):
                    return True
        return False

    def tabuleiro_cheio(self):#Se não houver espaço vazio na linha do topo de nenhuma coluna
        for c in range(self.colunas):
            if self.__tab[0][c] == self.vazio:
                return False
        return True


class Jogo:
    def __init__(self):
        self.tabuleiro = Tabuleiro() #Cria o objeto Tabuleiro
        self.jogador_atual = "Azul"  #Começa com o Azul

    # --- MÉTODOS DE CONTROLE ---

    def jogar_humano(self):
        while True:
            entrada = input(f"Jogador {self.jogador_atual}, escolha coluna (a-g): ").lower().strip()
            if entrada in self.tabuleiro.letras:#Verifica se é uma letra válida
                col_idx = self.tabuleiro.letras.index(entrada) #Converte letra para número
                if not self.tabuleiro.coluna_cheia(col_idx):
                    return col_idx
                else:
                    print(">> Essa coluna está cheia! Tente outra.")
            else:
                print(">> Entrada inválida! Digite uma letra de 'a' a 'g'.")

    def jogar_computador(self):
        print(f"Computador ({self.jogador_atual}) pensando...")
        validas = [] #Cria lista de colunas livres para escolher aleatoriamente
        for c in range(7):
            if not self.tabuleiro.coluna_cheia(c):
                validas.append(c)
        escolha = random.choice(validas)
        letra_escolhida = self.tabuleiro.letras[escolha] #Mostra qual letra o computador escolheu (para o humano entender)
        print(f">> O Computador jogou na coluna '{letra_escolhida}'")
        return escolha

    def alternar_jogador(self):
        self.jogador_atual = "Vermelho" if self.jogador_atual == "Azul" else "Azul"

    def iniciar(self, contra_pc):
        print("\n=== CONNECT FOUR ===")
        self.tabuleiro.exibir()
        while True:
            if contra_pc and self.jogador_atual == "Vermelho": # Computador joga se for o turno dele e o modo PVE estiver ativo
                coluna = self.jogar_computador()
            else:
                coluna = self.jogar_humano()
            # Insere a peça e mostra o estado atual
            self.tabuleiro.inserir_peca(coluna, self.jogador_atual)
            self.tabuleiro.exibir()
            # Verifica condições de fim de jogo
            if self.tabuleiro.verificar_vitoria(self.jogador_atual):
                print(f"\nParabéns! Jogador {self.jogador_atual} venceu!")
                break

            if self.tabuleiro.tabuleiro_cheio():
                print("\nEmpate! O tabuleiro lotou.")
                break

            self.alternar_jogador()

def main():
    print("Escolha o modo de jogo:")
    print("1 - Humano x Humano")
    print("2 - Humano x Computador")

    while True:
        modo = input("Opção: ")
        if modo in ["1", "2"]:
            break
        print("Opção inválida!")

    jogo = Jogo()
    jogo.iniciar(contra_pc=(modo == "2"))

if __name__ == "__main__":
    main()