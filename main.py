import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np
from scipy import interpolate


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

        # next time using widgets and variables

        self.choosenMethod = StringVar()
        self.findX = IntVar()
        self.answer = StringVar()

        self.y_arr = []
        self.x_arr = []
        self.xEnters = []
        self.x = []

        self.xyLabels = Label(text='Введите координаты точек')
        self.methodsLabel = Label(text='Выберите метод')
        self.findLabel = Label(text='Введите точку рассчёта')
        self.methodChoose = ttk.Combobox(self, textvariable=self.choosenMethod, width=17)
        self.methods = ['Метод Лагранжа', 'Метод Ньютона']
        self.methodChoose['values'] = self.methods
        self.findEnter = Entry(textvariable=self.findX, width=17)
        self.continueButton = Button(text='Продолжить', command=self.interpolate, pady=5)

        self.answerTitle = Label(text='Ответ:')
        self.AnswerLabel = Label(textvariable=self.answer)

        self.n = None
        self.yEnters = None
        self.y = None

    def spawn(self):
        if int(self.countEnter.get()) >= 5:
            self.methods = ['Метод Лагранжа', 'Метод Ньютона', 'Метод кубических сплайнов']
            self.methodChoose['values'] = self.methods

        self.countEnter.grid_remove()
        self.spawnButton.grid_remove()
        self.xyLabels.grid(row=1, column=1)

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

        self.methodsLabel.grid(row=self.n + 3, column=1)
        self.findLabel.grid(row=self.n + 3, column=2)
        self.methodChoose.grid(row=self.n + 4, column=1)
        self.findEnter.grid(row=self.n + 4, column=2)
        self.continueButton.grid(row=self.n + 5, column=2)

    def interpolate(self):
        self.answerTitle.grid(row=self.n + 6, column=1)
        self.AnswerLabel.grid(row=self.n + 6, column=2)

        self.x_arr = []
        self.y_arr = []

        for i in range(self.n):
            self.x_arr.append(self.x[i].get())
            self.y_arr.append(self.y[i].get())

        if self.choosenMethod.get() == self.methods[0]:
            self.answer.set(self.lagrange() ** (1 / 2))

        elif self.choosenMethod.get() == self.methods[1]:
            self.answer.set(self.newton())

        elif self.choosenMethod.get() == self.methods[2]:
            self.answer.set(self.qubicSplines())

    def lagrange(self):
        def _basis(j):
            p = [(self.findX.get() - self.x_arr[m]) / (self.x_arr[j] - self.x_arr[m]) for m in range(self.n) if m != j]
            return np.prod(p, axis=0) * self.y_arr[j]

        assert len(self.x_arr) != 0 and (
                len(self.x_arr) == len(self.y_arr))
        k = len(self.x_arr)
        return sum(_basis(j) * self.y_arr[j] for j in range(k))

    def newton(self):
        def _poly_newton_coefficient():
            m = len(self.x_arr)
            x = np.copy(self.x_arr)
            a = np.copy(self.y_arr)
            for k in range(1, m):
                a[k:m] = (a[k:m] - a[k - 1]) / (x[k:m] - x[k - 1])
            return a

        def newton_polynomial():
            a = _poly_newton_coefficient()
            n = len(self.x_arr) - 1  # Degree of polynomial
            p = a[n]
            for k in range(1, n + 1):
                p = a[n - k] + (self.findX.get() - self.x_arr[n - k]) * p
            return p

        return newton_polynomial()

    def qubicSplines(self):
        tck = interpolate.splrep(self.x_arr, self.y_arr)
        return interpolate.splev(self.findX.get(), tck)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
