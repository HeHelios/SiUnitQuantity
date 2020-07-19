class NaturalUnitQuantity:
    
    FORMAT = "MeV"
    BASIC_FORMAT = "eV"
    """
    SI_BASIC_UNITS_DESCRIPT = {"kg": {"__val__":1, "kg": 1, "m": 0, "s": 0, "A": 0, "K": 0, "mol": 0},
                               "m": {"__val__":1, "kg": 0, "m": 1, "s": 0, "A": 0, "K": 0, "mol": 0},
                               "s": {"__val__":1, "kg": 0, "m": 0, "s": 1, "A": 0, "K": 0, "mol": 0},
                               "A": {"__val__":1, "kg": 0, "m": 0, "s": 0, "A": 1, "K": 0, "mol": 0},
                               "K": {"__val__":1, "kg": 0, "m": 0, "s": 0, "A": 0, "K": 1, "mol": 0},
                               "mol": {"__val__":1, "kg": 0, "m": 0, "s": 0, "A": 0, "K": 0, "mol": 1},}
    
    SI_DEPENDENT_UNITS_DESCRIPT = {"Hz": {"__val__":1, "kg": 0, "m": 0, "s": -1, "A": 0, "K": 0, "mol": 0},
                                   "N": {"__val__":1, "kg": 1, "m": 1, "s": -2, "A": 0, "K": 0, "mol": 0},
                                   "J": {"__val__":1, "kg": 1, "m": 2, "s": -2, "A": 0, "K": 0, "mol": 0},
                                   "W": {"__val__":1, "kg": 1, "m": 2, "s": -3, "A": 0, "K": 0, "mol": 0},
                                   "Pa": {"__val__":1, "kg": 1, "m": -1, "s": -2, "A": 0, "K": 0, "mol": 0},
                                   "C": {"__val__":1, "kg": 0, "m": 0, "s": 1, "A": 1, "K": 0, "mol": 0},
                                   "V": {"__val__":1, "kg": 1, "m": 2, "s": -3, "A": -1, "K": 0, "mol": 0},
                                   "F": {"__val__":1, "kg": -1, "m": -2, "s": 4, "A": 2, "K": 0, "mol": 0},
                                   "Ohm": {"__val__":1, "kg": 1, "m": 2, "s": -3, "A": -2, "K": 0, "mol": 0},
                                   "T": {"__val__":1, "kg": 1, "m": 0, "s": -2, "A": -1, "K": 0, "mol": 0},
                                   "H": {"__val__":1, "kg": 1, "m": 2, "s": -2, "A": -2, "K": 0, "mol": 0},
                                   "g": {"__val__":1e-3, "kg": 1, "m": 0, "s": 0, "A": 0, "K": 0, "mol": 0},}
    
    USER_UNITS_DESCRIPT = {"1": {"__val__":1, "kg": 0, "m": 0, "s": 0, "A": 0, "K": 0, "mol": 0},}    
    """
    
    BASIC_PREFIX = {"Y" : 1e24, "Z": 1e21, "E": 1e18, "P": 1e15, "T": 1e12, "G": 1e9, \
                    "M": 1e6, "k": 1e3, "c": 1e-2, "m": 1e-3, "u": 1e-6, "n": 1e-9, \
                    "p": 1e-12, "f": 1e-15, "a": 1e-18, "z": 1e-21, "y":1e-24}
    
    
    def __init__(self, magnitude = 1.0, exp = 0):
        self.exp = exp
        self.magnitude = magnitude

    def is_unitless(self):
        return self.exp == 0

    def match_units(self, other):
        return self.exp == other.exp


    def __str__(self):
        unit_format = NaturalUnitQuantity.FORMAT
        result = ''
        
        numerator = ''
        denominator = ''        
        numerator_num = 0
        denominator_num = 0
        
        num = self.magnitude
        
        prefix = 1
        if (unit_format[0] in NaturalUnitQuantity.BASIC_PREFIX):
            prefix = NaturalUnitQuantity.BASIC_PREFIX[unit_format[0]]
        
        num /= prefix**self.exp
        
        result = str(num) + ' '

        if self.is_unitless():
            return result[:-1]

        #Helper functionfor cool output
        def out_func(unit_exp, name):
            nonlocal numerator, denominator, numerator_num, denominator_num
            
            new_unit_exp = unit_exp
            if (not isinstance(unit_exp, int)) and unit_exp.is_integer():
                new_unit_exp = int(unit_exp)
            
            if new_unit_exp > 0:
                if new_unit_exp == 1:
                    numerator += name + ' * '
                else:
                    numerator += name + '^' + str(new_unit_exp) + ' * '
                numerator_num += 1
            elif new_unit_exp < 0:
                if new_unit_exp == -1:
                    denominator += name + ' * '
                else:
                    denominator += name + '^' + str(-new_unit_exp) + ' * '
                denominator_num += 1

        #building a units string
        out_func(self.exp, unit_format)

        if numerator_num == 0:
            numerator = '1'
        elif numerator_num == 1:
            numerator = numerator[:-3]
            if denominator_num == 0:
                return result + numerator
            
        else:
            numerator = numerator[:-3]
            if denominator_num != 0:
                numerator = '(' + numerator + ')'
            else:
                return result + numerator
            

        if denominator_num == 1:
            denominator = denominator[:-3]
        else:
            denominator = denominator[:-3]
            denominator = '(' + denominator + ')'
            
        result += numerator + '/' + denominator
        
        return result


    #arithmetics
    def __add__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return NaturalUnitQuantity(magnitude = self.magnitude + right)
            else:
                raise TypeError("Unit mismatch in adding NaturalUnitQuantity and a non-NaturalUnitQuantity")
        if not self.match_units(right):
            raise TypeError("Unit mismatch in adding two NaturalUnitQuantities")
        return NaturalUnitQuantity(magnitude = self.magnitude + right.magnitude, exp = self.exp)

    def __radd__(self, right):
        return self + right


    def __sub__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return NaturalUnitQuantity(magnitude = self.magnitude - right)
            else:
                raise TypeError("Unit mismatch in substructing NaturalUnitQuantity and a non-NaturalUnitQuantity")
        if not self.match_units(right):
            raise TypeError("Unit mismatch in substructing two NaturalUnitQuantities")
        return NaturalUnitQuantity(magnitude = self.magnitude - right.magnitude, exp = self.exp)

    def __rsub__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return NaturalUnitQuantity(magnitude = right - self.magnitude)
            raise TypeError("Unit mismatch in substructing NaturalUnitQuantity and a non-NaturalUnitQuantity")

    
    def __mul__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            return NaturalUnitQuantity(self.magnitude * right, exp = self.exp)              
        new_exp = self.exp + right.exp
        return NaturalUnitQuantity(self.magnitude * right.magnitude, exp = new_exp)

    def __rmul__(self, right):
        return self*right

    def __truediv__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            return NaturalUnitQuantity(self.magnitude / right, exp = self.exp)
        new_exp = self.exp - right.exp
        return NaturalUnitQuantity(self.magnitude / right.magnitude, exp = new_exp)

    def __rtruediv__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            return NaturalUnitQuantity(right/self.magnitude, exp  = -self.exp)

    def __pow__(self, right):
        if not isinstance(right, NaturalUnitQuantity):
            new_exp = self.exp * right
            return NaturalUnitQuantity(magnitude = self.magnitude ** right, exp = new_exp)
        elif isinstance(right, NaturalUnitQuantity) and right.is_unitless():
            new_exp = self.exp * right.magnitude
            return NaturalUnitQuantity(magnitude = self.magnitude ** right.magnitude, exp = new_exp) 
        else:
            raise ValueError('Needs unitless number for a power.')
    
    def __rpow__(self, right):
        if self.is_unitless():
            return right ** self.magnitude
        raise ValueError('Needs unitless number for a power.')
        
    #equalities and inequalities
    def __eq__(self, other):
        if not isinstance(other, NaturalUnitQuantity):
            if self.is_unitless():
                return self.magnitude == other
            else:
                raise TypeError("Unit mismatch in comparing NaturalUnitQuantity and a non-NaturalUnitQuantity")
        if not self.match_units(other):
            raise TypeError("Unit mismatch in comparing two NaturalUnitQuantities")
        return self.magnitude == other.magnitude

    def __ne__(self, other):
        return not self == other
        
    def __lt__(self, right):  #<
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return self.magnitude < right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude < right.magnitude
        raise ValueError('Quantities with different units cannot be compared')
    

    def __gt__(self, right):  #>
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return self.magnitude > right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude > right.magnitude
        raise ValueError('Quantities with different units cannot be compared')
        
    def __le__(self, right):  #<=
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return self.magnitude <= right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude <= right.magnitude
        raise ValueError('Quantities with different units cannot be compared')            

    def __ge__(self, right):  #>=
        if not isinstance(right, NaturalUnitQuantity):
            if self.is_unitless():
                return self.magnitude >= right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude >= right.magnitude
        raise ValueError('Quantities with different units cannot be compared')
        
    def __abs__(self):
        return NaturalUnitQuantity(magnitude = abs(self.magnitude), exp = self.exp)
    
    def __int__(self):
        return int(self.magnitude)
    
    def __float__(self):
        return float(self.magnitude)
    
    def __round__(self, digits = 0):
        return NaturalUnitQuantity(magnitude = round(self.magnitude, digits), exp = self.exp)
    
    def int_units(self):    
    #Converts float exponents to int expotnents
        new_exp = int(self.exp)
        return NaturalUnitQuantity(magnitude = self.magnitude, exp = new_exp)

if __name__ == '__main__':
 
    x = NaturalUnitQuantity(-4.3e6, exp = 0)
    print(x)