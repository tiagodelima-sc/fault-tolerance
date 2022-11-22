import threading
import socket

PORTA_PRIMARIA = 2000

def receptor():
    endereco = ('localhost', 3000)
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(endereco)
    socket_servidor.listen()

    def conexao_operacoes(PORT, mensagem):
        socket_operacoes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_operacoes.connect(('127.0.0.1', PORT))
        mensagem = mensagem.encode('utf-8')
        socket_operacoes.sendall(mensagem)

    saldo = 0
    contador = 0
    replicas = [4000, 5000, 6000]
    lista_valores = []

    print("=/="*10)
    print("=/==/ Replica 1 - Ativa =/==/=")
    print("=/="*10)
    print("\n")

    while True:
        conexao, port = socket_servidor.accept()
        while True:
            mensagem_dados = conexao.recv(1024)
            dados_formatados = mensagem_dados.decode().split("/")

            if len(mensagem_dados) == 0:
                #print("Aguardando Mensagem")
                break

            operacao = {
                "id": dados_formatados[0],
                "tipo_operacao": dados_formatados[1],
                "valor": dados_formatados[2],
            }

            id = operacao.get("id")
            tipo_operacao = operacao.get("tipo_operacao")
            valor = operacao.get("valor")

            if(tipo_operacao == "300"):
                print("Requisição de Crédito.")
                saldo += int(valor)
                mensagem = id + "/500/" + str(saldo)
                for replica in replicas:
                    thread_credito = threading.Thread(target = conexao_operacoes, args=[replica, mensagem])
                    thread_credito.start()

            elif(tipo_operacao == "400"):
                print("Requisição de Débito.")
                saldo -= int(valor)
                mensagem = id + "/500/" + str(saldo)
                for replica in replicas:
                    thread_debito = threading.Thread(target = conexao_operacoes, args=[replica, mensagem])
                    thread_debito.start()

            elif(tipo_operacao == "500"):
                lista_valores.append(int(valor))
                # Verifica se o tamanho da lista é igual a 3, porque ele recebe informações de 3 replicas
                if (len(lista_valores) == 3):
                    #Para cada valor na minha lista de valores
                    for valor_lista in lista_valores:
                        # Faço uma verificacao se o valor da lista é igual o saldo, se for, icremento o contador
                        if (valor_lista == saldo):
                            contador += 1
                    if (contador == 3):
                        # Enviando Mensagem de ok para a primaria, contendo o id recebido do cliente, para saber que está ok
                        mensagem = str(id) + "/600/" + str(saldo)
                        print("Comparação Realizada com Sucesso")
                        thread_sucesso = threading.Thread(target = conexao_operacoes, args=[PORTA_PRIMARIA, mensagem])
                        thread_sucesso.start()
                        lista_valores.clear()
                        contador = 0
                        #Apartir da setima requisicao, o ultimo valor vai ser alterado e vai cair no meu else
                    else:
                        mensagem = str(id) + "/700/" + str(saldo)
                        print("Ops! Aconteceu algum erro na comparação.")
                        thread_erro = threading.Thread(target = conexao_operacoes, args=[PORTA_PRIMARIA, mensagem])
                        thread_erro.start()
                        lista_valores.clear()
                        contador = 0

        conexao.close()


def main():

    thread_servidor = threading.Thread(target=receptor)
    thread_servidor.start()


main()
