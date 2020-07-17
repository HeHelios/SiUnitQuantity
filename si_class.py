import numpy as np
from numpy import linalg

SI_BASIC_UNITS = {"mass": "kg", "length": "m", "time": "s", "current": "A", "temperature": "K", "amount of substance": "mol"}


class SiUnitQuantity:
    FORMAT = ["kg", "J", "s", "A", "K", "mol"]
    
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
    
    
    BASIC_PREFIX = {"Y" : 1e24, "Z": 1e21, "E": 1e18, "P": 1e15, "T": 1e12, "G": 1e9, \
                    "M": 1e6, "k": 1e3, "c": 1e-2, "m": 1e-3, "u": 1e-6, "n": 1e-9, \
                    "p": 1e-12, "f": 1e-15, "a": 1e-18, "z": 1e-21, "y":1e-24}
    
    
    def __init__(self, magnitude = 1.0, exponents = {"mass": 0, "length": 0, "time": 0, "current": 0, "temperature": 0}):
        self.exponents = exponents
        for unit in SI_BASIC_UNITS:
            if unit not in self.exponents:
                self.exponents[unit] = 0
        self.magnitude = magnitude

    def is_unitless(self):
        return all(val == 0 for val in self.exponents.values())

    def match_units(self, other):
        return self.exponents == other.exponents


    def __str__(self):
        
        units_format = SiUnitQuantity.FORMAT
        result = ''
        
        numerator = ''
        denominator = ''        
        numerator_num = 0
        denominator_num = 0
        
        if self.is_unitless():
            return result[:-1]
        
        #Linear algebra
        if len(units_format) != 6:
            raise ValueError("Full basis of output units should be given.")
        
        basic = np.array([self.exponents[key] for key in SI_BASIC_UNITS])
        
        ALL_UNITS = SiUnitQuantity.SI_BASIC_UNITS_DESCRIPT.copy()
        ALL_UNITS.update(SiUnitQuantity.SI_DEPENDENT_UNITS_DESCRIPT)
        ALL_UNITS.update(SiUnitQuantity.USER_UNITS_DESCRIPT)
        
        transform_matrix = [[0]*6 for i in range(6)]        
        
        j = 0
        for unit in units_format:
            i = 0
            for key in SI_BASIC_UNITS:
                basic_unit = SI_BASIC_UNITS[key]
                transform_matrix[i][j] = ALL_UNITS[unit][basic_unit]
                i += 1
            j += 1
        
        transform_matrix = np.array(transform_matrix)
        
        if linalg.det(transform_matrix) == 0:
            raise ValueError("Inrevertible set of units.")
        
        coefs = linalg.solve(transform_matrix, basic)
        coefs = {units_format[i]: coefs[i] for i in range(6)}
        
        #Helper functionfor cool output
        def out_func(unit_exp, name):
            nonlocal numerator, denominator, numerator_num, denominator_num
            
            new_unit_exp = unit_exp
            if unit_exp.is_integer():
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


        for unit in coefs:
            out_func(coefs[unit], unit)

        
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
        
        #calculating a right number
        
        num = self.magnitude
        for unit in coefs:
            num /= (ALL_UNITS[unit]["__val__"]**coefs[unit])
        
        result = str(num) + ' ' + result
        return result


    #arithmetics
    def __add__(self, right):
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return SiUnitQuantity(magnitude = self.magnitude + right)
            else:
                raise TypeError("Unit mismatch in adding SiUnitQuantity and a non-SiUnitQuantity")
        if not self.match_units(right):
            raise TypeError("Unit mismatch in adding two SiUnitQuantities")
        return SiUnitQuantity(magnitude = self.magnitude + right.magnitude, exponents = dict(self.exponents))

    def __radd__(self, right):
        return self + right


    def __sub__(self, right):
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return SiUnitQuantity(magnitude = self.magnitude - right)
            else:
                raise TypeError("Unit mismatch in substructing SiUnitQuantity and a non-SiUnitQuantity")
        if not self.match_units(right):
            raise TypeError("Unit mismatch in substructing two SiUnitQuantities")
        return SiUnitQuantity(magnitude = self.magnitude - right.magnitude, exponents = dict(self.exponents))

    def __rsub__(self, right):
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return SiUnitQuantity(magnitude = right - self.magnitude)
            raise TypeError("Unit mismatch in substructing SiUnitQuantity and a non-SiUnitQuantity")

    
    def __mul__(self, right):
        if not isinstance(right, SiUnitQuantity):
            return SiUnitQuantity(self.magnitude * right, exponents = dict(self.exponents))              
        new_exponents = {key: self.exponents[key] + right.exponents[key] for key in self.exponents.keys()}
        return SiUnitQuantity(self.magnitude * right.magnitude, exponents = new_exponents)

    def __rmul__(self, right):
        return self*right

    def __truediv__(self, right):
        if not isinstance(right, SiUnitQuantity):
            return SiUnitQuantity(self.magnitude / right, exponents = dict(self.exponents))
        new_exponents = {key: self.exponents[key] - right.exponents[key] for key in self.exponents.keys()}
        return SiUnitQuantity(self.magnitude / right.magnitude, exponents = new_exponents)

    def __rtruediv__(self, right):
        if not isinstance(right, SiUnitQuantity):
            new_exponents = {key: -self.exponents[key] for key in self.exponents.keys()}
            return SiUnitQuantity(right/self.magnitude, exponents  = new_exponents)

    def __pow__(self, right):
        if not isinstance(right, SiUnitQuantity):
            new_exponents = {key: self.exponents[key] * right for key in self.exponents.keys()}
            return SiUnitQuantity(magnitude = self.magnitude ** right, exponents = new_exponents)
        elif isinstance(right, SiUnitQuantity) and right.is_unitless():
            new_exponents = {key: self.exponents[key] * right.magnitude for key in self.exponents.keys()}
            return SiUnitQuantity(magnitude = self.magnitude ** right.magnitude, exponents = new_exponents) 
        else:
            raise ValueError('Needs unitless number for a power.')
    
    def __rpow__(self, right):
        if self.is_unitless():
            return right ** self.magnitude
        raise ValueError('Needs unitless number for a power.')
        
    #equalities and inequalities
    def __eq__(self, other):
        if not isinstance(other, SiUnitQuantity):
            if self.is_unitless():
                return self.magnitude == other
            else:
                raise TypeError("Unit mismatch in comparing SiUnitQuantity and a non-SiUnitQuantity")
        if not self.match_units(other):
            raise TypeError("Unit mismatch in comparing two SiUnitQuantities")
        return self.magnitude == other.magnitude

    def __ne__(self, other):
        return not self == other
        
    def __lt__(self, right):  #<
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return self.magnitude < right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude < right.magnitude
        raise ValueError('Quantities with different units cannot be compared')
    

    def __gt__(self, right):  #>
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return self.magnitude > right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude > right.magnitude
        raise ValueError('Quantities with different units cannot be compared')
        
    def __le__(self, right):  #<=
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return self.magnitude <= right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude <= right.magnitude
        raise ValueError('Quantities with different units cannot be compared')            

    def __ge__(self, right):  #>=
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return self.magnitude >= right
            raise ValueError('Quantities with different units cannot be compared.')
        
        if self.match_units(right):
            return self.magnitude >= right.magnitude
        raise ValueError('Quantities with different units cannot be compared')
        
    def __abs__(self):
        return SiUnitQuantity(magnitude = abs(self.magnitude), exponents = self.exponents)
    
    def __int__(self):
        return int(self.magnitude)
    
    def __float__(self):
        return float(self.magnitude)
    
    def __round__(self, digits = 0):
        return SiUnitQuantity(magnitude = round(self.magnitude, digits), exponents = self.exponents)
    
    def int_units(self):    
    #Converts float exponents to int expotnents
        new_exponents = {key : int(self.exponents[key]) for key in self.exponents.keys()}
        return SiUnitQuantity(magnitude = self.magnitude, exponents = new_exponents)

if __name__ == '__main__':
 
    x = SiUnitQuantity(-5, exponents = {"mass": 1, "time": -1})
    print(x)