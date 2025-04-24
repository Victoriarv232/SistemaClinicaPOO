"""Situação problema:
Fila de espera / atendimento médico
Cada Consultório atende 20 pacientes por dia
Senha Preferencial e Normal
CG  (3) - CG60
GIN (2) - GIN40
PED (2) - PED40
GER (2) - GER40
ORT (2) - ORT40

Guichê (2)
Cada atendimento demora em média 5 minutos"""


class Paciente:
    def __init__(self, setor, senha, preferencial):
        self.setor = setor
        self.senha = senha
        self.preferencial = preferencial

    def __repr__(self):
        return f"{self.senha} ({'Preferencial' if self.preferencial else 'Normal'}) - {self.setor}"


class GeradorSenhaUnico:
    def __init__(self, sigla, limite):
        self.sigla = sigla
        self.limite = limite
        self.contador = 1

    def gerar_senha(self, preferencial=False):
        if self.contador > self.limite:
            return None
        prefixo = f"{self.sigla}P" if preferencial else self.sigla
        senha = f"{prefixo}{self.contador:02d}"
        self.contador += 1
        return senha

    def senhas_restantes(self):
        return max(0, self.limite - self.contador + 1)

    def resetar(self):
        self.contador = 1


consultorios = {
    'CG - Clínica Geral': {'sigla': 'CG', 'limite': 60},
    'GIN - Ginecologia': {'sigla': 'GIN', 'limite': 40},
    'PED - Pediatria': {'sigla': 'PED', 'limite': 40},
    'GER - Geriatria': {'sigla': 'GER', 'limite': 40},
    'ORT - Ortopedia': {'sigla': 'ORT', 'limite': 40},
}


def inicializar_sistema():
    fila = []
    geradores = {}
    for nome, info in consultorios.items():
        geradores[nome] = GeradorSenhaUnico(info["sigla"], info["limite"])
    return fila, geradores


fila_espera, geradores = inicializar_sistema()


def gerar_senha():
    print("\nSetor de atendimento:")
    for i, setor in enumerate(consultorios):
        print(f"{i+1}. {setor}")
    setor_escolhido = list(consultorios.keys())[int(input("Selecione: ")) - 1]

    print("\nVocê é preferencial?\n1. Sim\n2. Não")
    preferencial = int(input("Selecione: ")) == 1

    senha = geradores[setor_escolhido].gerar_senha(preferencial)
    if senha is None:
        print(f"\n⚠️ Limite de senhas atingido para {setor_escolhido}.")
        return

    paciente = Paciente(setor_escolhido, senha, preferencial)
    fila_espera.append(paciente)

    print(f"\nSenha gerada: {senha}")
    print("Aguarde ser chamado no painel.")


def chamar_paciente_guiche(guiche_num):
    for i, paciente in enumerate(fila_espera):
        if paciente.preferencial:
            chamado = fila_espera.pop(i)
            print(f"Guichê {guiche_num}: {chamado}")
            return
    if fila_espera:
        chamado = fila_espera.pop(0)
        print(f"Guichê {guiche_num}: {chamado}")
    else:
        print(f"Guichê {guiche_num}: Nenhum paciente na fila.")


def chamar_pacientes_dois_guiches():
    print("\nChamando pacientes...")
    chamar_paciente_guiche(1)
    chamar_paciente_guiche(2)


def ver_fila():
    if not fila_espera:
        print("\nFila está vazia.")
    else:
        print("\nFila atual:")
        for paciente in fila_espera:
            print(f" - {paciente}")


def ver_senhas_restantes():
    print("\nSenhas restantes por setor:")
    for setor, gerador in geradores.items():
        restante = gerador.senhas_restantes()
        print(f" - {setor}: {restante} senha(s) disponíveis")


def resetar_sistema():
    global fila_espera, geradores
    fila_espera, geradores = inicializar_sistema()
    print("\nSistema resetado com sucesso. Novo dia de atendimentos iniciado.")


# Menu principal
while True:
    print("\n--- Menu ---")
    print("1. Gerar senha")
    print("2. Chamar pacientes (Guichês 1 e 2)")
    print("3. Ver fila")
    print("4. Ver senhas restantes")
    print("5. Resetar sistema (novo dia)")
    print("6. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        gerar_senha()
    elif opcao == '2':
        chamar_pacientes_dois_guiches()
    elif opcao == '3':
        ver_fila()
    elif opcao == '4':
        ver_senhas_restantes()
    elif opcao == '5':
        resetar_sistema()
    elif opcao == '6':
        print("\nEncerrando sistema.")
        break
    else:
        print("Opção inválida.")
