import matplotlib

matplotlib.use('TkAgg')
from tkinter import *
from solve_koshi_task_methods import SolveKoshiTaskMethods
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D


class Program(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Program")
        self.pack(fill=BOTH, expand=True)
        self.grid()

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        Label(self, text="dt").grid(row=0, column=1, padx=5, pady=5, sticky=W + E + N)
        self.dt = Entry(self)
        self.dt.grid(row=0, column=2, padx=5, pady=5, sticky=W + E + N)
        self.dt.insert(0, "1e-3")

        Label(self, text="steps").grid(row=1, column=1, padx=5, pady=5, sticky=W + E + N)
        self.steps = Entry(self)
        self.steps.grid(row=1, column=2, padx=5, pady=5, sticky=W + E + N)
        self.steps.insert(0, "100000")

        Label(self, text="y0").grid(row=2, column=1, padx=5, pady=5, sticky=W + E + N)
        self.y0 = Entry(self)
        self.y0.grid(row=2, column=2, padx=5, pady=5, sticky=W + E + N)
        self.y0.insert(0, "1,1,1")

        scrollbar = Scrollbar(self)
        scrollbar.grid(row=3, column=3, padx=5, pady=5, sticky=W + E + N)
        self.expressions = Text(self, height=4, width=30)
        self.expressions.grid(row=3, column=2, padx=5, pady=5, sticky=W + E + N)
        scrollbar.config(command=self.expressions.yview)
        self.expressions.config(yscrollcommand=scrollbar.set)

        lorenz = "10 * (-y_1 + y_2)\n30 * y_1 - y_2 - y_1 * y_3\n-8/3 * y_3 + y_1 * y_2"
        self.expressions.insert(END, lorenz)

        self.method = IntVar()
        Radiobutton(self, text="Метод Рунге-Кутта", variable=self.method, value=0).grid(row=4, column=2, padx=5, pady=5,
                                                                                        sticky=W + N)
        Radiobutton(self, text="Метод Эйлера", variable=self.method, value=1).grid(row=5, column=2, padx=5, pady=5,
                                                                                   sticky=W + N)
        self.method.set(0)

        Button(self, text="Start", command=self.appender).grid(row=6, column=2, padx=5, pady=5, sticky=W + E + N)
        Button(self, text="Clear", command=self.clear, width=6).grid(row=7, column=2, padx=5, pady=5, sticky=N + E + W)
        self.fig = plt.figure()
        self.figure_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.figure_canvas.get_tk_widget().grid(row=0, column=0, rowspan=8, padx=5, pady=5, sticky=E + W + S + N)
        self.figure_canvas.draw()
        self.ax = Axes3D(self.fig)

    def appender(self):
        y_funcs = []
        lines = self.expressions.get('1.0', END).splitlines()
        i = 0
        for line in lines:
            for j in range(len(lines)):
                line = str(line).replace("_" + str(j + 1), "[" + str(j) + "]")
            exec('y_funcs.append("y_new[' + str(i) + ']=' + line + '")')
            i += 1
        y0 = [int(s) for s in str(self.y0.get()).split(',')]
        dt = float(self.dt.get())
        steps = int(self.steps.get())
        rk = SolveKoshiTaskMethods()
        if self.method.get() == 0:
            rk.runge_kutta(y_funcs, dt, steps, y0)
        else:
            rk.explicit_method_euler(y_funcs, dt, steps, y0)
        self.plot(rk)

    def plot(self, rk):
        self.ax.clear()
        self.ax.set_xlabel("y1")
        self.ax.set_ylabel("y2")
        self.ax.set_zlabel("y3")
        if self.method.get() == 0:
            self.ax.set_title("Метод Рунге-Кутта")
        else:
            self.ax.set_title("Метод Эйлера")
        self.ax.plot(rk.res[0], rk.res[1], rk.res[2], color="red", lw=1)
        plt.savefig("fig.png")

    def clear(self):
        self.expressions.delete('1.0', END)


if __name__ == "__main__":
    window = Tk()
    window.geometry("1000x500")
    start = Program()
    window.mainloop()
