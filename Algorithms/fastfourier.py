import math
import cmath
'''
This file handles the logic of a Fast Fourier transform, including the handling of complex numbers, algebraic expressions etc.

The FFT algorithm converts a function from polynomial, to sample points in O(nlogn) time
'''
import copy
class AlgebraicExpression:
    def __init__(self, coefficients = None):
        self.degree = len(coefficients) - 1 if coefficients != None else 0
        if coefficients is None:
            self.coefficients = [0]
        else:
            self.coefficients = coefficients

    def __str__(self):
        string = ''
        for i in range(self.degree, -1, -1):
            string += f"{self.coefficients[i]}x^{i} "
        return string
    def __add__(self, other):
        # Pad to max degree
        if isinstance(other, (int, float)):
            alg = AlgebraicExpression()
            alg.coefficients[0] = other
            other = alg
        degree = max(self.degree, other.degree)
        alg1 = self.pad(degree)
        alg2 = other.pad(degree)
        new_alg = Algebraic_Expression().pad(degree)
        for i in range(degree):
            new_alg.coefficients[i] = alg1.coefficients[i] + alg2.coefficients[i]
        return new_alg


    def scal_mult(self, scal):
        new_alg = copy.deepcopy(self)
        degree = new_alg.degree
        for i in range(degree):
            new_alg.coefficients[i] *= degree
        return new_alg
    def pad(self, degree):
        # Pads the Expression up to this degree
        alg = copy.deepcopy(self)
        amount_to_pad = max(degree - self.degree)
        for i in range(amount_to_pad):
            alg.coefficients += [0]
        return alg
class NaiveFastFourier():
    # Still O(N^2), but follows the divide and conquer paradigm of Fast Fourier Transforms
    def __init__(self, polynomial1, polynomial2):
        self.polynomial1 = polynomial1
        self.polynomial2 = polynomial2

        self.coefficients1 = self.polynomial1.coefficients
        self.coefficients2 = self.polynomial2.coefficients

    def recurse(self, x, coefficients, num_coef):
        # Num Coef exists to eliminate the need for len(), which is O(n)
        if num_coef == 1:
            return coefficients[0]
        # Extract Even and Odd Terms
        even_terms = []
        odd_terms = []
        num_even = 0
        num_odd = 0
        for i in range(0, num_coef):
            if i % 2 == 0:
                even_terms += [coefficients[i]]
                num_even += 1
            else:
                odd_terms += [coefficients[i]]
                num_odd += 1
        # Recurse
        A_even = self.recurse(x ** 2, even_terms, num_even)
        A_odd = self.recurse(x ** 2, odd_terms, num_odd) * x
        return A_even + A_odd
    def solve(self, x):
        # Evaluates The Polynomial at a point(simply use the function more times for more evals)
        result1 = self.recurse(x, self.coefficients1, self.polynomial1.degree + 1)
        result2 = self.recurse(x, self.coefficients2, self.polynomial2.degree + 1)
        # multiply to get a sample point on the new function
        return (x, result1 * result2)
class FastFourier():
    # Uses the N roots of Unity to quickly compute the fast Fourier Transform in O(NLogN)
    # Repeated Computation is skipped in the recursion, so no need for DP + Memoization
    def __init__(self, polynomial1, polynomial2):
        self.polynomial1 = polynomial1
        self.polynomial2 = polynomial2

        self.coefficients1 = self.polynomial1.coefficients
        self.coefficients2 = self.polynomial2.coefficients
    def recurse(self, coefficients, num_coefs):

        if num_coefs == 1:
            return [coefficients[0]]
        assert num_coefs % 2 == 0, "Needs to be an even number of terms"
        # split into odd and Even
        even_terms = []
        odd_terms = []
        num_terms = 0
        for i in range(0, num_coefs, 2):
            even_terms += [coefficients[i]]
            odd_terms += [coefficients[i + 1]]
            num_terms += 1
        A_even = self.recurse(even_terms, num_terms)
        A_odd = self.recurse(odd_terms, num_terms)
        odd_variant = []
        even_variant = []
        for i in range(0, num_terms):
            exponent = ((2 * cmath.pi) / (2 * num_terms))  * i
            numb = cmath.exp(complex(0, exponent))
            x = round(numb.real, 3)
            y = round(numb.imag, 3) # reduce floating point instability
            x = complex(x, y)
            even_variant += [A_even[i] + x * A_odd[i]]
            odd_variant += [A_even[i] - x * A_odd[i]]
        return even_variant + odd_variant
    def solve(self):
        # Pad to nearest 2 * 2
        max_degree = max(self.polynomial1.degree, self.polynomial2.degree)
        max_degree = ((max_degree + 1) * 2 // 2)
        # Pad coefficients
        exp = 2 ** max_degree
        padded = [0] * exp
        padded2 = [0] * exp
        padded[exp - (self.polynomial1.degree + 1):] = self.polynomial1.coefficients
        padded2[exp - (self.polynomial2.degree + 1):] = self.polynomial2.coefficients
        # Evaluate
        points = self.recurse(padded, exp)
        points2 = self.recurse(padded2, exp)
        # Hadamard Product
        hadamard = []
        for idx in range(2 ** max_degree):
            val = points[idx] * points2[idx]
            if isinstance(val, complex):
                x = round(val.real, 3)
                y = round(val.imag, 3)
                val = complex(x, y)
            else:
                val = round(val, 3)
            hadamard.append(val)
        return hadamard
class InverseFastFourier():
    def __init__(self, points):
        self.points = points
        self.dim = len(self.points)
    def recurse(self, coefficients, num_coefs):
        if num_coefs == 1:
            return [coefficients[0]]
        # Split into Even and Odd
        assert num_coefs % 2 == 0
        even_coefs = []
        odd_coefs = []
        num_terms = 0
        for idx in range(0, num_coefs):
            if idx % 2 == 0:
                even_coefs += [coefficients[idx]]
                num_terms += 1
            else:
                odd_coefs += [coefficients[idx]]
        A_even= self.recurse(even_coefs, num_terms)
        A_odd = self.recurse(odd_coefs, num_terms)
        even_vals = []
        odd_vals = []
        for idx in range(num_terms):
            x = complex(0, (-1 * cmath.pi / num_terms) * idx) # Complex Conjugate
            exp = cmath.exp(x)
            # Round
            x = round(exp.real, 3)
            y = round(exp.imag, 3)

            x = complex(x, y)
            even_vals += [A_even[idx] + x * A_odd[idx]]
            odd_vals += [A_even[idx] - x * A_odd[idx]]
        mult = even_vals + odd_vals

        for i in range(num_coefs):
            mult[i] /= 2
            # Round
            val = mult[i]
            if isinstance(val, complex):
                x = round(val.real, 1)
                y = round(val.imag, 1)
                val = complex(x, y) # can't have an imaginary here anyways.
            else:
                val = round(val, 1)
            mult[i] = val
        return mult
    def solve(self):
        fourier = self.recurse(self.points, self.dim)
        # create new polynomial
        length = len(fourier)
        terms = []
        for i in range(length):
            if fourier[i] != 0:
                # first term
                terms = fourier[i:]
                break
        dim = len(terms)
        algebraic_expression = AlgebraicExpression(coefficients = terms)
        return algebraic_expression


class Solution():
    def __init__(self, coef1, coef2):
        self.coef1 =coef1
        self.coef2 = coef2
    def solve(self):
        function1 = AlgebraicExpression(coefficients = self.coef1)
        function2 = AlgebraicExpression(coefficients = self.coef2)
        solver = FastFourier(function1, function2)
        points = solver.solve()
        solver = InverseFastFourier(points)
        alg = solver.solve()
        return alg
def main():
    eq1 =[3, 2, 1, 1]
    eq2 = [1, 1]
    solver = Solution(eq1, eq2)
    algebraic_exp = solver.solve()
    print(algebraic_exp)
if __name__ == '__main__':
    main()
# Errors in Computation. I suspect it's in IFFT