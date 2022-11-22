import threading
import socket

def receptor():
    endereco = ('localhost', 1000)
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(endereco)
    socket_servidor.listen()
    while True:
        conexao, port = socket_servidor.accept()
        while True:
            mensagem_dados = conexao.recv(1024)
            dados_formatados = mensagem_dados.decode().split("/")

            operacao = {
                "id": dados_formatados[0],
                "tipo_operacao": dados_formatados[1],
                "valor": dados_formatados[2],
            }

            id = operacao.get("id")
            tipo_operacao = operacao.get("tipo_operacao")
            valor = operacao.get("valor")

            if (tipo_operacao == "600"):
                print(f"\nMensagem Recebida. ID: {id}. Saldo Atual: {valor}")
                break
            elif (tipo_operacao == "700"):
                print("Aconteceu algum erro!")
                print(f"\nMensagem Recebida. ID: {id}. Saldo Atual: {valor}")
                break

        conexao.close()

def main():

    thread_servidor = threading.Thread(target=receptor)
    thread_servidor.start()
    id = 1

    while True:

        opcao = int(input("=/=/=/=/=/=/=/=/=/\n\nEscolha uma opção:\n\n1) Crédito.\n2) Débito.\n\n=/=/=/=/=/=/=/=/=/\n"))
        valor = int(input("Digite algum valor:"))

        if(opcao == 1):
            mensagem = str(id) + "/300/" + str(valor)
            socket_credito = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_credito.connect(('127.0.0.1', 2000))
            mensagem = mensagem.encode('utf-8')
            thread_credito = threading.Thread(target = socket_credito.sendall(mensagem), args=[])
            thread_credito.start()
            print(f"\nMensagem Enviada. ID {str(id)}. Valor Enviado: {int(valor)}\n")
            id += 1
            socket_credito.close()

        elif(opcao == 2):
            mensagem = str(id) + "/400/" + str(valor)
            socket_debito = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_debito.connect(('127.0.0.1', 2000))
            mensagem = mensagem.encode('utf-8')
            thread_debito = threading.Thread(target = socket_debito.sendall(mensagem), args=[])
            thread_debito.start()
            id += 1
            socket_debito.close()

        else:
            break


main()
