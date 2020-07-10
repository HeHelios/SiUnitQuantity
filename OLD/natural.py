from math import pi

class Units:
    #Basic
    kg = SiUnitQuantity(magnitude = 1, exponents = {"mass": 1})
    m = SiUnitQuantity(magnitude = 1, exponents = {"length": 1})
    s = SiUnitQuantity(magnitude = 1, exponents = {"time": 1})
    A = SiUnitQuantity(magnitude = 1, exponents = {"current": 1})
    K = SiUnitQuantity(magnitude = 1, exponents = {"temperature": 1})
    mol = SiUnitQuantity(magnitude = 1, exponents = {"amount of substance": 1})
    
    #Dependent
    Hz = 1/s
    N = kg * m / (s**2)
    J = N * m
    W = J / s
    Pa = N / (m**2)
    C = A * s
    V = J / C
    F = C / V
    Ohm = V / A
    T = V * s / (m**2)
    H = Ohm * s


class Constants:
    
    #For user guide
    SI_BASIC_UNITS = {"mass": "kg", "length": "m", "time": "s", "current": "A", "temperature": "K", "amount of substance": "mol"}
    
    SI_DEPENDENT_UNITS = {"frequency": "Hz", "Force": "N", "energy": "J", "power": "W", "pressure": "Pa", \
                          "charge": "C", "voltage": "V", "capacitance": "F", "resistance": "Ohm", \
                          "Magnetic field": "T", "inductance": "H", }

    #For internal code
    __SI_BASIC_UNITS = {"kg": Units.kg, "m": Units.m, "s": Units.s, "A": Units.A, "K": Units.K, "mol": Units.mol}
    
    __SI_DEPENDENT_UNITS = {"Hz": Units.Hz, "N": Units.N, "J": Units.J, "W": Units.W, "Pa": Units.Pa, \
                          "C": Units.C, "V": Units.V, "F": Units.F, "Ohm": Units.Ohm, \
                          "T": Units.T, "H": Units.H, }

    c = 299792458 * m / s                              #speed of ligtht
    h = 6.62607015e-34 * J * s                         #Planck constant
    hbar = h/(2 * pi)                                  #Planck constant
    G = 6.67430e-11 * J * m / (kg**2)                  #gravity constant
    eps0 = 8.8541878128e-12 * F / m                    #vacuum electric permittivity
    mu0 = 1.25663706212e-6 * N / (A**2)                #vacuum magnetic permeability
    e = 1.602176634e-19 * C                            #elementary charge
    Na = 6.02214076e23 / mol                           #Avogadro constant
    kb = 1.380649e-23 * J / K                          #Boltzman constant    
    alph = 7.2973525693e-3                             #fine structure constant
    me = 9.1093837015e-31 * kg                         #electron mass
    mp = 1.67262192369e-27 * kg                        #proton mass
    mn = 1.67492749804e-27 * kg                        #neutron mass
    sigm = 5.670374419e-8 * W / ( (m**2) * (K**4) )    #Stefan-Boltzman constant    
    
    
class SiUnitQuantity:
    def __init__(self, magnitude = 1.0, exponents = {"mass": 0, "length": 0, "time": 0, "current": 0, "temperature": 0}):
        self.exponents = exponents
        for unit in Constants.SI_BASIC_UNITS:
            if unit not in self.exponents:
                self.exponents[unit] = 0
        self.magnitude = magnitude

    def is_unitless(self):
        return all(val == 0 for val in self.exponents.values())

    def match_units(self, other):
        return self.exponents == other.exponents


    def __str__(self):
        result = str(self.magnitude) + ' '
        
        numerator = ''
        denominator = ''        
        numerator_num = 0
        denominator_num = 0
        
        if self.is_unitless():
            return result[:-1]

        #Helper functionfor cool output
        def out_func(unit_exp, name):
            nonlocal numerator, denominator, numerator_num, denominator_num
            
            if unit_exp > 0:
                if unit_exp == 1:
                    numerator += name + ' * '
                else:
                    numerator += name + '^' + str(unit_exp) + ' * '
                numerator_num += 1
            elif unit_exp < 0:
                if unit_exp == -1:
                    denominator += name + ' * '
                else:
                    denominator += name + '^' + str(-unit_exp) + ' * '
                denominator_num += 1

        for unit in Constants.SI_BASIC_UNITS:
            out_func(self.exponents[unit], Constants.SI_BASIC_UNITS[unit])

        
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


def new(unit):
    
    def parser(string):
        SPECIAL = {"(", ")", "*", "/"}
        
        result = ["",]
        L = len(string)
        if L == 0:
            raise ValueError("Can not convert empty string")
        
        for i in range(L):
            if L[i] == " ":
                continue
            if L[i] not in SPECIAL:
                result[-1] += L[i]
            if L[i] in SPECIAL:
                result += [L[i], ""]
                
        if result[-1] == "":
            result = result[:-1]
        return result
    
    elems = parser(unit)
    print(elems)
    
if __name__ == '__main__':
 
    x = SiUnitQuantity(-5, exponents = {"length": 1, "time": -1})
    y = SiUnitQuantity(2.0)

    new("1 J / s")