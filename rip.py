import socket
import json
import sys
import threading
import socket
import random
import time

#############################################################################
# Configuração da arquitetura
#############################################################################

# Define o endereço de cada interface de cada um dos roteadores
NODE0_INTERFACES_ADD = [ '192.168.1.100', '192.168.2.100', '192.168.3.100' ]
NODE1_INTERFACES_ADD = [ '192.168.1.200', '192.168.5.100' ]
NODE2_INTERFACES_ADD = [ '192.168.3.200', '192.168.4.100' ]
NODE3_INTERFACES_ADD = [ '192.168.5.200', '192.168.2.200', '192.168.4.200' ]

# Define o endereço de cada interface vizinha de cada um dos roteadores (Cada posição no vetor é o índice da interface de saída)
NODE0_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.1.200', '192.168.2.200', '192.168.3.200' ]
NODE1_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.1.100', '192.168.5.200' ]
NODE2_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.3.100', '192.168.4.200' ]
NODE3_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.5.100', '192.168.2.100', '192.168.4.100' ]

# Armazena o id dos roteadores vizinhos
NODE0_ID_NEIGHBORHOOD = [ 1, 2, 3 ]
NODE1_ID_NEIGHBORHOOD = [ 0, 3 ]
NODE2_ID_NEIGHBORHOOD = [ 0, 3 ]
NODE3_ID_NEIGHBORHOOD = [ 0, 1, 2 ]

PORT = 10000

# Define a tabela RIP inicial de cada Roteador
NODE0_TABLE_RIP = [{"numeroRoteador": 0, "distancia": 0 , "proximoNumeroRoteador": "-"},
					{"numeroRoteador": 1, "distancia": 99999 , "proximoNumeroRoteador": 1},
					{"numeroRoteador": 2, "distancia": 99999 , "proximoNumeroRoteador": 2},
					{"numeroRoteador": 3, "distancia": 99999 , "proximoNumeroRoteador": 3}
]
NODE1_TABLE_RIP = [{"numeroRoteador": 0, "distancia": 99999 , "proximoNumeroRoteador": 0},
					{"numeroRoteador": 1, "distancia": 0 , "proximoNumeroRoteador": "-"},
					{"numeroRoteador": 2, "distancia": 99999 , "proximoNumeroRoteador": "-"},
					{"numeroRoteador": 3, "distancia": 99999 , "proximoNumeroRoteador": 3}
]
NODE2_TABLE_RIP = [{"numeroRoteador": 0, "distancia": 99999 , "proximoNumeroRoteador": 0},
					{"numeroRoteador": 1, "distancia": 99999 , "proximoNumeroRoteador": "-"},
					{"numeroRoteador": 2, "distancia": 0 , "proximoNumeroRoteador": "-"},
					{"numeroRoteador": 3, "distancia": 99999 , "proximoNumeroRoteador": 3}
]
NODE3_TABLE_RIP = [{"numeroRoteador": 0, "distancia": 99999 , "proximoNumeroRoteador": 0},
					{"numeroRoteador": 1, "distancia": 99999 , "proximoNumeroRoteador": 1},
					{"numeroRoteador": 2, "distancia": 99999 , "proximoNumeroRoteador": 2},
					{"numeroRoteador": 3, "distancia": 0 , "proximoNumeroRoteador": "-"}					
]


#############################################################################
# Inicialização do roteador
#############################################################################

# Inicializa a tabela de RIP do Roteador
def inicializarTabelaRIP(idRoteador):
	switcher = {
		0: NODE0_TABLE_RIP,
		1: NODE1_TABLE_RIP,
		2: NODE2_TABLE_RIP,
		3: NODE3_TABLE_RIP
	}

	tabelaInicial = switcher.get(idRoteador, [])
	return(tabelaInicial)

# Configura os endereços de cada interface do roteador
def configurarInterfacesEntrada(idRoteador):
	switcher = {
		0: NODE0_INTERFACES_ADD,
		1: NODE1_INTERFACES_ADD,
		2: NODE2_INTERFACES_ADD,
		3: NODE3_INTERFACES_ADD
	}

	interfaces = switcher.get(idRoteador, [])
	return(interfaces)

def configurarInterfacesSaida(idRoteador):
	switcher = {
		0: NODE0_INTERFACES_ADD_NEIGHBORHOOD,
		1: NODE1_INTERFACES_ADD_NEIGHBORHOOD,
		2: NODE2_INTERFACES_ADD_NEIGHBORHOOD,
		3: NODE3_INTERFACES_ADD_NEIGHBORHOOD
	}

	interfaces = switcher.get(idRoteador, [])
	return(interfaces)

# Configura o roteador
def inicializarRoteador(idRoteador):
	interfacesEntrada = configurarInterfacesEntrada(idRoteador)
	interfacesSaida = configurarInterfacesSaida(idRoteador)
	tabelaInicial = inicializarTabelaRIP(idRoteador)
	return(interfacesEntrada, interfacesSaida, tabelaInicial)


def alterarDistancias(idRoteador, tabelaRegistros, idVizinhos):
	for idVizinho in idVizinhos:
		peso = input("Digite um peso para enlace ligando ao roteador de id {}:".format(idVizinho))
		tabelaRegistros[idVizinho]["distancia"] = int(peso)

def obterVizinhos(idRoteador):
	switcher = {
		0: NODE0_ID_NEIGHBORHOOD,
		1: NODE1_ID_NEIGHBORHOOD,
		2: NODE2_ID_NEIGHBORHOOD,
		3: NODE3_ID_NEIGHBORHOOD
	}

	idVizinhos = switcher.get(idRoteador, [])
	return(idVizinhos)

#############################################################################
# Configuração de envio/recebimento mensagens com socket
#############################################################################

# Envia mensagem em "Broadcast"
def enviarBroadcast(interfaces, mensagem):
	for interface in interfaces:
		sender(interface, mensagem)

# Recebe mensagens via socket UDP
def receiver(idRoteador, interfaces, tabelaRegistros, idVizinhos):
	server_address = (interface, PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(server_address)

	while(True):
		data, address = sock.recvfrom(4096)
		#time.sleep(random.randint(1, 10))

		jsonMessage = json.loads(data.decode('utf-8'))
		print(jsonMessage)
		atualizarTabelaRIP(idRoteador, interfaces, tabelaRegistros, idVizinhos, jsonMessage)

# Envia mensagens via socket UDP
def sender(interface, mensagem):
	server_address = (interface, PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = json.dumps(mensagem)
	sent = sock.sendto(data.encode('utf-8'), server_address)

#############################################################################
# Execução do RIP
#############################################################################

# Atualiza a tabela RIP com a mensagem recebida do roteador vizinho
def atualizarTabelaRIP(idRoteador, interfaces, tabelaRegistros, idVizinhos, mensagem):
	# Obtém identificador do roteador remetente
	idRemetente = mensagem["idRemetente"]
	
	# Atualiza a distância até o roteador remetente
	distanciaRemetenteAteAtual = mensagem["tabelaRegistros"][idRoteador]["distancia"]
	distanciaAtualAteRemetente = tabelaRegistros[idRemetente]["distancia"]
	
	ocorreuAtualizacao = False

	if distanciaAtualAteRemetente != distanciaRemetenteAteAtual:
		ocorreuAtualizacao = True
		tabelaRegistros[idRemetente]["distancia"] = distanciaRemetenteAteAtual

	for i in range(4):
		if i == idRoteador:
			continue
			
		distanciaRecebida = mensagem["tabelaRegistros"][i]["distancia"]
		distanciaAtual = tabelaRegistros[i]["distancia"]

		if (distanciaRecebida+distanciaAtualAteRemetente < distanciaAtual):
			tabelaRegistros[i]["distancia"] = distanciaRecebida+distanciaAtualAteRemetente
			tabelaRegistros[i]["proximoNumeroRoteador"] = idRemetente
			ocorreuAtualizacao = True


	print("Recebida mensagem RIP do roteador {}".format(idRemetente))
	exibirTabelaRIP(tabelaRegistros)
	
	if ocorreuAtualizacao:
	#	enviarTabelaRIPVizinhos(idRoteador, interfaces, tabelaRegistros)
		print(ocorreuAtualizacao)

# Realiza o envio da tabela atual para os roteadores vizinhos
def enviarTabelaRIPVizinhos(idRoteador, tabelaRegistros, interfacesSaida):
	mensagemRIP = {"idRemetente": idRoteador, "tabelaRegistros": tabelaRegistros}
	enviarBroadcast(interfacesSaida, mensagemRIP)
	#print(json.dumps(jsonMessage, indent=4))

#############################################################################
# Exibir informações
#############################################################################

# Exibe registros
def exibirTabelaRIP(tabela):
	print("##########################################")
	print("# Nº Rotedor | Distancia | Prox Roteador #")
	print("##########################################")

	for registro in tabela:
		distancia = "    -    " if registro["distancia"] == 99999 else str(registro["distancia"])
		print('#      {}     | {} |       {}       #'.format(			
			registro["numeroRoteador"], str(distancia).center(9),
			registro["proximoNumeroRoteador"]))
	
	print("##########################################")

def exibirInterfaces(interfaces):
	print("\nEndereço das interfaces:")
	for i in range(len(interfaces))	:
		print("Interface {}: \"{}\"".format(i, interfaces[i]))
	print("")	

def exibirMenu():
	print("#################################")
	print("# O que deseja fazer?           #")
	print("#################################")
	print("# 1 - Mudar pesos               #")
	print("# 2 - Iniciar RIP               #")
	print("#################################")


#############################################################################
# Programa principal
#############################################################################

# Recebe o número do roteador e configura-o
idRoteador = int(input("Digite o número do nó: "))
interfacesEntrada, interfacesSaida, tabelaRegistros = inicializarRoteador(idRoteador)

if not interfacesEntrada and not interfacesSaida and not tabelaRegistros:
	exit("Não existe roteador: Digite um número entre 0 e 3\nNão foi possível construir tabela RIP")

print("")

# Inicializar distância para vizinho
idVizinhos = obterVizinhos(idRoteador)
alterarDistancias(idRoteador, tabelaRegistros, idVizinhos)

# Exibe as interfaces e a tabela atual
exibirInterfaces(interfacesEntrada)	
exibirTabelaRIP(tabelaRegistros)

# Cria uma thread para receber mensagens em cada interface
for interface in interfacesEntrada:
	t = threading.Thread(target=receiver, args=(idRoteador, interface, tabelaRegistros, idVizinhos))
	t.start()

while(True):
	input()
	exibirMenu()
	print("")
	opcao = input("Opção: ")

	if int(opcao) == 1:
		alterarDistancias(idRoteador, tabelaRegistros, idVizinhos)
		exibirTabelaRIP(tabelaRegistros)
	else:
		enviarTabelaRIPVizinhos(idRoteador, tabelaRegistros, interfacesSaida)
#############################################################################
# Formato da mensagem será um Json com seguinte campos:
# idRemetende
# tabelaRemetente
#############################################################################


