# Código do Programa de Controle da Interface de Envio dos Comandos

import serial
import time
import os
from tkinter import filedialog

global arquivo
global err
global loop
global loopstart
loop = 0
loopstart = 0
portas = []
idem = []
echo = []
canais = {}
dups = {}
port = 0
baud = 9600
last_vars = [[0, 0, 0], ['', '', '']] #[[Ports],[Temp, Pump, Agit]]
parser_triggers =  ['TAG_HEAT', 'TAG_PUMP', 'TAG_AGT']

def reset():
    global err
    portas.clear()
    idem.clear()
    echo.clear()
    canais.clear()
    dups.clear()
    loop = 0
    loopstart = 0
    err = 0
    port = 0
    baud = 9600

def abrir_canais(l):
    print(f'\n[ABRINDO CANAL]{[l]}')
    com = canais[l]
    if l not in dups.keys():
        try:
            if serial.Serial(com, baud).isOpen():
                serial.Serial(com, baud).close()
        except:
            print("[PORTA ABERTA POR OUTRO PRGRAMA]")
            canais[l] = 'OCUPADO'
            return

        while True:
            global err
            canais[l] = serial.Serial(com, baud)
            time.sleep(1)
            if canais[l].readline():
                err = 0
                while canais[l].inWaiting():
                    print(canais[l].readline().decode('utf-8').strip())
                return
            elif err > 100:
                print("\n\n[0][ERRO NA CONEXAO]")
                err = 0
            else:
                err += 1

def reopen_channel(port):
    for k in canais.keys():
        if canais[k] == port:
            canais[k].close()
            abrir_canais(k)

def fechar_canais():
    for l in canais.keys():
        try:
            print(f'\n-->A porta {l} foi fechada')
            canais[l].close()
        except AttributeError:
            canais[l] = ''

def process_linha(portas):
    global loop
    global loopstart
    if portas[0] in canais.keys() or portas[0] in dups.keys():
        if portas[0] in canais.keys() and canais[portas[0]] != 'OCUPADO':
            printport(portas, 1)
        elif portas[0] in dups.keys() and canais[dups[portas[0]]] != 'OCUPADO':
            printport(portas, 2)
        else:
            printport(portas, 3)
            return(print("[COMANDO ANULADO]\n[PORTA ABERTA POR OUTRO PRGRAMA]"))
    elif portas[0] in ['LOOP', 'loop']:
        if int(loop) < int(portas[2]):
            print(f"\n[LOOP COUNT] [{loop}]")
            loop += 1
            arquivo.seek(loopstart)
            next(arquivo)
        else:
            print("\n[LOOP ENCERRADO]")
    elif portas[0] == 'LOOPSTART':
        line = arquivo.readline()
        while line:
            arquivo.tell()  # returns the location of the next line
            loopstart =  arquivo.readline()
    else:
        return(print("\n[COMANDO INVALIDO]"))
    print(loopstart)

def env_com(port, msg):
    global err
    port.reset_input_buffer()
    port.write(msg.encode('utf-8'))
    time.sleep(1)
    err = [0,0]
    while True:
        time.sleep(0.5)
        if port.isOpen():
            answer = port.readline().decode('utf-8')
            answer1 = answer.split('\n')[0]
            answer2 = answer.split('\r')[0]
            print(f"{answer1 if len(answer1) > 0 else answer2 }")
            for i in idem:
                if i in answer:
                    port.reset_input_buffer()
                    time.sleep(0.2)
                    err = [0,0]
                    return
                elif answer.split(':')[0] not in echo:
                    err[1] += 1
        elif err[0] > 50:
            print("\n\n[1][ERRO NA CONEXAO]")
            port.reset_input_buffer()
            reopen_channel()
            last_parser(port, msg, True)
            port.write(msg.encode('utf-8'))
            err[0] = 0
        elif err[1] > 50:
            print("\n\n[1][ERRO NO PARSER]")
            port.reset_input_buffer()
            port.write(msg.encode('utf-8'))
            err[1] = 0
        else:
            time.sleep(0.5)
            err[0] += 1

def last_parser(port, msg, reset = False):
    for i in range(len(parser_triggers)):
        if parser_triggers[i] in msg and not reset:
            last_vars[0][i] = port
            last_vars[1][i] = msg
            return
        if reset:
            env_com(last_vars[0][i], last_vars[1][i])

def printport(portas, i):
    if i == 1:
        port = canais[portas[0]]
        portd = portas[0]
    elif i == 2:
        portd = dups[portas[0]] + '/' + portas[0]
        port = canais[dups[portas[0]]]
    else:
        portd = portas[0]
    portas.pop(0)
    msg = ''
    for l in portas:
        msg += l.upper() + ' '
    msg += '\n'
    print(f'\n<{portd}>{msg}', end='')
    if i != 3:
        last_parser(port, msg)
        env_com(port, msg)
def combreak():
    try:
        input("\n\t[Pressione Enter Para continuar]")
    except KeyboardInterrupt:
        print("\n\n[FIM DO PROGRAMA]")
    finally:
        os.system('cls')

while True:
    reset()
    while True:
        arq = filedialog.askopenfilename(filetypes=[("Arquivos GCODE", "*.gcode")])
        if arq:
            break
        else:
            combreak()

    # while True:
    #     arq = input("-->Insira o nome do arquivo: ")
    #     os.system('cls')
    #     if arq.isalnum() or ('\\'not in arq and '/'not in arq and ':'not in arq):
    #         arq += '.gcode'
    #         break

    try:
        with open(arq, 'r') as arquivo:
            for linha in arquivo:
                if len(linha) > 0 and linha != '\n':
                    if 'CFG' in linha.split()[0].upper():
                        portas = linha.split()
                        portas.pop(0)
                        baudttg = True
                        # Modelo de arquivo:
                        # CFG BAUD9600 P5 COM4/IDX/ramps COM7/IDX/arduino IDEM:OK
                        for x in portas:
                            if x.startswith('BAUD') and x.replace("BAUD", "").isnumeric():
                                baud = int(x.replace("BAUD", ""))
                                baudttg = False
                            elif baudttg:
                                while True:
                                    baud = input("-->Insira a baud rate: ")
                                    os.system('cls')
                                    if baud.isnumeric():
                                        baudttg = False
                                        break
                            elif x.startswith('P') and x.replace("P", "").isnumeric():
                                port = int(x.replace("P", ""))
                            elif x.startswith('IDEM') and ':' in x:
                                idem = x.split(':')
                                idem = list(filter(None, idem))
                                idem.pop(0)
                            elif x.startswith('ECHO') and ':' in x:
                                echo = x.split(':')
                                echo = list(filter(None, echo))
                                echo.pop(0)
                            elif x.startswith('COM') and '/IDX/' in x and x.split('/IDX/')[1] not in canais.keys():
                                if x.split('/IDX/')[0] in canais.values():
                                    for l, k in canais.items():
                                        if k == x.split('/IDX/')[0]:
                                            dups[x.split('/IDX/')[1]] = l
                                else:
                                    canais[x.split('/IDX/')[1]] = x.split('/IDX/')[0]
                        if port > len(canais):
                            for p in range(port - len(canais)):
                                while True:
                                    total = input(f"-->Insira o número da {p + len(canais) + 1}ª porta: ")
                                    iden = input(f"-->Insira o identificador da {p + len(canais) + 1}ª porta: ")
                                    os.system('cls')
                                    if total.isnumeric():
                                        canais[iden] = 'COM' + total
                                        break
                        for l in canais.items():
                            print(l)

                        for l in canais.keys():
                            abrir_canais(l)

                        print('\n-->Baud rate: ', baud)
                        print('-->Quantidade de portas: ', port)
                        print('-->As portas selecionadas são: \n')
                        for l in canais.items():
                            print(l)
                        if len(dups) > 0:
                            print('\n-->As portas duplicadas são:\n')
                            for l in dups.keys():
                                print(f'[{l}] equivale a [{dups[l]}]')
                        print('\n-->Os identificadores são: \n', idem)
                        combreak()
                    else:
                        process_linha(linha.split())
            fechar_canais()
            print("\n\n[FIM DO CODIGO]")

    except FileNotFoundError:
        print("\n\n[ARQUIVO GCODE NAO ENCONTRADO]")

    except KeyboardInterrupt:
        fechar_canais()
        print("\n\n[PROGRAMA INTERROMPIDO PELO USUARIO]")

    except AttributeError:
        print("\n\n[ERRO NAS PORTAS]")

    except Exception as err:
        print(f"\n\n[ERRO] [{err=}]\nLog: {type(err)=}")

    finally:
        if not FileNotFoundError:
            if arquivo:
                arquivo.close()
    combreak()
