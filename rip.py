import socket
import json
import sys
import threading
import socket

#############################################################################
# Configuração da arquitetura
#############################################################################

# Define o endereço de cada interface de cada um dos roteadores
NODE0_INTERFACES_ADD = [ '192.168.1.100', '192.168.2.100', '192.168.3.100' ]
NODE1_INTERFACES_ADD = [ '192.168.1.200', '192.168.5.100' ]
NODE2_INTERFACES_ADD = [ '192.168.3.200', '192.168.4.100' ]
NODE3_INTERFACES_ADD = [ '192.168.5.200', '192.168.2.200', '192.168.4.200' ]

# Define o endereço de cada interface vizinha de cada um dos roteadores
NODE0_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.1.200', '192.168.2.200', '192.168.3.200' ]
NODE1_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.1.100', '192.168.5.200' ]
NODE2_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.3.100', '192.168.4.100' ]
NODE3_INTERFACES_ADD_NEIGHBORHOOD = [ '192.168.5.100', '192.168.2.100', '192.168.4.100' ]

PORT = 10000

# Define a tabela RIP inicial e cada Roteador
NODE0_TABLE_RIP = [{"numeroRoteador": 0, "distancia": 0 , "proximoNumeroRoteador": "-", "interface": "-"}]
NODE1_TABLE_RIP = [{"numeroRoteador": 1, "distancia": 0 , "proximoNumeroRoteador": "-", "interface": "-"}]
NODE2_TABLE_RIP = [{"numeroRoteador": 2, "distancia": 0 , "proximoNumeroRoteador": "-", "interface": "-"}]
NODE3_TABLE_RIP = [{"numeroRoteador": 3, "distancia": 0 , "proximoNumeroRoteador": "-", "interface": "-"}]


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
def configurarInterfacesEntrada(numeroRoteador):
	switcher = {
		0: NODE0_INTERFACES_ADD,
		1: NODE1_INTERFACES_ADD,
		2: NODE2_INTERFACES_ADD,
		3: NODE3_INTERFACES_ADD
	}

	interfaces = switcher.get(numeroRoteador, [])
	return(interfaces)

def configurarInterfacesSaida(numeroRoteador):
	switcher = {
		0: NODE0_INTERFACES_ADD_NEIGHBORHOOD,
		1: NODE1_INTERFACES_ADD_NEIGHBORHOOD,
		2: NODE2_INTERFACES_ADD_NEIGHBORHOOD,
		3: NODE3_INTERFACES_ADD_NEIGHBORHOOD
	}

	interfaces = switcher.get(numeroRoteador, [])
	return(interfaces)

# Configura o roteador
def configurarRoteador(numeroRoteador):
	interfacesEntrada = configurarInterfacesEntrada(numeroRoteador)
	interfacesSaida = configurarInterfacesSaida(numeroRoteador)
	tabelaInicial = inicializarTabelaRIP(numeroRoteador)
	return(interfacesEntrada, interfacesSaida, tabelaInicial)

#############################################################################
# Configuração de envio/recebimento mensagens com socket
#############################################################################

# Recebe mensagens via socket UDP
def receiver(interface):
	server_address = (interface, PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(server_address)
	data, address = sock.recvfrom(4096)

	jsonMessage = json.loads(data.decode('utf-8'))
	print(jsonMessage)

# Envia mensagens via socket UDP
def sender(interface, mensagem):
	server_address = (interface, PORT)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	data = json.dumps(mensagem)
    sent = sock.sendto(data.encode('utf-8'), server_address)

#############################################################################
# Exibir informações
#############################################################################

# Exibe registros
def exibirTabelaRIP(tabela):
	print("######################################################")
	print("# Nº Rotedor | Distancia | Prox Roteador | Interface #")
	print("######################################################")

	for registro in tabela:
		print('#      {}     | {} |       {}       |     {}     #'.format(
			registro["numeroRoteador"], str(registro["distancia"]).zfill(9),
			registro["proximoNumeroRoteador"], registro["interface"]))
	
	print("######################################################")

def exibirInterfaces(interfaces):
	print("\nEndereço das interfaces:")
	for i in range(len(interfaces))	:
		print("Interface {}: \"{}\"".format(i, interfaces[i]))
	print("")	


#############################################################################
# Programa principal
#############################################################################

registrosAlterados = []

# Recebe o número do roteador e configura-o
numeroRoteador = int(input("Digite o número do nó: "))
interfacesEntrada, interfacesSaida, tabelaRegistros = configurarRoteador(numeroRoteador)

if not interfacesEntrada and not interfacesSaida and not tabelaRegistros:
	exit("Não existe roteador: Digite um número entre 0 e 3\nNão foi possível construir tabela RIP")

# Exibe as interfaces e a tabela atual
exibirInterfaces(interfacesEntrada)	
exibirTabelaRIP(tabelaRegistros)

# Cria uma thread para receber mensagens em cada interface
for interface in interfacesEntrada:
	t = threading.Thread(target=receiver, args=(interface,))
	t.start()
