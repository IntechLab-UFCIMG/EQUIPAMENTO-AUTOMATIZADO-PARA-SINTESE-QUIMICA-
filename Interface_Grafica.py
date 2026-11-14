#Código da Interface Gráfica (Python 3) 

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
# from serial.tools import list_ports
import serial.tools.list_ports # type: ignore
# import json as archlogger
import os
global win_switch, win_pop

class InterfaceGrafica:
    def __init__(self, main):
        self.root = main
        self.root.title("Criar_metodologia")
        self.root.resizable(0, 0)

        # Criando as variaveis
        self.last = {}
        self.lastvalv = {}
        self.valvp = {}
        self.vert = tk.IntVar()
        self.autoserv = tk.BooleanVar()
        self.autoiniv = tk.BooleanVar()
        self.autox = tk.BooleanVar()
        self.dump = tk.BooleanVar()
        self.dumpallv = tk.IntVar()
        self.checkboxes = []
        self.check1 = tk.DoubleVar()
        self.agit = tk.DoubleVar()
        self.temp = tk.DoubleVar()
        self.feedX = tk.DoubleVar()
        self.feedA = tk.DoubleVar()
        self.feedB = tk.DoubleVar()
        self.feedY = tk.DoubleVar()
        self.feedZ = tk.DoubleVar()
        self.feedV = tk.DoubleVar()
        self.feedautop = tk.DoubleVar()
        self.feedP = tk.DoubleVar()
        self.feedPIP = tk.DoubleVar()
        self.accel_val = []
        self.val_via = tk.DoubleVar()
        self.minagit = tk.IntVar()
        self.redftggl = tk.IntVar()
        self.accelttg = tk.IntVar()
        self.valvttg = tk.IntVar()
        self.abspol = True

        # Criando as variaveis de parametros
        self.dvolp = tk.DoubleVar()
        self.state_cap = []
        self.dump_vol = {}
        self.mxvol = {}
        self.minvol = {}
        self.curva = {}
        self.cfg = []

        # Criando as variaveis de track
        self.txt_back = []
        self.log_back = []
        self.last_amostr = []
        self.lastdelay = []
        self.lastmov = []
        self.lastmix = []
        self.logcount = tk.IntVar()

        # Criar os botões principais
        self.botao1 = tk.Button(
            main, text="Valvula 1", command=lambda: self.clicou_val('X', self.cbox1.get(), True))
        self.botao2 = tk.Button(
            main, text="Valvula 2", command=lambda: self.clicou_val('A', self.cbox2.get(), True))
        self.botao3 = tk.Button(
            main, text="Valvula 3", command=lambda: self.clicou_val('B', self.cbox3.get(), True))
        self.botao4 = tk.Button(
            main, text="Valvula 4", command=lambda: self.clicou_val('Y', self.cbox4.get(), True))
        self.botao5 = tk.Button(
            main, text="Valvula 5", command=lambda: self.clicou_val('Z', self.cbox5.get(), True))
        self.botao6 = tk.Button(
            main, text="Seringa 1", command=lambda: self.clicou_ser('X', self.cbox1.get(), self.entry6.get(), 1))
        self.botao7 = tk.Button(
            main, text="Seringa 2", command=lambda: self.clicou_ser('A', self.cbox2.get(), self.entry7.get(), 1))
        self.botao8 = tk.Button(
            main, text="Seringa 3", command=lambda: self.clicou_ser('B', self.cbox3.get(), self.entry8.get(), 1))
        self.botao9 = tk.Button(
            main, text="Seringa 4", command=lambda: self.clicou_ser('Y', self.cbox4.get(), self.entry9.get(), 1))
        self.botao10 = tk.Button(
            main, text="Seringa 5", command=lambda: self.clicou_ser('Z', self.cbox5.get(), self.entry10.get(), 1))
        self.botao11 = tk.Button(main, text="Agitação", width=9, command=lambda: self.clicou_agitacao())
        self.botao12 = tk.Button(main, text="Temperatura", width=9, command=lambda: self.clicou_aquecimento())
        self.botao13 = tk.Button(main, text="Esperar", width=9, command=lambda: self.comm_wait())
        self.botao14 = tk.Button(main, text="Posicionar", command=lambda: self.controle_pos())

        # Criando as checkbox
        self.checkboxes = [tk.Checkbutton(main, variable=self.check1, onvalue=i, foreground="red") for i in range(25)]

        # Adicionar Entradas abaixo dos botões 6 a 10
        self.label_entry = [tk.Label(main, text="Volume [mL]     Vazão [mL/s]") for i in range(5)]
        self.entry6 = tk.Entry(main, width=10)
        self.spinfeed1 = tk.Spinbox(main, from_=0.005, to=10, increment=0.005, textvariable=self.feedX)
        self.spinfeed1.config(validate="all", repeatdelay=200, repeatinterval=2, width=6)
        self.spinfeed1.config(validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.spinfeed1.bind('<FocusOut>', lambda event: self.reset_spinbox(self.spinfeed1, self.feedX))
        self.spinfeed1.bind('<Return>', lambda event: self.reset_spinbox(self.spinfeed1, self.feedX))
        self.spinfeed1.bind('<Tab>', lambda event: self.reset_spinbox(self.spinfeed1, self.feedX))

        self.entry7 = tk.Entry(main, width=10)
        self.spinfeed2 = tk.Spinbox(main, from_=0.005, to=10, increment=0.005, textvariable=self.feedA)
        self.spinfeed2.config(validate="all", repeatdelay=200, repeatinterval=2, width=6)
        self.spinfeed2.config(validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.spinfeed2.bind('<FocusOut>', lambda event: self.reset_spinbox(self.spinfeed2, self.feedA))
        self.spinfeed2.bind('<Return>', lambda event: self.reset_spinbox(self.spinfeed2, self.feedA))
        self.spinfeed2.bind('<Tab>', lambda event: self.reset_spinbox(self.spinfeed2, self.feedA))

        self.entry8 = tk.Entry(main, width=10)
        self.spinfeed3 = tk.Spinbox(main, from_=0.005, to=10, increment=0.005, textvariable=self.feedB)
        self.spinfeed3.config(validate="all", repeatdelay=200, repeatinterval=2, width=6)
        self.spinfeed3.config(validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.spinfeed3.bind('<FocusOut>', lambda event: self.reset_spinbox(self.spinfeed3, self.feedB))
        self.spinfeed3.bind('<Return>', lambda event: self.reset_spinbox(self.spinfeed3, self.feedB))
        self.spinfeed3.bind('<Tab>', lambda event: self.reset_spinbox(self.spinfeed3, self.feedB))

        self.entry9 = tk.Entry(main, width=10)
        self.spinfeed4 = tk.Spinbox(main, from_=0.005, to=10, increment=0.005, textvariable=self.feedY)
        self.spinfeed4.config(validate="all", repeatdelay=200, repeatinterval=2, width=6)
        self.spinfeed4.config(validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.spinfeed4.bind('<FocusOut>', lambda event: self.reset_spinbox(self.spinfeed4, self.feedY))
        self.spinfeed4.bind('<Return>', lambda event: self.reset_spinbox(self.spinfeed4, self.feedY))
        self.spinfeed4.bind('<Tab>', lambda event: self.reset_spinbox(self.spinfeed4, self.feedY))

        self.entry10 = tk.Entry(main, width=10)
        self.spinfeed5 = tk.Spinbox(main, from_=0.005, to=10, increment=0.005, textvariable=self.feedZ)
        self.spinfeed5.config(validate="all", repeatdelay=200, repeatinterval=2, width=6)
        self.spinfeed5.config(validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.spinfeed5.bind('<FocusOut>', lambda event: self.reset_spinbox(self.spinfeed5, self.feedZ))
        self.spinfeed5.bind('<Return>', lambda event: self.reset_spinbox(self.spinfeed5, self.feedZ))
        self.spinfeed5.bind('<Tab>', lambda event: self.reset_spinbox(self.spinfeed5, self.feedZ))

        # Adicionnar botoes pipetador
        self.label_entry11 = tk.Label(main, text="=========[Atenção]=======", foreground="red")
        self.label_entry12 = tk.Label(main, text="""\tX----------0
            /  (2)  (1)  /
        /  (4)  (3)  /
    0----------Y
        [Sentido do Amostrador]""", foreground="green")
        self.label_entry13 = tk.Label(main, text="Posição da bandeja:")
        self.label_entry14 = tk.Label(main, text="Feedrate:")
        self.label_entry10 = tk.Label(main, text="mm/min")
        self.entry14 = tk.Spinbox(main, from_=1000, to=10000, increment=1, textvariable=self.feedPIP, state="readonly")
        self.entry14.config(repeatdelay=200, repeatinterval=2, width=5)

        # Botões da bandeja
        self.label_combox6 = tk.Label(main, text="Bandeja:")
        self.cbox6 = ttk.Combobox(main, state="readonly", values=["Nenhum", "\t A [2X3]", "\t B [2X3]", "\t C [2X3]",
                                                                  "\t A1 [4X6]", "\t B1 [4X6]", "\t C1 [4X6]",
                                                                  "\t A2 [3X4]", "\t B2 [3X4]", "\t C2 [3X4]"])
        self.cbox6.bind('<Return>', lambda event: self.alterar_bandeja(self.cbox6.get()))
        self.cbox6.bind('<<ComboboxSelected>>', lambda event: self.alterar_bandeja(self.cbox6.get()))
        self.alterar_bandeja('Nenhum')
        self.cbox7 = ttk.Combobox(main, state="readonly", width=9, values=["Abaixar", "Levantar"])
        self.cbox7.bind('<Return>', lambda event: self.alterar_pip(self.cbox7.get()))
        self.cbox7.bind('<<ComboboxSelected>>', lambda event: self.alterar_pip(self.cbox7.get()))
        self.spin_needle = tk.Spinbox(main, from_=0, to=100, increment=0.5, width=4)

        # Adicionar entry utilitaria
        self.label_entry15 = tk.Label(main, text="%")  # Agitacao
        self.entry11 = tk.Spinbox(main, from_=0, to=100, increment=1, textvariable=self.agit)
        self.entry11.config(repeatdelay=200, repeatinterval=24, relief="groove", width=5)
        self.entry11.config(validate="all", validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.entry11.bind('<FocusOut>', lambda event: self.reset_spinbox(self.entry11, self.agit))
        self.entry11.bind('<Return>', lambda event: self.reset_spinbox(self.entry11, self.agit))
        self.entry11.bind('<Tab>', lambda event: self.reset_spinbox(self.entry11, self.agit))

        self.label_entry16 = tk.Label(main, text="ºC")  # Aquecimento
        self.entry12 = tk.Spinbox(main, from_=0, to=100, increment=0.5, textvariable=self.temp)
        self.entry12.config(repeatdelay=200, repeatinterval=18, relief="groove", width=5)
        self.entry12.config(validate="all", validatecommand=(main.register(self.spinbox_validation), "%P", "%S", "%W"))
        self.entry12.bind('<FocusOut>', lambda event: self.reset_spinbox(self.entry12, self.temp))
        self.entry12.bind('<Return>', lambda event: self.reset_spinbox(self.entry12, self.temp))
        self.entry12.bind('<Tab>', lambda event: self.reset_spinbox(self.entry12, self.temp))

        self.wait_txt = tk.StringVar()  # Delay
        self.wait_txt1 = tk.StringVar()
        self.wait_txt2 = tk.StringVar()
        self.label_entry17 = tk.Label(main, text="Seg  Min Hor")
        self.label_entry18 = tk.Label(main, text="     :       :     ")
        self.entryseg = tk.Entry(main, textvariable=self.wait_txt, width=2)
        self.entrymin = tk.Entry(main, textvariable=self.wait_txt1, width=2)
        self.entryhor = tk.Entry(main, textvariable=self.wait_txt2, width=2)
        self.autoservo = tk.Checkbutton(main, variable=self.autoserv, onvalue=True, text="Servos Automaticos")
        self.autopump = tk.Checkbutton(
            main, variable=self.autox, onvalue=True, text="Auto Pump [Seringa 1]")

        # Adicionar Combobox abaixo dos botões 1 a 5
        self.cbox1 = ttk.Combobox(main, state="readonly", values=["Encher", "Manifold", "Ejetar"])
        self.cbox2 = ttk.Combobox(main, state="readonly", values=["Encher", "Manifold", "Ejetar"])
        self.cbox3 = ttk.Combobox(main, state="readonly", values=["Encher", "Manifold", "Ejetar"])
        self.cbox4 = ttk.Combobox(main, state="readonly", values=["Encher", "Manifold", "Ejetar"])
        self.cbox5 = ttk.Combobox(main, state="readonly", values=["Encher", "Manifold", "Ejetar"])

        # Adicionar botoes de roteamento
        self.chnel = {1: 'Bandeja', 2: 'Reator'}
        self.chk_band = tk.Checkbutton(
            main, variable=self.vert, text=self.chnel[1], onvalue=0, command=lambda: self.alterar_via())
        self.chk_reat = tk.Checkbutton(
            main, variable=self.vert, text=self.chnel[2], onvalue=1, command=lambda: self.alterar_via())
        self.bot_reat = tk.Button(main, text="Drenar", width=7, command=lambda: self.controle_pump(self.entry15.get(), 0))
        self.label_entry19 = tk.Label(main, text="mL")
        self.entry15 = tk.Entry(main, width=7)

        # Adicionar a caixa de texto com barra de rolagem
        self.caixa_texto = scrolledtext.ScrolledText(main, wrap=tk.WORD, width=100, height=25, bg='black')
        self.caixa_texto.config(foreground="white", undo=True, maxundo=-1)

        # Adicionar console
        self.console = scrolledtext.ScrolledText(main, wrap=tk.WORD, width=35, height=35, bg='black', state="disabled")
        self.console.tag_config('g', foreground="green")
        self.console.tag_config('r', foreground="red")

        # Adicionar botoes auxiliares
        self.botao_gravar = tk.Button(main, text="Gravar Texto", command=self.gravar_texto)
        self.botao_calibr = tk.Button(main, text="Calibrar sistema", command=lambda: janelaspop('cal'))
        self.botao_serial = tk.Button(main, text="Comunicador Serial", command=lambda: janelaspop('ser'))
        self.botao_cfg = tk.Button(main, text="Configurar", command=lambda: janelaspop('conf'))
        self.botao_back = tk.Button(main, text="Desfazer", command=lambda: self.desfazer())

        # Adicionar botoes reset
        self.sr_ex = {'[Todos]': 'all', 'Seringa 1': 'X', 'Seringa 2': 'A', 'Seringa 3': 'B', 'Seringa 4': 'Y',
                      'Seringa 5': 'Z', 'Pipetador': 'pip', 'Bomba': 'bmb', 'Valvulas': 'valv'}
        self.bot_set = tk.Button(
            main, text="Inicializar", command=lambda: self.ser_ini(self.sr_ex[self.cbox8.get()], 2))
        self.cbox8 = ttk.Combobox(main, state="readonly", width=9, values=list(self.sr_ex.keys()))
        self.autoini = tk.Checkbutton(main, variable=self.autoiniv, text="Auto inicializar", onvalue=True)
        self.dumpall = tk.Checkbutton(main, variable=self.dump, text="Multi descarte")
        self.dumpall.config(onvalue=True, offvalue=False, command=lambda: self.alterar_descarte())
        self.dumpalls = tk.Spinbox(main, from_=2, increment=1, to=100, state="readonly")
        self.dumpalls.config(repeatdelay=200, repeatinterval=24, width=4, textvariable=self.dumpallv)

        # Posicionar os elementos na grade
        self.posicionar_elementos()
        self.alterar_descarte()
        self.alterar_via()
        self.sys_config()
        self.start_setup()
        return

    def posicionar_elementos(self):
        # Posicionar os botões na parte superior
        self.botao1.grid(row=0, column=0)
        self.botao2.grid(row=0, column=1)
        self.botao3.grid(row=0, column=2)
        self.botao4.grid(row=0, column=3)
        self.botao5.grid(row=0, column=4)
        self.botao6.grid(row=3, column=0)
        self.botao7.grid(row=3, column=1)
        self.botao8.grid(row=3, column=2)
        self.botao9.grid(row=3, column=3)
        self.botao10.grid(row=3, column=4)
        # Utilitários
        self.botao12.grid(row=2, column=4, padx=25, rowspan=2, columnspan=11, pady=6, sticky='S')  # Aquecimento
        self.entry12.grid(row=2, column=4, padx=3, rowspan=2, columnspan=8, pady=9, sticky='SE')
        self.label_entry16.grid(row=2, column=9, rowspan=2, columnspan=4, padx=5, pady=10, sticky='SE')
        self.botao11.grid(row=2, column=4, padx=25, rowspan=4, columnspan=11, pady=25, sticky='S')  # Agitacao
        self.entry11.grid(row=2, column=4, rowspan=4, columnspan=8, padx=3, pady=28, sticky='SE')
        self.label_entry15.grid(row=2, column=9, rowspan=4, columnspan=4, padx=8, pady=28, sticky='SE')
        self.botao13.grid(row=3, column=4, rowspan=4, columnspan=11, pady=33, sticky='S')  # Espera
        self.entryseg.grid(row=3, column=8, rowspan=4, columnspan=4, pady=36, sticky='S')
        self.entrymin.grid(row=3, column=7, rowspan=4, columnspan=7, pady=36, sticky='S')
        self.entryhor.grid(row=3, column=9, rowspan=4, columnspan=4, pady=36, padx=4, sticky='SE')
        self.label_entry17.grid(row=3, column=7, rowspan=4, columnspan=7, padx=45, pady=18, sticky='SE')
        self.label_entry18.grid(row=3, column=7, rowspan=4, columnspan=7, pady=35, sticky='S')
        self.autopump.grid(row=0, column=4, rowspan=3, columnspan=9, padx=7, pady=19, sticky='NE')  # Autoservo
        self.autoservo.grid(row=0, column=4, rowspan=4, columnspan=9, padx=22, pady=0, sticky='NE')  # Autopump

        # Botoes pipetador
        self.label_combox6.grid(row=4, column=5, rowspan=5, columnspan=8)
        self.cbox6.grid(row=6, column=5, rowspan=3, columnspan=8)
        self.cbox7.grid(row=5, column=5, rowspan=7, columnspan=8, pady=18, sticky='S')
        self.label_entry14.grid(row=10, column=5, rowspan=4, columnspan=8, sticky='W')
        self.label_entry10.grid(row=10, column=5, rowspan=4, columnspan=8, sticky='E')
        self.entry14.grid(row=10, column=5, rowspan=4, columnspan=8, padx=54, sticky='W')
        self.botao14.grid(row=12, column=5, rowspan=3, columnspan=8, pady=15, sticky='N')

        # Botoes da parte de baixo
        self.chk_band.grid(row=12, column=5, rowspan=3, columnspan=8, padx=10, pady=54, sticky='NW')
        self.chk_reat.grid(row=12, column=5, rowspan=3, columnspan=8, padx=10, pady=54, sticky='NE')
        self.bot_set.grid(row=14, column=5, columnspan=8, padx=10, sticky='W')
        self.cbox8.grid(row=14, column=5, columnspan=8, padx=4, sticky='E')
        self.autoini.grid(row=14, rowspan=2, column=5, columnspan=8, pady=35, padx=6, sticky='SW')
        self.dumpall.grid(row=14, rowspan=2, column=5, columnspan=8, pady=16, padx=6, sticky='SW')

        # Posicionar Entradas abaixo dos botões 6 a 10
        for i in range(5): self.label_entry[i].grid(row=4, column=i)
        self.entry6.grid(row=5, column=0, padx=12, sticky='W')
        self.spinfeed1.grid(row=5, column=0, pady=5, padx=14, sticky='E')
        self.entry7.grid(row=5, column=1, padx=12, sticky='W')
        self.spinfeed2.grid(row=5, column=1, pady=5, padx=14, sticky='E')
        self.entry8.grid(row=5, column=2, padx=12, sticky='W')
        self.spinfeed3.grid(row=5, column=2, pady=5, padx=14, sticky='E')
        self.entry9.grid(row=5, column=3, padx=12, sticky='W')
        self.spinfeed4.grid(row=5, column=3, pady=5, padx=14, sticky='E')
        self.entry10.grid(row=5, column=4, padx=12, sticky='W')
        self.spinfeed5.grid(row=5, column=4, pady=5, padx=14, sticky='E')
        # Posicionar combox abaixo dos botões 1 a 5
        self.cbox1.grid(row=2, column=0, pady=10)
        self.cbox2.grid(row=2, column=1)
        self.cbox3.grid(row=2, column=2)
        self.cbox4.grid(row=2, column=3)
        self.cbox5.grid(row=2, column=4)

        # Posicionar a caixa de texto
        self.caixa_texto.grid(row=6, column=0, columnspan=5, rowspan=10, padx=10, pady=10)
        self.console.grid(row=0, column=13, columnspan=7, rowspan=18, padx=20)

        # Posicionar botoes da parte inferior
        self.botao_cfg.grid(row=18, column=0, sticky="W", padx=10)
        self.botao_gravar.grid(row=18, column=0, columnspan=5, pady=15)
        self.botao_calibr.grid(row=18, column=5, columnspan=8, pady=15)
        self.botao_serial.grid(row=18, column=13, columnspan=7, pady=15)
        self.botao_back.grid(row=18, column=4, sticky="E", padx=30)

    def alterar_bandeja(self, tray):
        self.check_clean()
        # Checkboxes do pipetador
        if tray == self.cbox6['values'][1] or tray == self.cbox6['values'][2] or tray == \
                self.cbox6['values'][3]:
            self.label_entry13.grid(row=4, column=5, rowspan=8, columnspan=8)
            self.checkboxes[1].grid(row=8, column=7, rowspan=2, columnspan=7)
            self.checkboxes[2].grid(row=8, column=5, rowspan=2, columnspan=8)
            self.checkboxes[3].grid(row=8, column=3, rowspan=2, columnspan=15)
            self.checkboxes[4].grid(row=8, column=7, rowspan=4, columnspan=7)
            self.checkboxes[5].grid(row=8, column=5, rowspan=4, columnspan=8)
            self.checkboxes[6].grid(row=8, column=3, rowspan=4, columnspan=15)
        elif tray == self.cbox6['values'][4] or tray == self.cbox6['values'][5] or tray == \
                self.cbox6['values'][6]:
            self.label_entry13.grid(row=4, column=5, rowspan=8, columnspan=8)
            for x in range(1, 7):
                self.checkboxes[x].grid(row=3, column=4, rowspan=11, columnspan=16 - x)
                self.checkboxes[x + 6].grid(row=6, column=4, rowspan=7, columnspan=16 - x)
                self.checkboxes[x + 12].grid(row=7, column=4, rowspan=6, columnspan=16 - x)
                self.checkboxes[x + 18].grid(row=8, column=4, rowspan=5, columnspan=16 - x)
        elif tray == self.cbox6['values'][7] or tray == self.cbox6['values'][8] or tray == \
                self.cbox6['values'][9]:
            self.label_entry13.grid(row=4, column=5, rowspan=8, columnspan=8)
            for x in range(1, 5):
                self.checkboxes[x].grid(row=5, column=4, rowspan=8, columnspan=15 - x)
                self.checkboxes[x + 4].grid(row=5, column=4, rowspan=9, columnspan=15 - x)
                self.checkboxes[x + 8].grid(row=4, column=4, rowspan=11, columnspan=15 - x)
        elif tray == self.cbox6['values'][0]:
            self.label_entry11.grid(row=5, column=4, rowspan=6, columnspan=12)
            self.label_entry12.grid(row=6, column=4, rowspan=7, columnspan=12)

    def alterar_pip(self, tray):
        if tray == self.cbox7['values'][1]:
            self.cbox7.grid(row=5, column=5, rowspan=7, columnspan=8, pady=18, sticky='S')
            self.spin_needle.grid_forget()
        elif tray == self.cbox7['values'][0]:
            self.cbox7.grid(row=5, column=5, rowspan=7, columnspan=8, padx=20, pady=18, sticky='SW')
            self.spin_needle.grid(row=5, column=5, rowspan=7, columnspan=8, padx=10, pady=18, sticky='SE')

    def check_clean(self):
        self.check1.set(0)
        self.label_entry11.grid_forget()
        self.label_entry12.grid_forget()
        self.label_entry13.grid_forget()
        for i in range(25): self.checkboxes[i].grid_forget()

    def alterar_via(self):
        if self.vert.get() == 1:  # Referrente ao reator
            pady_adjust = 44
            self.bot_reat.grid(row=12, column=5, rowspan=3, columnspan=8, padx=11, pady=52, sticky='SW')
            self.entry15.grid(row=12, column=5, rowspan=3, columnspan=8, padx=35, pady=56, sticky='SE')
            self.label_entry19.grid(row=12, column=5, rowspan=3, columnspan=8, padx=10, pady=56, sticky='SE')
        elif self.vert.get() == 0:  # Referrente a bandeja
            pady_adjust = 54
            self.bot_reat.grid_forget()
            self.entry15.grid_forget()
            self.label_entry19.grid_forget()
        else:
            self.vert.set(1)
            self.alterar_via()
            return
        self.chk_reat.grid(row=12, column=5, rowspan=3, columnspan=8, padx=10, pady=pady_adjust, sticky='NE')
        self.chk_band.grid(row=12, column=5, rowspan=3, columnspan=8, padx=10, pady=pady_adjust, sticky='NW')

    def alterar_descarte(self):
        if self.dump.get():
            self.dumpallv.set(2)
            self.dumpall['text'] = "Multi descarte:"
            self.dumpalls.grid(row=14, rowspan=2, column=5, columnspan=8, pady=18, padx=6, sticky='SE')
        else:
            self.dumpallv.set(1)
            self.dumpall['text'] = "Multi descarte"
            self.dumpalls.grid_forget()

    def spinbox_validation(self, P, S, W):
        entry = S.replace(".", "", 1)
        valid = entry == '' or entry.isdigit()
        # if valid:
        #     # get minimum and maximum values of the widget to be validated
        #     minval = int(self.root.nametowidget(W).config('from')[4])
        #     maxval = int(self.root.nametowidget(W).config('to')[4])
        #     # check if it's in range
        #     if int(P) not in range(minval, maxval): valid = False
        # if not valid: self.root.bell()
        return valid

    def reset_spinbox(self, spinbox, var):
        value = var.get()
        if value < spinbox['from']:
            var.set(spinbox['from'])
            return
        if value > spinbox['to']:
            var.set(spinbox['to'])
            return
        var.set(round(var.get(), 2))

    def desfazer(self):
        if len(self.txt_back) > 1:
            self.console.config(state="normal")
            last_txt = self.caixa_texto.get('1.0', self.txt_back[-1][0])
            last_log = self.console.get('1.0-1c', self.txt_back[-1][1])
            self.caixa_texto.replace('1.0', tk.END, last_txt)
            self.console.replace('1.0', tk.END, last_log, 'g')
            self.console.config(state="disabled")
            self.state_cap = self.txt_back[-1][2]
            self.last.update(self.txt_back[-1][3])
            self.lastmov = self.txt_back[-1][4]
            self.lastvalv = self.txt_back[-1][5]
            self.last_amostr = self.txt_back[-1][6]
            self.lastmix = self.txt_back[-1][7]
            self.minvol.update(self.txt_back[-1][8])
            self.mxvol.update(self.txt_back[-1][9])
            self.dump_vol.update(self.txt_back[-1][10])
            self.logcount.set(self.txt_back[-1][11])
            self.redftggl.set(self.txt_back[-1][12])
            self.feedautop.set(self.txt_back[-1][13])
            self.valvttg.set(self.txt_back[-1][14])
            self.txt_back.pop(-1)

    def log_updt(self):
        self.txt_back.append([self.caixa_texto.index('end-1c'), self.console.index('end-1c'), self.state_cap.copy(),
                              self.last.copy(), self.lastmov.copy(), self.lastvalv.copy(), self.last_amostr.copy(),
                              self.lastmix.copy(), self.minvol.copy(), self.mxvol.copy(), self.dump_vol.copy(),
                              self.logcount.get(), self.redftggl.get(), self.feedautop.get(), self.valvttg.get()])

    def sys_config(self):
        # Aplicar os parametricos iniciais
        self.cfg = [115200, 3, 'COM16', 'RAMPS', 'COM17', 'RAMPSERV', 'COM19', 'UNOPIP']  # Portas iniciais
        self.valvp = {
            'X': [-10, 0, 10, 2.5, 0.2], 'A': [-10, 0.1, 10, 2.68, -0.3],
            'B': [-10, 0, 10, 2.6, -0.3], 'Y': [-10, 0, 10, 2.5, -0.1],
            'Z': [-10, 0, 10, 2.5, 0]}  # Valor das posicoes das valvulas [90º, 0 , -90º, Pipetar, Ajuste fino]
        #Volume máximo [Seringas-> 5/10/20/60 mL || Pipetador-> 83.8mm altura max || Reatores-> 11/36/56/65 mL]
        self.mxvol = {'X': 60.0, 'A': 20.0, 'B': 20.0, 'Y': 5.0, 'Z': 5.0, 'P': 83.8, 'R': 36}  # Volume maximo
        self.minvol = {'X': 0, 'A': 0, 'B': 0, 'Y': 0, 'Z': 0, 'P': 0}  # Volume minimo
        self.curva = {'X': 2.02, 'A': 4.814, 'B': 4.79, 'Y': 11.628, 'Z': 11.614, 'P': 2.1408}  # Curva de calibração
        self.dump_vol = {'X': 0, 'A': 25, 'B': 25, 'Y': 60, 'Z': 60} # %Volume do reset de cada seringa
        self.state_cap = [80, 0.200]  # [%Volume do Auto-X, Volume de seg]
        self.reset_vpos = [2.5,-2.5, 10, -10]
        self.val_via.set(65)
        self.minagit.set(65)
        self.dvolp.set(1)

        # Aplicar as feedrates iniciais [mm/s]
        target_feed = 500  # Feedrate setada ao iniciar o programa
        self.feedX.set(round(target_feed/(self.curva['X']*60), 2))
        self.feedA.set(round(target_feed/(self.curva['A']*60), 2))
        self.feedB.set(round(target_feed/(self.curva['B']*60), 2))
        self.feedY.set(round(target_feed/(self.curva['Y']*60), 2))
        self.feedZ.set(round(target_feed/(self.curva['Z']*60), 2))
        self.feedautop.set(round(target_feed/(self.curva['X']*60), 2))
        self.feedV.set(800)
        self.feedPIP.set(4500)
        self.feedP.set(200)

        # Editar as acelerações [mm/s^2]
        self.accel_val = [100, 15, 100] #[Seringa, Valvula, Pipetador]

    def start_setup(self):
        # Aplicar valores de controle
        self.last = {'X': 'nan', 'A': 'nan', 'B': 'nan', 'Y': 'nan', 'Z': 'nan', 'all': 'nan', 'pip': 'nan', 'bmb': 'nan', 'valv': 'nan'}
        self.lastvalv = {'X': 0, 'A': 0, 'B': 0, 'Y': 0, 'Z': 0}
        self.last_amostr = [0, 0, 0, 0, '', '', 0]
        self.lastmov = ['', '', '']
        self.lastdelay = [0, 0, 0]
        self.lastmix = [0, 0]
        self.check1.set(0)

        # Resetar as posições Combox
        self.cbox1.current(1)
        self.cbox2.current(1)
        self.cbox3.current(1)
        self.cbox4.current(1)
        self.cbox5.current(1)
        self.cbox6.current(0)
        self.cbox7.current(0)
        self.cbox8.current(0)
        self.autoservo.select()
        self.autopump.select()
        self.chk_band.select()
        self.autoini.select()
        self.redftggl.set(1)
        self.valvttg.set(0)
        self.logcount.set(0)

        self.spin_needle.config(to=self.mxvol['P']-self.minvol['P'])
        self.caixa_texto.insert(tk.END, f"CFG BAUD{self.cfg[0]} P{self.cfg[1]} ")
        for i in range(0, self.cfg[1] * 2, 2):
            self.caixa_texto.insert(tk.END, f"{self.cfg[i + 2]}/IDX/{self.cfg[i + 3]} ")
        self.caixa_texto.insert(tk.END, "IDEM:ok:OK ECHO:echo\n")
        self.log_updt()

    def end_setup(self):
        #Ramps endcode Seringas
        final_gcode = f"{self.cfg[3]} M104 S0; Desliga o sistema de aquecimento  [TAG_HEAT]\n"
        final_gcode += f"{self.cfg[3]} M42 I P9 S0; Desliga sistema de agitacao  [TAG_AGT]\n"
        final_gcode += f"{self.cfg[3]} M82; Desabilita os motores de passo das Seringas\n"

        # Ramps endcode Valvulas
        final_gcode += self.reset_valv(1)
        final_gcode += f"{self.cfg[5]} M82; Desabilita os motores de passo das Válvulas\n"

        # Cnc shield endcode pipetador
        pip_feedrate = round(float(self.entry14.get()), 2)
        final_gcode += f"{self.cfg[7]} M3 S160; Levanta o pipetador por segurança\n"
        final_gcode += f"{self.cfg[7]} $H; Homing\n"
        final_gcode += f"{self.cfg[7]} G1 X1 Y1 F{pip_feedrate}; Posiciona o pipetador fora da Bandeja\n"

        return final_gcode

    def accel_set(self):
        if self.accelttg.get() == 0:
            accel_gcode = f"{self.cfg[3]} G91 ; Define todos os eixos como movimento relativo"
            accel_gcode += f"{self.cfg[3]} M204 P{self.accel_val[0]} T{self.accel_val[0]}; Define as aceleracoes das Seringas\n"
            accel_gcode += f"{self.cfg[5]} M204 P{self.accel_val[1]} T{self.accel_val[1]}; Define as aceleracoes das Valvulas\n"
            accel_gcode += f"{self.cfg[7]} $120={self.accel_val[2]}\n"
            accel_gcode += f"{self.cfg[7]} $121={self.accel_val[2]}\n"
            accel_gcode += f"{self.cfg[7]} $122={self.accel_val[2]}\n"
            self.caixa_texto.insert(tk.END, accel_gcode)
            self.accelttg.set(1)

    def func_vol(self, ser, idx):
        if idx == 1: return self.mxvol[ser] - self.minvol[ser]
        if idx == 2: return self.func_vol(ser, 1) * (self.dump_vol[ser] / 100)

    def ser_ini(self, seringa, tag):
        self.log_updt() if tag not in [0, 3, 4] else None
        if seringa in ['all', 'pip'] or self.redftggl.get() == 1:
            self.redftggl.set(1)
            self.accel_set()
            self.caixa_texto.insert(tk.END, self.misc_pip('', 1))
            self.caixa_texto.insert(tk.END, self.misc_pip('', 2))
            self.reset_valv(0)
            self.last_amostr = [0, 0, 0, 0, '', '', 0]
            self.pos_statusmisc(2)
        if seringa in ['all', 'bmb']:
            self.accel_set()
            self.descarte_pip(0)
            self.controle_pump(str(self.mxvol['R']), 1)
        if seringa in ['all', 'valv']:
            self.accel_set()
            self.reset_valv(0)
        if (self.last[seringa] == 'nan' and self.autoiniv.get()) or tag in [2, 3]:
            self.accel_set()
            for ser in list(self.sr_ex.values())[1:6]:
                if seringa == 'all' or ser == seringa:
                    self.dir_plot(self.vert.get(), tag)
                    cond = self.last['X'] == 'nan' and ser != 'X'
                    if cond and self.autox.get() and tag != 0: self.ser_ini('X', 3)
                    self.descarte_pip(0)
                    self.ser_zero(ser)
                    for rep in range(int(self.dumpallv.get())):
                        self.clicou_ser(ser, 'Encher', str(self.func_vol(ser, 2)), 4)
                        self.clicou_ser(ser, 'Ejetar', str(self.func_vol(ser, 2)), 4)
                    self.clicou_ser(ser, 'Encher', str(self.minvol[ser]), 0)
                    self.caixa_texto.insert(tk.END, f"{self.cfg[3]} G92 {ser[0]}0; Redefine o volume morto\n")
                    self.txt_back[-1][2] = self.txt_back[0][2]
                    self.txt_back[-1][3] = self.txt_back[0][3]
                    self.last[ser] = 0.0
                    self.vol_updt(f"Reset-{ser}", 0.0)
                    self.autox_comm(ser, tag)
                    self.descarte_pip(1) if tag != 3 else None
        elif self.last[seringa] == 'nan':
            self.last[seringa] = 0

    def ser_zero(self, seringa):
        if self.lastmov[0] != 'Encher' or self.lastmov[1] != seringa:
            self.clicou_val(seringa, 'Encher', False)
        self.caixa_texto.insert(tk.END, f"{self.cfg[3]} G28 {seringa}; Reset seringa {seringa}\n")
        self.last[seringa] = 0.0

    def clicou_val(self, seringa, valor_combox, tag1):
        self.log_updt() if tag1 else None
        self.accel_set()
        self.reset_valv(0)
        if valor_combox is not None:
            self.caixa_texto.insert(tk.END, self.interpreta_valvula(seringa, valor_combox))
            self.caixa_texto.insert(tk.END, f"{self.cfg[5]} M400; Espera a finalizacao do comando\n")
            self.caixa_texto.insert(tk.END, f"{self.cfg[5]} M82; Desabilita os motores de passo\n")
            self.last_updt(seringa, valor_combox)
            self.caixa_texto.yview('end')
        else: self.blank()

    def reset_valv(self, tag):
        if self.valvttg.get() == 0 or tag == 1:
            gcode_reset = f"{self.cfg[5]} M211 S0; Desabilita os fins de curso virtuais\n"
            if tag == 0:
                for id in list(self.valvp.keys()):
                    for p in self.reset_vpos:
                        gcode_reset += f"{self.cfg[5]} G1 {id}{p} F{round(self.feedV.get() * 1.25, 2)};\n"
                    gcode_reset += f"{self.cfg[5]} M400; Espera a finalizacao do comando\n"
                gcode_reset += f"{self.cfg[5]} G28; Reseta a posição de todas as valvulas\n"
            else:
                gcode_reset += f"{self.cfg[5]} G1 X0 A0 B0 Y0 Z0 F{round(self.feedV.get() * 1.25, 2)}; Posição zero\n"
            gcode_reset += f"{self.cfg[5]} G1"
            for id in list(self.valvp.keys()):
                gcode_reset += f" {id}{self.valvp[id][4]}"
            gcode_reset += f" F{round(self.feedV.get() / 2, 2)}; Ajuste fino das válvulas\n"
            gcode_reset += f"{self.cfg[5]} G92"
            for id in list(self.valvp.keys()):
                gcode_reset += f" {id}0"
                self.lastvalv[id] = 0
            gcode_reset += "; Set zero das válvulas\n"
            gcode_reset += f"{self.cfg[5]} G1"
            for id in list(self.valvp.keys()):
                gcode_reset += f" {id}{self.valvp[id][3]}"
            gcode_reset += f" F{self.feedV.get()}; Posição de segurança das válvulas\n"
            if self.valvttg.get() == 0: self.valvttg.set(1)
            if tag == 0: self.caixa_texto.insert(tk.END, gcode_reset)
            return gcode_reset

    def interpreta_valvula(self, idx, comando):
        gcode = ''
        if comando == "Encher":
            pos = self.lastvalv[idx]+self.valvp[idx][3]
            gcode += f"{self.cfg[5]} G1 {idx}{pos} F{self.feedV.get()}; "
            gcode += f"Valvula da seringa {idx} na posicao pipetar\n"
            self.lastvalv[idx] = pos
        elif comando == "Manifold":
            gcode += f"{self.cfg[5]} G1 {idx}{self.valvp[idx][1]} F{self.feedV.get()}; "
            gcode += f"Valvula da seringa {idx} na posicao manifold\n"
            self.lastvalv[idx] = self.valvp[idx][1]
        elif comando == "Ejetar":
            for id in list(self.valvp.keys())[::-1]:
                if id == idx:
                    gcode += f"{self.cfg[5]} G1 {idx}{self.valvp[idx][0]} F{self.feedV.get()}; "
                    gcode += f"Valvula da seringa {idx} na posicao verter\n"
                    self.lastvalv[idx] = self.valvp[idx][2]
                    break
                gcode += f"{self.cfg[5]} G1 {id}{self.valvp[id][1]} F{self.feedV.get()}; "
                gcode += f"Valvula da seringa {id} na posicao manifold\n"
                self.lastvalv[id] = self.valvp[id][1]
        elif comando == "via":
            gcode += f"{self.cfg[3]} M280 P0 S{idx*self.val_via.get()}\n"
        return gcode

    def clicou_ser(self, seringa, cbox, entry, tag):
        if entry.replace(".", '', 1).isnumeric() and cbox != "Manifold" and len(entry) > 0:
            self.ser_ini(seringa, tag)
            entry = float(entry)
            con = (self.last[seringa] + entry) <= self.func_vol(seringa, 1) and entry != 0
            con1 = (self.last[seringa] - entry) >= 0 and entry != 0
            if cbox == 'Encher' and con:
                val = self.last[seringa] + entry
                self.protoc_plot(val, cbox, seringa, tag)
            elif cbox == 'Ejetar' and con1:
                val = self.last[seringa] - entry
                self.dir_plot(self.vert.get(), tag)
                self.protoc_plot(val, cbox, seringa, tag)
                self.autox_comm(seringa, tag)
            elif cbox == 'Encher' and entry > 0 and tag != 0:
                self.err(6)
            elif tag not in [0, 4]:
                self.err(4)
        elif cbox != "Manifold" and len(entry) > 0:
            self.err(1)
        else: self.blank()
        self.txt_clean(seringa)

    def protoc_plot(self, val, combox, eix, tag):
        chng = val - self.last[eix]
        feed = self.curva[eix] * 60
        laste = self.lastmov[1]
        self.last[eix] = round(val, 3)
        if (self.lastmov[0] != combox or laste != eix) and (self.autoserv.get() or tag == 0):
            self.clicou_val(eix, combox, False)
        feed *= self.feedX.get() if eix == 'X' else 1
        feed *= self.feedA.get() if eix == 'A' else 1
        feed *= self.feedB.get() if eix == 'B' else 1
        feed *= self.feedY.get() if eix == 'Y' else 1
        feed *= self.feedZ.get() if eix == 'Z' else 1
        if tag == 4 and eix == 'X': feed = self.feedautop.get() * self.curva[eix] * 60
        translator = {value: key for key, value in self.sr_ex.items()}
        self.caixa_texto.insert(tk.END,
                                f"{self.cfg[3]} G1 {eix[0]}{round(chng * self.curva[eix], 3)} F{round(feed, 3)}; ")
        self.caixa_texto.insert(tk.END, f"Movimenta o embolo da {translator[eix]}\n")
        self.caixa_texto.insert(tk.END, f"{self.cfg[3]} M400; Espera a finalizacao do comando\n")
        self.caixa_texto.insert(tk.END, f"{self.cfg[3]} M82 {eix}; Desabilita o motor da {translator[eix]}\n")
        self.caixa_texto.yview('end')
        self.vol_updt(eix, chng) if tag not in [0, 4] else None

    def dir_plot(self, way, tag):
        if self.lastmov[2] != way and tag != 0:
            self.caixa_texto.insert(tk.END, self.interpreta_valvula(way, "via"))
            self.lastmov[2] = way

    def autox_comm(self, eix, tag):
        if self.autox.get() and eix != 'X' and self.lastmov[1] != 'X' and tag != 0:
            if tag != 2: self.log_updt()
            currentvol = 0 if self.last['X'] == 'nan' else self.last['X']
            autovol = round(self.func_vol('X', 1) * (self.state_cap[0] / 100) - currentvol, 2)
            self.clicou_ser('X', 'Encher', str(autovol), 4)
            self.clicou_ser('X', 'Ejetar', str(autovol), 0)
            self.vol_updt('Auto-X', autovol)

    def vol_updt(self, eix, chng):
        self.console.config(state="normal")
        self.logcount.set(self.logcount.get()+1)
        gcode = f"\n-->[{self.logcount.get():03d}]\t      [Volume atual]\n"
        gcode += f"-->[Alteração]\t[{eix}] " + ('+' if chng > 0 else '') + f"{chng:.3f} mL\n"
        for i in list(self.sr_ex.keys())[1:6]:
            mxval = self.func_vol(self.sr_ex[i], 1)
            try:
                gcode += f"-->[{i}] {self.last[self.sr_ex[i]]:06.3f} / "
                gcode += f"{mxval:05.2f} mL\n"
            except: gcode += f"-->[{i}]  Nulo  / {mxval:05.2f} mL\n"
        self.console.insert(tk.END, gcode, 'g')
        self.console.yview('end')
        self.console.config(state="disabled")

    def last_updt(self, eix, combox):
        self.lastmov[1] = eix
        self.lastmov[0] = combox

    def txt_clean(self, seringa):
        self.entry6.delete(0, tk.END) if seringa == 'X' else None
        self.entry7.delete(0, tk.END) if seringa == 'A' else None
        self.entry8.delete(0, tk.END) if seringa == 'B' else None
        self.entry9.delete(0, tk.END) if seringa == 'Y' else None
        self.entry10.delete(0, tk.END) if seringa == 'Z' else None
        self.entry15.delete(0, tk.END) if seringa == 'P' else None

    def blank(self):
        self.log_updt()
        self.console.config(state="normal")
        self.console.insert(tk.END, '\n-->[NADA A GRAVAR]<--\n', 'g')
        self.console.yview('end')
        self.console.config(state="disabled")

    def err(self, typ):
        self.log_updt()
        self.console.config(state="normal")
        if typ == 1: self.console.insert(tk.END, '\n-->[COMANDO INCORRETO]\n', 'r')
        elif typ == 2: self.console.insert(tk.END, '\n-->[VALOR MUITO ALTO]<--\n', 'r')
        elif typ == 3: self.console.insert(tk.END, '\n-->[ERRO DE VALOR]<--\n', 'r')
        elif typ == 4:
            self.console.insert(tk.END, '\n-->[VOLUME INSUFICIENTE]<--\n', 'r')
            self.vol_updt(self.lastmov[1], 0)
        elif typ == 5: self.console.insert(tk.END, '\n-->[VALOR INDEFINIDO]<--\n', 'r')
        elif typ == 6:
            self.console.insert(tk.END, '\n-->[VOLUME ACIMA DO LIMITE]<--\n', 'r')
            self.vol_updt(self.lastmov[1], 0)
        else: self.console.insert(tk.END, '\n-->[ERRO DE COMANDO]<--\n', 'r')
        self.console.yview('end')
        self.console.config(state="disabled")

    def clicou_aquecimento(self):
        valor_entry = float(self.temp.get())
        if valor_entry != self.lastmix[0]:
            self.log_updt()
            self.caixa_texto.insert(tk.END,
                                    f"{self.cfg[3]} M104 S{round(valor_entry, 1)}; Aciona sistema de aquecimento [TAG_HEAT]\n")
            self.caixa_texto.yview('end')
            self.lastmix[0] = valor_entry
            self.pos_statusmisc(1)
        else: self.blank()

    def clicou_agitacao(self):
        valor_entry = int(self.agit.get())
        if valor_entry != self.lastmix[1]:
            val = (valor_entry/100) * (255-self.minagit.get()) + (self.minagit.get() if valor_entry else 0)
            self.log_updt()
            self.caixa_texto.insert(tk.END,
                                    f"{self.cfg[3]} M42 I P9 S{round(val)}; Aciona sistema de agitacao [TAG_AGT]\n")
            self.caixa_texto.yview('end')
            self.lastmix[1] = valor_entry
            self.pos_statusmisc(1)
        else: self.blank()

    def comm_wait(self):
        txt_entry = [self.wait_txt, self.wait_txt1, self.wait_txt2]
        timer = [0, 0, 0]
        valor = 0
        try:
            for txt in txt_entry:
                idx = txt_entry.index(txt)
                if txt.get() != '' and txt.get().isnumeric():
                    if len(txt.get()) <= 2 and int(txt.get()) < 59:
                        timer[idx] = int(txt.get())
                        valor += int(txt.get()) * (60 ** idx)
                    elif len(txt.get()) <= 2 and idx < 2:
                        timer[idx] = int(txt.get()) - 60
                        timer[idx + 1] += 1
                        valor += int(txt.get()) * (60 ** idx)
                    else:
                        txt.set(txt.get()[:2])
                        self.err(2)
                        return
                else: txt.set('')
            if valor != 0 and float(valor) <= 90000:
                self.log_updt()
                self.caixa_texto.insert(tk.END,
                                        f"{self.cfg[3]} G4 S{valor}; Aguarda {valor} segundos antes de prosseguir\n")
                self.caixa_texto.yview('end')
                for i in range(3): self.lastdelay[i] = timer[i]
                self.pos_statusmisc(4)
            elif valor != 0: self.err(2)
            else:
                for i in txt_entry: i.set('')
                self.err(3)
        except:
            for i in txt_entry: i.set('') if not i.get().isnumeric() else None
            self.err(1)

    def pos_statusmisc(self, typ):
        self.console.config(state="normal")
        self.logcount.set(self.logcount.get() + 1)
        if typ == 1:
            self.console.insert(tk.END,
                                f'\n-->[{self.logcount.get():03d}]\t       [Valores atuais]'
                                f'\n-->[Agitação]\t\t  {self.lastmix[1]}%'
                                f'\n-->[Aquecimento]\t {round(self.lastmix[0], 2)} ºC', 'g')
            self.console.yview('end')
        elif typ == 2:
            self.console.insert(tk.END,
                                f"\n-->[{self.logcount.get():03d}]\t        [Valores atuais]\n"
                                f"-->[Posição][{self.last_amostr[3]:02d}] "
                                f"X{round(self.last_amostr[0], 2)} || Y{round(self.last_amostr[1], 2)}\n"
                                f"-->[Feedrate]    F{round(self.last_amostr[2], 2)}\n"
                                f"-->[Bandeja]   {self.last_amostr[4]}\n"
                                f"-->[Estado]      {self.last_amostr[5]} "
                                + (f"[{self.last_amostr[6]}]" if self.last_amostr[5] == 'Abaixar' else '')+"\n", 'g')
            self.console.yview('end')
        elif typ == 3:
            self.console.insert(tk.END, f"\n-->[{self.logcount.get():03d}]\t  [Controle da Bomba]\n\
-->[Volume drenado]  {round(self.last_amostr[7], 2):06.2f} mL\n", 'g')
            self.console.yview('end')
        elif typ == 4:
            self.console.insert(tk.END, f"\n-->[{self.logcount.get():03d}]\t[Controle de atraso]\n\
-->[Último delay]  [{self.lastdelay[0]:02d}:{self.lastdelay[1]:02d}:{self.lastdelay[2]:02d}]\n", 'g')
            self.console.yview('end')
        self.console.config(state="disabled")

    def controle_pos(self):
        tray_type = self.cbox6.get()
        toggle = self.cbox7.get()
        checkb = self.check1.get()
        height = float(self.spin_needle.get()) + self.minvol['P']

        # Tipos de bandeja
        # Formato [X0, Y0, VarX, VarY]
        btype1 = [13, 45, 39.5, 39.5]   #Bandeja [2X3]
        btype2 = [3, 37, 19.1, 18.5]    #Bandeja [4X6]
        btype3 = [13, 41.6, 25.2, 26.2] #Bandeja [3X4]
        bvar = 130.8

        lastck1 = checkb != self.last_amostr[3] or tray_type != self.last_amostr[4]
        lastck2 = toggle != self.last_amostr[5] or height != self.last_amostr[6]
        if checkb != 0 and tray_type != 'Nenhum' and lastck1:
            self.log_updt()
            feedr = float(self.entry14.get())
            if tray_type in [self.cbox6['values'][1], self.cbox6['values'][2]] or tray_type == \
                    self.cbox6['values'][3]:
                bandeja = btype1
                upx = btype1[2] * ((checkb - 1) % 3)
                upy = btype1[3] * ((checkb - 1) // 3)
            elif tray_type in [self.cbox6['values'][4], self.cbox6['values'][5]] or tray_type == \
                    self.cbox6['values'][6]:
                bandeja = btype2
                upx = btype2[2] * ((checkb - 1) % 6)
                upy = btype2[3] * ((checkb - 1) // 6)
            elif tray_type in [self.cbox6['values'][7], self.cbox6['values'][8]] or tray_type == \
                    self.cbox6['values'][9]:
                bandeja = btype3
                upx = btype3[2] * ((checkb - 1) % 4)
                upy = btype3[3] * ((checkb - 1) // 4)
            else:
                self.blank()
                return
            bandeja[0] += bvar if 'B' in tray_type else bvar * 2 if 'C' in tray_type else 0
            stats = [upx + bandeja[0], bandeja[1] + upy, feedr, int(checkb), tray_type, toggle, height]
            gcode = self.comm_pip(stats)
            for i in range(7): self.last_amostr.insert(i, stats[i])
            self.pos_statusmisc(2)
        elif checkb != 0 and lastck2 and tray_type != 'Nenhum':
            self.log_updt()
            gcode = self.misc_pip('', self.cbox7['values'].index(toggle))
            self.last_amostr.insert(5, toggle)
            self.last_amostr.insert(6, height)
            self.pos_statusmisc(2)
        else:
            self.blank()
            return
        self.caixa_texto.insert(tk.END, gcode, 'g')
        self.caixa_texto.yview('end')

    def comm_pip(self, lista):
        feed = lista[2] if lista[2] != 0 else float(self.entry14.get())
        gcode = ''
        gcode = self.misc_pip(gcode, 1)
        gcode = self.misc_pip(gcode, 2)
        gcode += f"{self.cfg[7]} G1 X{round(lista[0])} Y{round(lista[1])} F{round(feed, 2)};"
        gcode += f" Posiciona o pipetador na posiçao {lista[3]}\n"
        gcode = self.misc_pip(gcode, 0) if lista[0:2] != [0,0] else gcode
        return gcode

    def misc_pip(self, gcode, tag):
        height = ((float(self.spin_needle.get()) + self.minvol['P']) / self.mxvol['P']) * 170
        if self.cbox7.get() == "Abaixar" and tag == 0:
            gcode += f"{self.cfg[7]} M3 S{height}; Abaixa o pipetador\n"
            gcode += f"{self.cfg[7]} G4 P1; Espera o pipetador abaixar\n"
        if tag == 1:
            gcode += f"{self.cfg[7]} M3 S160; Levanta o pipetador por segurança\n"
            gcode += f"{self.cfg[7]} G4 P1; Espera o pipetador levantar\n"
        if (self.redftggl.get() == 1 and tag == 2) or tag == 3:
            gcode += f"{self.cfg[7]} $H; Homing\n"
            self.redftggl.set(0)
        return gcode

    def descarte_pip(self, flag):
        gcode = ''
        if flag == 0:
            gcode = self.misc_pip(gcode, 1)
            if self.last_amostr[0:2] != [0,0]: gcode += f"{self.cfg[7]} G1 X0 Y0 F{float(self.entry14.get())};\n"
        elif flag == 1: gcode = self.comm_pip(self.last_amostr)
        if gcode != '': self.caixa_texto.insert(tk.END, gcode)

    def controle_pump(self, entryp, tag):
        if entryp.replace(".", '', 1).isnumeric() and len(entryp) > 0:
            self.log_updt() if tag == 0 else None
            entryp = (float(entryp) if float(entryp) <= self.mxvol['R'] else self.mxvol['R'])
            self.last_amostr.insert(7, entryp)
            time = round(((entryp if entryp > 0 else 0)/self.curva['P']), 2)
            gcode = self.misc_pip('', 2)
            gcode += f"{self.cfg[3]} M42 I P8 S254; Liga a bomba persitaltica [TAG_PUMP]\n"
            gcode += f"{self.cfg[3]} G4 S{round(time*self.dvolp.get(),2)}; Aguarda o volume da peristaltica\n"
            gcode += f"{self.cfg[3]} M42 I P8 S0; Desliga a bomba persitaltica [TAG_PUMP]\n"
            gcode += f"{self.cfg[3]} G4 S{round(time*(1-self.dvolp.get()),2)}; Aguarda depressurizacao\n"
            self.caixa_texto.insert(tk.END, gcode, 'g')
            self.caixa_texto.yview('end')
            self.txt_clean('P')
            self.pos_statusmisc(3)
        else: self.blank()

    def gravar_texto(self):
        texto = filedialog.asksaveasfile(mode='w', defaultextension=".gcode")
        if texto is None: return
        texto.write(self.caixa_texto.get("1.0", tk.END))
        texto.write(self.end_setup())
        messagebox.showinfo('', 'PROGRAMA GRAVADO COM SUCESSO!\n\n' + os.path.abspath(texto.name))
        texto.close()


class Config:
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.win.grab_set()
        self.win.title("Configurar")
        self.win.resizable(0, 0)

        # Buscando as variaveis
        self.portramp = tk.StringVar()
        self.portramp.set(app.cfg[3])
        self.portservo = tk.StringVar()
        self.portservo.set(app.cfg[5])
        self.portpip = tk.StringVar()
        self.portpip.set(app.cfg[7])
        self.portl = scan_serial()

        self.mxval1 = tk.DoubleVar()
        self.mxval1.set(app.mxvol['X'])
        self.mxval2 = tk.DoubleVar()
        self.mxval2.set(app.mxvol['A'])
        self.mxval3 = tk.DoubleVar()
        self.mxval3.set(app.mxvol['B'])
        self.mxval4 = tk.DoubleVar()
        self.mxval4.set(app.mxvol['Y'])
        self.mxval5 = tk.DoubleVar()
        self.mxval5.set(app.mxvol['Z'])
        self.mxval = [self.mxval1, self.mxval2, self.mxval3, self.mxval4, self.mxval5]

        self.minval1 = tk.DoubleVar()
        self.minval1.set(app.minvol['X'])
        self.minval2 = tk.DoubleVar()
        self.minval2.set(app.minvol['A'])
        self.minval3 = tk.DoubleVar()
        self.minval3.set(app.minvol['B'])
        self.minval4 = tk.DoubleVar()
        self.minval4.set(app.minvol['Y'])
        self.minval5 = tk.DoubleVar()
        self.minval5.set(app.minvol['Z'])
        self.minval = [self.minval1, self.minval2, self.minval3, self.minval4, self.minval5]

        self.minpump = tk.DoubleVar()
        self.minpump.set(app.minvol['P'])

        self.ser_keys = app.sr_ex.copy()
        self.dead_x = tk.DoubleVar()
        self.dead_x.set(app.dump_vol['X'])
        self.dead_a = tk.DoubleVar()
        self.dead_a.set(app.dump_vol['A'])
        self.dead_b = tk.DoubleVar()
        self.dead_b.set(app.dump_vol['B'])
        self.dead_y = tk.DoubleVar()
        self.dead_y.set(app.dump_vol['Y'])
        self.dead_z = tk.DoubleVar()
        self.dead_z.set(app.dump_vol['Z'])
        self.dead_val = {'X': self.dead_x, 'A': self.dead_a, 'B': self.dead_b, 'Y': self.dead_y, 'Z': self.dead_z}

        self.autox_val = tk.DoubleVar()
        self.autox_val.set(app.state_cap[0])

        self.autopumpf = tk.DoubleVar()
        self.autopumpf.set(app.feedautop.get())

        self.dead_p = tk.DoubleVar()
        self.dead_p.set(app.dvolp.get())
        self.feed_p = tk.DoubleVar()
        self.feed_p.set(app.feedP.get()/app.curva['P'])

        # Criando os botões config
        self.botao_confirm = tk.Button(win, text="Aplicar", command=lambda: self.apply_cfg())
        self.botao_reset = tk.Button(win, text="Reset", command=lambda: self.reset())
        self.botao_desfazer = tk.Button(win, text="Desfazer", command=lambda: self.desfazer())

        self.lab = tk.Label(win, text="Placa principal:")
        self.nameramp = tk.Entry(win, width=12, textvariable=self.portramp)
        self.cbramp = ttk.Combobox(win, state="readonly", width=8, postcommand=lambda: self.cbox_mng(self.cbramp, 0))
        self.cbramp.set(app.cfg[2])

        self.lab1 = tk.Label(win, text="Placa dos servos:")
        self.nameservo = tk.Entry(win, width=12, textvariable=self.portservo)
        self.cbserv = ttk.Combobox(win, state="readonly", width=8, postcommand=lambda: self.cbox_mng(self.cbserv, 0))
        self.cbserv.set(app.cfg[4])

        self.lab2 = tk.Label(win, text="Placa do pipetador:")
        self.namepip = tk.Entry(win, width=12, textvariable=self.portpip)
        self.cbpip = ttk.Combobox(win, state="readonly", width=8, postcommand=lambda: self.cbox_mng(self.cbpip, 0))
        self.cbpip.set(app.cfg[6])

        # Criando as scrollbox
        self.scrolab = []
        self.spbox = []
        for i in range(5): self.scrolab.append(tk.Label(win, text=f"Seringa {i + 1}:"))
        for i in range(10): self.scrolab.append(tk.Label(win, text="mL"))
        for i in range(5): self.scrolab.append(tk.Label(win, text="[Min]"))
        for i in range(5): self.scrolab.append(tk.Label(win, text="[Max]"))
        for i in range(5):
            self.spbox.append(tk.Spinbox(win, from_=1, to=60, increment=0.1, textvariable=self.mxval[i], width=4))
            self.spbox[-1].config(repeatdelay=150, repeatinterval=10, state="readonly", command=lambda: self.minvol_mng(1))
        for i in range(5):
            self.spbox.append(tk.Spinbox(win, from_=0, to=round((self.mxval[i].get()+10) / 10), increment=0.01, format='%.2f'))
            self.spbox[-1].config(repeatdelay=100, repeatinterval=5, width=4, textvariable=self.minval[i], state="readonly")

        # Criando os botoes extras
        self.lab3 = tk.Label(win, text="Máximo do Descarte:")
        self.cb_deadv = ttk.Combobox(win, state="readonly", width=8, values=list(self.ser_keys.keys())[1:6])
        self.cb_deadv.bind('<<ComboboxSelected>>', lambda event: self.cbox_mng(self.spin_deadv, 1))
        self.spin_deadv = tk.Spinbox(win, from_=0, to=100, increment=0.5, state="readonly", format='%.2f')
        self.spin_deadv.config(repeatdelay=200, repeatinterval=24, width=5, textvariable=self.dead_val['X'])
        self.lab4 = tk.Label(win, text=f"%   -->")
        self.cb_deadv.current(0)

        self.lab5 = tk.Label(win, text="Máximo do Auto Pump:")
        self.autox_cap = tk.Spinbox(win, from_=10, to=100, increment=0.5, state="readonly", textvariable=self.autox_val)
        self.autox_cap.config(repeatdelay=200, repeatinterval=24, width=5, command=lambda: self.minvol_mng(2))
        self.lab6 = tk.Label(win, text=f"%         --> [{round(self.mxval1.get() * (self.autox_val.get() / 100), 1)}] mL")

        self.lab7 = tk.Label(win, text="Enchimento do Auto Pump:")
        self.autox_feed = tk.Spinbox(win, from_=0.005, to=10, increment=0.005, state="readonly", textvariable=self.autopumpf)
        self.autox_feed.config(repeatdelay=200, repeatinterval=2, width=6, command=lambda: self.minvol_mng(3))
        self.lab8 = tk.Label(win, text=f"mL/s  --> [{round(self.autopumpf.get()/app.feedX.get(), 2)*100:03.1f}] %")

        self.lab9 = tk.Label(win, text="Altura da Agulha:")
        to_text = round(app.mxvol['P']-float(app.spin_needle.get()))
        self.needl_h = tk.Spinbox(win, from_=0, to=to_text, textvariable=self.minpump)
        self.needl_h.config(repeatdelay=200, repeatinterval=24, width=5, increment=0.5, state="readonly")
        self.lab10 = tk.Label(win, text=f"mm")

        self.lab11 = tk.Label(win, text="Vol. Morto da Bomba:")
        self.pump_d = tk.Spinbox(win, from_=0, to=1000, increment=0.5, state="readonly", textvariable=self.dead_p)
        self.pump_d.config(repeatdelay=200, repeatinterval=24, width=5)
        self.lab12 = tk.Label(win, text=f"mL")

        self.lab13 = tk.Label(win, text="Feedrate da Bomba:")
        self.feed_d = tk.Spinbox(win, from_=1, to=100, increment=0.05, state="readonly", textvariable=self.feed_p)
        self.feed_d.config(repeatdelay=100, repeatinterval=3, width=6)
        self.lab14 = tk.Label(win, text=f"mL/s")

        self.grid_config()
        return
    def grid_config(self):
        # Posicionando comboxes
        self.lab.grid(row=0, column=0, columnspan=2, padx=42, pady=10, sticky="E")
        self.nameramp.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="E")
        self.cbramp.grid(row=0, column=2, columnspan=4, padx=50, pady=10, sticky="W")

        self.lab1.grid(row=1, column=0, columnspan=2, padx=42, pady=10, sticky="E")
        self.nameservo.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="E")
        self.cbserv.grid(row=1, column=2, columnspan=4, padx=50, pady=10, sticky="W")

        self.lab2.grid(row=2, column=0, columnspan=2, padx=42, pady=10, sticky="E")
        self.namepip.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="E")
        self.cbpip.grid(row=2, column=2, columnspan=4, padx=50, pady=10, sticky="W")

        # Posicionando scrollboxes
        for i in range(5):
            self.scrolab[i].grid(row=i + 3, column=0, padx=8, sticky="E")
            self.scrolab[i+5].grid(row=i + 3, column=1, columnspan=3, padx=16, sticky="E")
            self.scrolab[i+10].grid(row=i + 3, column=5, padx=18, sticky="E")
            self.scrolab[i+15].grid(row=i + 3, column=1, columnspan=3, sticky="W")
            self.scrolab[i+20].grid(row=i + 3, column=4, columnspan=2, padx=0, sticky="W")
        for i in range(5): self.spbox[i].grid(row=i+3, column=4, columnspan=2, padx=40, sticky="W")
        for i in range(5): self.spbox[i+5].grid(row=i+3, column=1, columnspan=3, padx=38, pady=10, sticky="W")

        # Posicionando botoes
        self.botao_reset.grid(row=15, column=0, columnspan=1, padx=10, pady=10, sticky="W")
        self.botao_desfazer.grid(row=15, column=0, columnspan=2, padx=50, pady=0, sticky="W")
        self.botao_confirm.grid(row=15, column=0, columnspan=2, padx=50, pady=0, sticky="E")

        self.lab5.grid(row=8, column=0, columnspan=2, sticky="E", padx=25, pady=2)
        self.lab6.grid(row=8, column=3, columnspan=3, sticky="W", padx=0, pady=2)
        self.autox_cap.grid(row=8, column=1, columnspan=3, sticky="E", padx=25, pady=2)
        self.lab7.grid(row=9, column=0, columnspan=2, sticky="E", padx=25, pady=2)
        self.lab8.grid(row=9, column=3, columnspan=3, sticky="W", padx=5, pady=2)
        self.autox_feed.grid(row=9, column=1, columnspan=3, sticky="E", padx=20, pady=2)
        self.lab3.grid(row=10, column=0, columnspan=2, sticky="E", padx=25, pady=2)
        self.lab4.grid(row=10, column=3, columnspan=3, sticky="W", padx=0, pady=2)
        self.spin_deadv.grid(row=10, column=1, columnspan=3, sticky="E", padx=25, pady=2)
        self.cb_deadv.grid(row=10, column=3, columnspan=3, sticky="E", padx=30, pady=2)
        self.lab9.grid(row=12, column=0, columnspan=2, sticky="E", padx=25, pady=2)
        self.lab10.grid(row=12, column=3, columnspan=3, sticky="W", padx=0, pady=2)
        self.needl_h.grid(row=12, column=1, columnspan=3, sticky="E", padx=25, pady=2)
        self.lab11.grid(row=13, column=0, columnspan=2, sticky="E", padx=25, pady=2)
        self.lab12.grid(row=13, column=3, columnspan=3, sticky="W", padx=0, pady=2)
        self.pump_d.grid(row=13, column=1, columnspan=3, sticky="E", padx=25, pady=2)
        self.lab13.grid(row=14, column=0, columnspan=2, sticky="E", padx=25, pady=2)
        self.lab14.grid(row=14, column=3, columnspan=3, sticky="W", padx=5, pady=2)
        self.feed_d.grid(row=14, column=1, columnspan=3, sticky="E", padx=20, pady=2)

    def cbox_mng(self, cbox, tag):
        if tag == 0:
            cbox['values'] = [i for i in self.portl if i not in [self.cbramp.get(), self.cbserv.get(), self.cbpip.get()]]
        if tag == 1: cbox['textvariable'] = self.dead_val[self.ser_keys[self.cb_deadv.get()]]

    def minvol_mng(self, tag):
        if tag == 1:
            for i in range(5): self.spbox[i+5]['to'] = round((self.mxval[i].get() + 10) / 10, 2)
        if tag == 2: self.lab6['text'] = f"%   --> [{round(self.mxval[0].get() * (self.autox_val.get() / 100), 1)}] mL"
        if tag == 3: self.lab8['text'] = f"mL/s  --> [{round(self.autopumpf.get()/app.feedX.get(), 2)*100:03.1f}] %"

    def apply_cfg(self):
        app.log_updt()
        oldidx = []
        for i in app.cfg: oldidx.append(i)
        app.cfg[2] = self.cbramp.get()
        app.cfg[3] = self.nameramp.get()
        app.cfg[4] = self.cbserv.get()
        app.cfg[5] = self.nameservo.get()
        app.cfg[6] = self.cbpip.get()
        app.cfg[7] = self.namepip.get()
        for i in list(app.mxvol.keys())[:5]: app.mxvol[i] = self.mxval[list(app.mxvol.keys()).index(i)].get()
        for i in list(app.minvol.keys())[:5]: app.minvol[i] = self.minval[list(app.minvol.keys()).index(i)].get()
        for i in list(self.dead_val.keys()): app.dump_vol[i] = self.dead_val[i].get()
        app.minvol['P'] = self.minpump.get()
        app.spin_needle.config(to=app.mxvol['P']-self.minpump.get())
        app.state_cap = [self.autox_val.get()]
        app.dvolp.set(self.dead_p.get())
        app.feedautop.set(self.autopumpf.get())
        app.feedP.set(self.feed_p.get()*app.curva['P'])
        for i in range(2, (app.cfg[1] * 2) + 2):
            maintxt = app.caixa_texto.get('1.0', 'end-1c').replace(oldidx[i], app.cfg[i])
            app.caixa_texto.replace('1.0', 'end-1c', maintxt)
        app.console.config(state="normal")
        app.console.insert(tk.END, '\n-->[Configurações alteradas]', 'g')
        app.vol_updt('all', 0)

    def reset(self):
        if messagebox.askyesno('Reset', 'Retornar as configurações padrão?', parent=self.win):
            app.log_updt()
            app.sys_config()
            app.console.insert(tk.END, '\n-->[Configurações alteradas]', 'g')
            app.vol_updt('all', 0)
            janelaspop('conf')
            self.win.destroy()

    def desfazer(self):
        app.desfazer()
        janelaspop('conf')
        self.win.destroy()

class Serialmonitor:
    def __init__(self, win2):
        super().__init__()
        self.win2 = win2
        self.win2.title("Monitor Serial")
        self.win2.resizable(0, 0)
        self.aaa = tk.StringVar()
        self.botao1 = tk.Button(win2, text="Seringa 2",
                                command=lambda: app.console.insert(tk.END, '-->[Estou mexendo ainda]\n', 'g'))
        self.botao1.grid(row=0, column=0)
        self.entry10 = tk.Entry(win2, textvariable=self.aaa)
        self.entry10.grid(row=0, column=1)

class Calibrar:
    def __init__(self, win1):
        super().__init__()
        self.win1 = win1
        self.win1.grab_set()
        self.win1.title("Calibração")
        self.win1.resizable(0, 0)
        self.botao1 = tk.Button(win1, text="Seringa 1",
                                command=lambda: app.console.insert(tk.END, '-->[Estou mexendo ainda]\n', 'g'))
        self.botao1.grid(row=0, column=0)

def scan_serial():
    ports = [app.cfg[2], app.cfg[4], app.cfg[6]]
    for port, desc, hwid in sorted(serial.tools.list_ports.comports()): ports.append(port)
    return ports
def janelaspop(jal):
    global win_switch, win_pop
    if jal == 'cal':
        win_pop = tk.Toplevel(root)
        Calibrar(win_pop)
        root.eval(f'tk::PlaceWindow {str(win_pop)} center')
    if jal == 'ser':
        try: win_switch.deiconify()
        except NameError:
            win_switch = tk.Toplevel(root)
            win_switch.wm_protocol("WM_DELETE_WINDOW", win_switch.iconify)
            Serialmonitor(win_switch)
            win_switch.update_idletasks()
            height = win_switch.winfo_height()
            titlebar_height = win_switch.winfo_rooty() - win_switch.winfo_y()
            win_height = height + titlebar_height
            x = root.winfo_rootx() + root.winfo_width() - win_switch.winfo_width()
            y = win_switch.winfo_screenheight() // 2 - win_height // 2
            win_switch.geometry(f"{win_switch.winfo_width()}x{height}+{x}+{y}")
    if jal == 'conf':
        win_pop = tk.Toplevel(root)
        Config(win_pop)
        root.eval(f'tk::PlaceWindow {str(win_pop)} center')

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
