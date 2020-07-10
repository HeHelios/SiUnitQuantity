from math import pi
from si_class import SiUnitQuantity


class Units:
    #For user guide
    SI_BASIC_UNITS = {"mass": "kg", "length": "m", "time": "s", "current": "A", "temperature": "K", "amount of substance": "mol"}
    
    SI_DEPENDENT_UNITS = {"frequency": "Hz", "Force": "N", "energy": "J", "power": "W", "pressure": "Pa", \
                          "charge": "C", "voltage": "V", "capacitance": "F", "resistance": "Ohm", \
                          "Magnetic field": "T", "inductance": "H", }
    
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
    
    #For internal code
    _SI_BASIC_UNITS = {"kg": kg, "m": m, "s": s, "A": A, "K": K, "mol": mol}
    
    _SI_DEPENDENT_UNITS = {"Hz": Hz, "N": N, "J": J, "W": W, "Pa": Pa, \
                          "C": C, "V": V, "F": F, "Ohm": Ohm, \
                          "T": T, "H": H, }
    
    BASIC_PREFIX = {}
    
    USER_UNITS = {"1": SiUnitQuantity(1), }
    
    ALL_UNITS = _SI_BASIC_UNITS.copy() 
    ALL_UNITS.update(_SI_DEPENDENT_UNITS)
    ALL_UNITS.update(USER_UNITS)
    
class Constants:
    
    kg = Units.kg
    m = Units.m
    s = Units.s
    K = Units.K
    A = Units.A
    mol = Units.mol
    
    J = Units.J
    N = Units.N
    W = Units.W
    F = Units.F
    C = Units.C
    
    
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
    
    


def new(unit):
    
    def parser(string):
        #processes the string to meaningfull elements list
        result = ["",]
        L = len(string)
        if L == 0:
            raise ValueError("Can not convert empty string")
        
        for i in range(L):
            if string[i] == " ":
                if len(result) == 1:
                    result += ["",]
                continue
            if string[i] not in SPECIAL:
                result[-1] += string[i]
            if string[i] in SPECIAL:
                if result[-1] == "":
                    result = result[:-1]
                result += [string[i], ""]
                
        if result[-1] == "":
            result = result[:-1]
            
        first = result[0]
        
        if len(result) == 1:
            return result
        
        try:
            result = [float(first), ] + ["*", ] + result[1:]
        except:
            for i in range(len(first)-1, -1, -1):
                if first[i].isalpha():
                    before = first[:i]
                    after = first[i:]
                    result = [before, "*", after] + result[1:]
                    break
        
        if result[1] in {"(", ")"}:
            result = [result[0], ] + ["*", ] + result[1:]
        return result
    
    
    def calculator(L, first = True):
        #Computes the final value from the list of elements
        result = SiUnitQuantity(1)
        if first:
            result = SiUnitQuantity(L[0])
            L = L[1:]

        n = 1
        while n != 0:
            n = 0
            m = 0
            for i in range(len(L)):
                if isinstance(L[i], str) and L[i] == '(':
                    if n == 0:
                        start = i
                    n += 1
                if isinstance(L[i], str) and L[i] == ')':
                    m += 1
                    if m == n:
                        finish = i
                        break
            if n != 0:
                parentheses_value = calculator(["*", ] + L[start+1 : finish], first = False)
                L = L[:start] + [parentheses_value, ] + L[finish+1:]
                
        while len(L) != 0:
            if isinstance(L[-1], SiUnitQuantity):
                x = L[-1]
            if isinstance(L[-1], str) and L[-1] == "*":
                result *= x
            if isinstance(L[-1], str) and L[-1] == "/":
                result /= x
            L = L[:-1]
        return result
    
    
    SPECIAL = {"(", ")", "*", "/"}

    elems = parser(unit)
    elems[0] = float(elems[0])
    
    if len(elems) == 1:
        return SiUnitQuantity(elems[0])
    
    for i in range(1, len(elems)):
        if elems[i] in Units.ALL_UNITS:
            elems[i] = Units.ALL_UNITS[elems[i]]
        elif elems[i] in SPECIAL:
            pass
        else:
            raise ValueError("String can not be converted to SI object: wrong format.")

    return calculator(elems)
 
    
    
if __name__ == '__main__':
 
    x = SiUnitQuantity(-5, exponents = {"length": 1, "time": -1})
    y = SiUnitQuantity(2.0)

    print(new("1.5 kg * m / s"))