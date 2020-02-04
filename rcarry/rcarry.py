import numpy as np


class RCarry:
    def __init__(self, modulus, shift_parameter, register):
        self.modulus = modulus
        self.shift_param = shift_parameter
        self.register = register
        self.reg_len = len(self.register)

        # initialize the current entry number as the final element of the shift
        # register
        self.entry_index = self.reg_len - 1

    def __calc_pq_elements(self):
        elem_p = self.shift_param + self.entry_index
        elem_q = self.reg_len + self.entry_index

        while elem_p >= self.reg_len:
            elem_p -= self.reg_len
        while elem_q >= self.reg_len:
            elem_q -= self.reg_len

        return elem_p, elem_q

    def __shift_register(self, new_entry):
        self.register[self.entry_index] = new_entry

        if self.entry_index == 0:
            self.entry_index = self.reg_len - 1
        else:
            self.entry_index -= 1

    def generate(self):
        """
        Generate a pseudo random point according to the shift register.
        """
        p, q = self.__calc_pq_elements()
        new_x = self.register[p] - self.register[q]

        while new_x < 0:
            # prevent returning a negative number, should only happen once but
            # maybe there are some very weird cases where this happens multiple
            # times?
            new_x += self.modulus - 1

        if 0 <= new_x <= self.modulus:
            # include the carry bit after taking the modulus
            self.__shift_register(new_x)
            return new_x / self.modulus
        else:
            new_x = new_x % self.modulus - 1
            self.__shift_register(new_x)
            return new_x / self.modulus

    def generate_set(self, n_points):
        """
        Generate a set of n_points.
        :param n_points:
        :return: the set of pseudo random points in an ndarray
        """
        set = np.zeros(n_points)
        for i in range(n_points):
            set[i] = self.generate()

        return set

    def __str__(self):
        return "PRNG RCarry with modulus " + str(
            self.modulus) + ", shift parameter " + str(
            self.shift_param) + ", and register length " + str(
            self.reg_len) + "."
