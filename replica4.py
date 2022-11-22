import threading
import socket

PORTA_PRIMARIA = 2000

def receptor():
    endereco = ('localhost', 6000)
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
    replicas = [3000, 4000, 5000]
    lista_valores = []

    print("=/="*10)
    print("=/==/ Replica 4 - Ativa =/==/=")
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

            if(int(id) <= 6):
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
                    if (len(lista_valores) == 3):
                        for valor_lista in lista_valores:
                            if (valor_lista == saldo):
                                contador += 1
                        if (contador == 3):
                            mensagem = str(id) + "/600/" + str(saldo)
                            print("Comparação Realizada com Sucesso")
                            thread_sucesso = threading.Thread(target = conexao_operacoes, args=[PORTA_PRIMARIA, mensagem])
                            thread_sucesso.start()
                            lista_valores.clear()
                            contador = 0
                        else:
                            mensagem = str(id) + "/700/" + str(saldo)
                            print("Ops! Aconteceu algum erro.")
                            thread_erro = threading.Thread(target = conexao_operacoes, args=[PORTA_PRIMARIA, mensagem])
                            thread_erro.start()
                            lista_valores.clear()
                            contador = 0

            else:
                if(tipo_operacao == "300"):
                    print("Crédito Invertido.")
                    saldo -= int(valor)
                    mensagem = id + "/500/" + str(saldo)
                    for replica in replicas:
                        thread_credito = threading.Thread(target = conexao_operacoes, args=[replica, mensagem])
                        thread_credito.start()

                elif(tipo_operacao == "400"):
                    print("Débito Invertido.")
                    saldo += int(valor)
                    mensagem = id + "/500/" + str(saldo)
                    for replica in replicas:
                        thread_debito = threading.Thread(target = conexao_operacoes, args=[replica, mensagem])
                        thread_debito.start()

                elif(tipo_operacao == "500"):
                    lista_valores.append(int(valor))
                    if (len(lista_valores) == 3):
                        for valor_lista in lista_valores:
                            if (valor_lista == saldo):
                                contador += 1
                        if (contador == 3):
                            mensagem = str(id) + "/600/" + str(saldo)
                            print("Comparação Realizada com Sucesso")
                            thread_sucesso = threading.Thread(target = conexao_operacoes, args=[PORTA_PRIMARIA, mensagem])
                            thread_sucesso.start()
                            lista_valores.clear()
                            contador = 0
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
