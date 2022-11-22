import threading
import socket

PORTA_CLIENTE = 1000

def receptor():
    endereco = ('localhost', 2000)
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(endereco)
    socket_servidor.listen()

    def conexao_operacoes(PORT, mensagem):
        socket_operacoes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_operacoes.connect(('127.0.0.1', PORT))
        mensagem = mensagem.encode('utf-8')
        socket_operacoes.sendall(mensagem)

    ultimo_saldo = 0
    saldo = 0
    contador = 0
    replicas = [3000, 4000, 5000, 6000]

    print("=/="*10)
    print("=/==/ Primaria - Ativa ==/==/=")
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
                for replica in replicas:
                    thread_credito = threading.Thread(target = conexao_operacoes, args=[replica, mensagem_dados.decode()])
                    thread_credito.start()

            elif(tipo_operacao == "400"):
                print("Requisição de Débito.")
                saldo -= int(valor)
                for replica in replicas:
                    thread_debito = threading.Thread(target = conexao_operacoes, args=[replica, mensagem_dados.decode()])
                    thread_debito.start()

            elif(tipo_operacao == "600"):
                contador += 1
                if (contador == 4):
                    print("Cálculo (OK).")
                    ultimo_saldo = saldo
                    mensagem = id + "/600/" + str(saldo)
                    thread_sucesso = threading.Thread(target = conexao_operacoes, args=[PORTA_CLIENTE, mensagem])
                    thread_sucesso.start()
                    contador = 0
            elif(tipo_operacao == "700"):
                contador += 1
                if (contador == 4):
                    print("Não Houve Acordo (NHA).")
                    mensagem = id + "/700/" + str(ultimo_saldo)
                    thread_erro = threading.Thread(target = conexao_operacoes, args=[PORTA_CLIENTE, mensagem])
                    thread_erro.start()
                    contador = 0

        conexao.close()


def main():
    thread_servidor = threading.Thread(target=receptor)
    thread_servidor.start()

main()

