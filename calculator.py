# ---------------------------- Functions ------------------------------- #

class Calculator:

    # Methods
    @staticmethod
    def montgomery_ladder(base: int, exponent: int, modulo: int) -> int:
        """
        Perform the Montgomery Ladder algorithm.
        :param int base: The base number for the calculation.
        :param int exponent: The exponent for the calculation.
        :param int modulo: The modulo for the calculation.
        :return: The result of the Montgomery Ladder calculation.
        """

        x = 1
        y = base % modulo
        exponent_in_bit = bin(exponent)[2:]

        for bit in exponent_in_bit:
            if bit == "1":
                x = (x * y) % modulo
                y = (y ** 2) % modulo
            else:
                y = (x * y) % modulo
                x = (x ** 2) % modulo

        return x
