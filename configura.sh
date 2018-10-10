# Cria as interfaces necessárias

if [ $# -ne '1' ]; then
	echo "Uso: \$configura < interface >"
	exit
fi

# Endereco de cada uma das interfaces
ENDERECOS[0]='192.168.1.100' 
ENDERECOS[1]='192.168.2.100'
ENDERECOS[2]='192.168.3.100'
ENDERECOS[3]='192.168.1.200'
ENDERECOS[4]='192.168.5.100'
ENDERECOS[5]='192.168.3.200'
ENDERECOS[6]='192.168.4.100'
ENDERECOS[7]='192.168.5.200'  
ENDERECOS[8]='192.168.2.200'
ENDERECOS[9]='192.168.4.200'

# Modo automático de obter interfaces (nem sempre funciona) 
# INTERFACES=$(ip link show | cut -d " " -f 2 | cut -d ":" -f 1 | cut -d$'\n' -f 3 )

for i in 0 1 2 3 4 5 6 7 8 9;
do
	sudo ifconfig $1:$i ${ENDERECOS[$i]}
done;
