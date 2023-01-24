import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Интерполирование')
        self.n_string = IntVar()
        self.n_string.set(1)

        self.countEnter = Entry(textvariable=self.n_string)
        self.spawnButton = Button(text='Создать', command=self.spawn)

        self.countEnter.grid(row=1, column=1, padx=10, pady=5)
        self.spawnButton.grid(row=1, column=2, padx=10)

    def spawn(self):
        self.xyLabels = Label(text='Введите координаты точек')
        self.xyLabels.grid(row=1, column=1)

        self.countEnter.grid_remove()
        self.spawnButton.grid_remove()
        self.n = self.n_string.get()

        self.xEnters = []
        self.x = []
        for i in range(self.n):
            self.x.append(IntVar())
            self.xEnters.append(Entry(textvariable=self.x[i], width=17))
            self.xEnters[i].grid(row=i + 2, column=1, pady=5, padx=5)

        self.yEnters = []
        self.y = []
        for i in range(self.n):
            self.y.append(IntVar())
            self.yEnters.append(Entry(textvariable=self.y[i], width=17))
            self.yEnters[i].grid(row=i + 2, column=2, pady=5, padx=5)

        self.methodsLabel = Label(text='Выберите метод')
        self.methodsLabel.grid(row=self.n + 3, column=1)

        self.findLabel = Label(text='Введите точку рассчёта')
        self.findLabel.grid(row=self.n + 3, column=2)

        self.choosenMethod = StringVar()
        self.methodChoose = ttk.Combobox(self, textvariable=self.choosenMethod, width=17)
        self.methods = ['Метод Лагранжа', 'Метод Ньютона', 'Метод кубических сплайнов']
        self.methodChoose['values'] = self.methods
        self.methodChoose.grid(row=self.n + 4, column=1)

        self.findX = IntVar()
        self.findEnter = Entry(textvariable=self.findX, width=17)
        self.findEnter.grid(row=self.n + 4, column=2)

        self.continueButton = Button(text='Продолжить', command=self.interpolate, pady=5)
        self.continueButton.grid(row=self.n + 5, column=2)

    def interpolate(self):
        self.x_arr = []
        self.y_arr = []
        for i in range(self.n):
            self.x_arr.append(self.x[i].get())
            self.y_arr.append(self.y[i].get())
        if self.choosenMethod.get() == self.methods[0]:
            self.answer = StringVar()
            self.answerTitle = Label(text='Ответ:')
            self.AnswerLabel = Label(textvariable=self.answer)
            self.answerTitle.grid(row=self.n+6, column=1)
            self.AnswerLabel.grid(row=self.n + 6, column=2)

            self.answer.set(self.lagrange()**(1/2))

    def lagrange(self):
        def _basis(j):
            p = [(self.findX.get() - self.x_arr[m]) / (self.x_arr[j] - self.x_arr[m]) for m in range(self.n) if m != j]
            return np.prod(p, axis=0) * self.y_arr[j]

        assert len(self.x_arr) != 0 and (
                len(self.x_arr) == len(self.y_arr))
        k = len(self.x_arr)
        return sum(_basis(j) * self.y_arr[j] for j in range(k))


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()