# ---------------------------- Libraries ------------------------------- #
from user_input_validator import UserInputValidator
from calculator import Calculator

# ---------------------------- Classes ------------------------------- #
class EllipticCurvePointFinder:

    # Constructor
    def __init__(self):
        self.calculator = Calculator()


    # Methods
    def check_polynomial(self, a: int, b: int, mod: int) -> bool:
        """
        Check if the polynomial is valid.
        :param int a: The 'a' coefficient of the polynomial.
        :param int b: The 'b' coefficient of the polynomial.
        :param int mod: The finite field modulo for the calculation.
        :return: True if the polynomial is valid, False otherwise.
        """

        a = self.calculator.montgomery_ladder(a, 3, mod)
        b = self.calculator.montgomery_ladder(b, 2, mod)
        result = ((4 * a) + (27 * b)) % mod

        if result == 0:
            return False
        else:
            return True

    def find_non_square_number(self, mod: int) -> int:
        """
        Find a non-square number in the finite field modulo.
        :param int mod: The finite field modulo for the calculation.
        :return: A non-square number in the finite field modulo.
        """

        x = 1
        h = int((mod - 1) / 2)

        while x < mod:
            if self.calculator.montgomery_ladder(x, h, mod)  == 1:
                x += 1

            else:
                return x

    def find_square_roots(self, square: int, non_square: int, mod: int) -> tuple:
        """
        Find the square roots of a given number in the finite field modulo.
        :param int square: The number to find the square roots of.
        :param int non_square: A non-square number in the finite field modulo.
        :param int mod: The finite field modulo for the calculation.
        :return: The square roots of the given number in the finite field modulo.
        """

        if (mod + 1) % 4 == 0:
            exponent = int((mod + 1) / 4)
            sqr_1 = self.calculator.montgomery_ladder(square, exponent, mod)
            sqr_2 = mod - sqr_1

            return sqr_1, sqr_2

        else:
            l_and_t = self.find_l_t(mod)
            n = 0
            i = 0

            while i != l_and_t[0]:
                exponent = self.calculator.montgomery_ladder(non_square,(l_and_t[0] - 1), mod)
                c = self.calculator.montgomery_ladder(square, exponent, mod) * self.calculator.montgomery_ladder(non_square, n, mod) % mod

                if c == 1:
                    n = int(n / 2)

                else:
                    n = int(n / 2 + (mod - 1) / 4)

                i += 1

            sqr_1 = self.calculator.montgomery_ladder(square, int((l_and_t[1] + 1) / 2), mod) * self.calculator.montgomery_ladder(non_square, n, mod) % mod
            sqr_2 = mod - sqr_1

            return sqr_1, sqr_2

    @staticmethod
    def find_l_t(p: int) -> tuple:
        """
        Find two numbers l and t such that (p-1)/2 = 2^l * t with l >= 1 and t odd.
        :param int p: The number to find l and t for.
        :return: The numbers l and t.
        """

        n = (p - 1) // 2
        l = 0
        while n % 2 == 0:
            n = n // 2
            l += 1
        t = n
        return l, t

    def check_for_square(self, a: int, mod: int):
        """
        Check if a number is a square in the finite field modulo.
        :param int a: The number to check.
        :param int mod: The finite field modulo for the calculation.
        :return: True if the number is a square, False otherwise.
        """

        b = int((mod - 1) / 2)

        if self.calculator.montgomery_ladder(a, b, mod) == 1:
            return True

        else:
            return False

    def find_point(self, a: int, b: int, mod: int) -> list or None:
        """
        Find a point on the elliptic curve defined by the given polynomial and finite field modulo.
        :param int a: The 'a' coefficient of the polynomial.
        :param int b: The 'b' coefficient of the polynomial.
        :param int mod: The finite field modulo for the calculation.
        :return: A point on the elliptic curve, or None if no point is found.
        """

        if self.check_polynomial(a, b, mod):
            print("Valid polynomial.")

            for x in range(mod - 1):

                result = (self.calculator.montgomery_ladder(x, 3, mod) + a * x + b) % mod

                if result == self.check_for_square(result, mod):

                    non_square = self.find_non_square_number(mod)
                    square_roots = self.find_square_roots(result, non_square, mod)
                    points = [(x, square_roots[0]), (x, square_roots[1])]

                    print(f"Square number: {result}")
                    print(f"Non-square number: {non_square}")
                    print(f"Square roots: {square_roots}")
                    print()
                    print("-" * 50)
                    print()
                    print(f"The points on the elliptic curve are: {points}")

                    return points

        else:
            print("Invalid polynomial.")
            return None


# ---------------------------- Constants ------------------------------- #
LOGO = """
 _____ _ _ _       _   _         ____                     
| ____| | (_)_ __ | |_(_) ___   / ___|   _ _ ____   _____ 
|  _| | | | | '_ \| __| |/ __| | |  | | | | '__\ \ / / _ \\
| |___| | | | |_) | |_| | (__  | |__| |_| | |   \ V /  __/
|_____|_|_|_| .__/ \__|_|\___|  \____\__,_|_|    \_/ \___|
 ____       |_|     _     _____ _           _             
|  _ \ ___ (_)_ __ | |_  |  ___(_)_ __   __| | ___ _ __   
| |_) / _ \| | '_ \| __| | |_  | | '_ \ / _` |/ _ \ '__|  
|  __/ (_) | | | | | |_  |  _| | | | | | (_| |  __/ |     
|_|   \___/|_|_| |_|\__| |_|   |_|_| |_|\__,_|\___|_|     
"""

# ---------------------------- Functions ------------------------------- #

def main():
    """
    Main function of the program.
    :return: None
    """

    # Header
    print(LOGO)
    print()
    print("The formula of the elliptic curve is: y² = x³ + ax + b")
    print("The elliptic curve is defined over the finite field modulo.")
    print()

    # Variables
    uiv = UserInputValidator()
    ecpf= EllipticCurvePointFinder()

    # Body
    a = uiv.validate_int_input("Enter the 'a' coefficient of the polynomial: ")
    b = uiv.validate_int_input("Enter the 'b' coefficient of the polynomial: ")
    mod = uiv.validate_int_input("Enter the finite field modulo: ")
    print()

    points = ecpf.find_point(a, b, mod)


# ------------------------------ Main ---------------------------------- #

if __name__ == "__main__":
    main()

