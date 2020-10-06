class SolveKoshiTaskMethods:
    def func(self, y):
        y_new = [0 for i in range(len(y))]
        for f in self.y_funcs:
            exec(f, {'y': y, 'y_new': y_new})
        return y_new

    def runge_kutta(self, y_funcs, dt, steps, y0):
        self.res = [[], [], []]
        self.y_funcs = y_funcs
        for _ in range(steps):
            k_0 = self.func(y0)
            k_1 = self.func([x + k * dt / 2
                             for x, k in zip(y0, k_0)])
            k_2 = self.func([x + k * dt / 2
                             for x, k in zip(y0, k_1)])
            k_3 = self.func([x + k * dt
                             for x, k in zip(y0, k_2)])
            for i in range(3):
                y0[i] += (k_0[i] + 2 * k_1[i] + 2 * k_2[i] + k_3[i]) \
                         * dt / 6.0
                self.res[i].append(y0[i])

    def calc_in_point(self, y_funcs, y):
        y_new = [0, 0, 0]
        for f in y_funcs:
            exec(f, {'y': y, 'y_new': y_new})
        return y_new

    def multiply_scalar_on_const(self, v, a):
        return [k * a for k in v]

    def sum_vectors(self, a, b):
        answ = []
        for i in range(len(a)):
            answ.append(a[i] + b[i])
        return answ

    def explicit_method_euler(self, y_funcs, dt, steps, y0):
        self.res = [y0]
        resp = [[], [], []]
        for k in range(1, steps):
            self.res.append(
                self.sum_vectors(self.res[k - 1],
                                 self.multiply_scalar_on_const(self.calc_in_point(y_funcs, self.res[k - 1]), dt)))
        for point_arr in self.res:
            for i in range(3):
                resp[i].append(point_arr[i])
        self.res = resp
