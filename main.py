import ttkbootstrap as ttk
import ttkbootstrap.constants as constants


class TurnoGusano(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        master.place_window_center()
        self.master = master

        self.master['padx'] = 20
        self.master['pady'] = 20

        self.actions = ['', '', '']
        self.combosOptions = [
            '',
            'Saltar',
            'Voltear',
            'Disparar'
        ]
        self.optsActions = {
            '': '',
            'Saltar':   'j',
            'Voltear':  'f',
            'Disparar': 's'
        }

        text1 = ttk.Label(self.master, text='Selecciona tus acciones')
        text1.grid(row=0, column=0, columnspan=3, sticky=constants.W)

        text2 = ttk.Label(self.master, text='Acción')
        text2.grid(row=1, column=0, pady=10)

        text3 = ttk.Label(self.master, text='Angulo')
        text3.grid(row=1, column=1, pady=10)

        text4 = ttk.Label(self.master, text='Fuerza')
        text4.grid(row=1, column=2, pady=10)

        # 1ª acción

        self.setvar('action1', '')
        self.accion1 = ttk.Combobox(
            self.master,
            values=self.combosOptions,
            state='readonly',
        )
        self.accion1.bind(
            '<<ComboboxSelected>>',
            lambda event, entry=self.accion1: self.update_value(entry.get(), 'action1'))
        self.accion1.grid(row=2, column=0, sticky=constants.W)

        angle1Frame = ttk.Frame(self.master)
        angle1Frame.grid(row=2, column=1, sticky=constants.W, padx=10)
        self.setvar('angle1', 0)

        angle1Label = ttk.Label(angle1Frame, textvariable='angle1', anchor=constants.CENTER)
        angle1Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.angle1 = ttk.Scale(
            angle1Frame,
            from_=0,
            to=120,
            command=lambda x, y='angle1': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.angle1.pack()

        force1Frame = ttk.Frame(self.master)
        force1Frame.grid(row=2, column=2, sticky=constants.W, padx=10)
        self.setvar('force1', 0)

        angle1Label = ttk.Label(force1Frame, textvariable='force1', anchor=constants.CENTER)
        angle1Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.force1 = ttk.Scale(
            force1Frame,
            from_=1,
            to=10,
            command=lambda x, y='force1': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.force1.pack()

        # 2ª acción

        self.setvar('action2', '')
        self.accion2 = ttk.Combobox(
            self.master,
            values=self.combosOptions,
            state='readonly',
        )
        self.accion2.bind(
            '<<ComboboxSelected>>',
            lambda event, entry=self.accion2: self.update_value(entry.get(), 'action2'))
        self.accion2.grid(row=3, column=0, sticky=constants.W)

        angle2Frame = ttk.Frame(self.master)
        angle2Frame.grid(row=3, column=1, sticky=constants.W, padx=10)
        self.setvar('angle2', 0)

        angle2Label = ttk.Label(angle2Frame, textvariable='angle2', anchor=constants.CENTER)
        angle2Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.angle2 = ttk.Scale(
            angle2Frame,
            from_=0,
            to=120,
            command=lambda x, y='angle2': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.angle2.pack()

        force2Frame = ttk.Frame(self.master)
        force2Frame.grid(row=3, column=2, sticky=constants.W, padx=10)
        self.setvar('force2', 0)

        force2Label = ttk.Label(force2Frame, textvariable='force2', anchor=constants.CENTER)
        force2Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.force2 = ttk.Scale(
            force2Frame,
            from_=1,
            to=10,
            command=lambda x, y='force2': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.force2.pack()

        # 3ª acción

        self.setvar('action3', '')
        self.accion3 = ttk.Combobox(
            self.master,
            values=self.combosOptions,
            state='readonly',
        )
        self.accion3.bind(
            '<<ComboboxSelected>>',
            lambda event, entry=self.accion3: self.update_value(entry.get(), 'action3'))
        self.accion3.grid(row=4, column=0, sticky=constants.W)

        angle3Frame = ttk.Frame(self.master)
        angle3Frame.grid(row=4, column=1, sticky=constants.W, padx=10)
        self.setvar('angle3', 0)

        angle3Label = ttk.Label(angle3Frame, textvariable='angle3', anchor=constants.CENTER)
        angle3Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.angle3 = ttk.Scale(
            angle3Frame,
            from_=0,
            to=120,
            command=lambda x, y='angle3': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.angle3.pack()

        force3Frame = ttk.Frame(self.master)
        force3Frame.grid(row=4, column=2, sticky=constants.W, padx=10)
        self.setvar('force3', 0)

        force3Label = ttk.Label(force3Frame, textvariable='force3', anchor=constants.CENTER)
        force3Label.pack(side=constants.TOP, fill=constants.X, pady=0)

        self.force3 = ttk.Scale(
            force3Frame,
            from_=1,
            to=10,
            command=lambda x, y='force3': self.update_value(x, y),
            state=constants.DISABLED
        )
        self.force3.pack()

        # Este botón copia el comando al portapapeles
        self.btnCopy = ttk.Button(
            master=master,
            text="Copiar",
            command=self.toClipboard,
            bootstyle=constants.SUCCESS,
            width=6,
            state=constants.DISABLED
        )
        self.btnCopy.grid(row=5, column=0, pady=10, sticky=constants.W)

        self.commandText = ttk.Label(master, textvariable='command', anchor=constants.W)
        self.commandText.grid(row=5, column=1, columnspan=2, pady=10, sticky=constants.W)
        self.setvar('command', '')

        self.anglesWidgets = [self.angle1, self.angle2, self.angle3]
        self.shotForceWidgets = [self.force1, self.force2, self.force3]

    def update_value(self, value, name):
        index = int(name[-1]) - 1

        if name.startswith('action'):
            command = self.optsActions[value]
            self.setvar(name, command)

            if command == 's':
                self.anglesWidgets[index].configure(state=constants.NORMAL)
                self.shotForceWidgets[index].configure(state=constants.NORMAL)
            else:
                self.anglesWidgets[index].configure(state=constants.DISABLED)
                self.shotForceWidgets[index].configure(state=constants.DISABLED)

        else:
            self.setvar(name, f'{float(value):.0f}')

        self.genCommand()

    def genCommand(self):
        command = '!turn '
        totalActions = 0
        self.btnCopy.configure(state=constants.DISABLED)

        for i in range(0, 3):
            action = self.master.getvar(f'action{i+1}')
            angle = self.master.getvar(f'angle{i+1}')
            force = self.master.getvar(f'force{i+1}')

            command += self.master.getvar(f'action{i+1}')
            if action:
                totalActions += 1

            if action == 's':
                command += f':{angle}:{force}'

            if i < 2:
                command += ';'

        if totalActions == 3:
            self.btnCopy.configure(state=constants.NORMAL)

        self.setvar('command', command)

    def toClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.getvar('command'))


if __name__ == '__main__':
    app = ttk.Window(
        themename='superhero',
        title='Tu turno, Gusano',
        iconphoto='icon.png',
        resizable=[False, False]
    )
    TurnoGusano(app)
    app.mainloop()
