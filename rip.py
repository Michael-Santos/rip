import socket
import json
import sys

#############################################################################
# Configuração da arquitetura
#############################################################################

# Define o endereço de cada interface de cada um dos roteadores
NODE0_INTERFACES_ADD = [ '192.168.1.100', '192.168.2.100', '192.168.3.100' ]
NODE1_INTERFACES_ADD = [ '192.168.1.200', '192.168.5.100' ]
NODE2_INTERFACES_ADD = [ '192.168.3.200', '192.168.4.100' ]
NODE3_INTERFACES_ADD = [ '192.168.5.200', '192.168.2.200', '192.168.4.200' ]

PORT = 1000

# Define a tabela RIP inicial e cada Roteador
NODE0_TABLE_RIP = [{"numeroRoteador": 0, "distancia": 0 , "proximoNumeroRoteador": None, "interface": None}]
NODE1_TABLE_RIP = [{"numeroRoteador": 1, "distancia": 0 , "proximoNumeroRoteador": None, "interface": None}]
NODE2_TABLE_RIP = [{"numeroRoteador": 2, "distancia": 0 , "proximoNumeroRoteador": None, "interface": None}]
NODE3_TABLE_RIP = [{"numeroRoteador": 3, "distancia": 0 , "proximoNumeroRoteador": None, "interface": None}]


# Inicializa a tabela de RIP do Roteador
def inicializarTabelaRIP(numeroRoteador):
	switcher = {
		0: NODE0_TABLE_RIP,
		1: NODE1_TABLE_RIP,
		2: NODE2_TABLE_RIP,
		3: NODE3_TABLE_RIP
	}

	tabelaInicial = switcher.get(numeroRoteador, [])
	return(tabelaInicial)

# Configura os endereços de cada interface do roteador
def configurarInterfaces(numeroRoteador):
	switcher = {
		0: NODE0_INTERFACES_ADD,
		1: NODE1_INTERFACES_ADD,
		2: NODE2_INTERFACES_ADD,
		3: NODE3_INTERFACES_ADD
	}

	enderecos = switcher.get(numeroRoteador, [])
	return(enderecos)

# Configura o roteador
def configurarRoteador(numeroRoteador):
	enderecos = configurarInterfaces(numeroRoteador)
	tabelaInicial = inicializarTabelaRIP(numeroRoteador)
	return(enderecos, tabelaInicial)


#############################################################################
# Configuração da arquitetura
#############################################################################


#def receiver():


#def serder():


#############################################################################
# Programa principal
#############################################################################

registrosAlterados = []

# Recebe o número do roteador e configura-o
numeroRoteador = int(input("Digite o número do nó: "))
enderecos, tabelaRegistros = configurarRoteador(numeroRoteador)

if not enderecos and not tabelaRegistros:
	exit("Não existe roteador: Digite um número entre 0 e 3\nNão foi possível construir tabela RIP")

# Exibe as interfaces e a tabela atual
print(enderecos)
print("")
print(tabelaRegistros)
