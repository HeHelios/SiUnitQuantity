class Constants:
    SI_BASIC_UNITS = {"mass": "kg", "length": "m", "time": "s", "current": "A", "temperature": "K"}

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

    def __eq__(self, other):
        if not isinstance(other, SiUnitQuantity):
            if self.is_unitless():
                return self.magnitude == right
            else:
                raise TypeError("Unit mismatch in comparing SiUnitQuantity and a non-SiUnitQuantity")
        if not self.match_units(right):
            raise TypeError("Unit mismatch in comparing two SiUnitQuantities")
        return self.magnitude == right.magnitude

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
                raise TypeError("Unit mismatch in adding SiUnitQuantity and a non-SiUnitQuantity")
        if not self.match_units(right):
            raise TypeError("Unit mismatch in adding two SiUnitQuantities")
        return SiUnitQuantity(magnitude = self.magnitude - right.magnitude, exponents = dict(self.exponents))

    def __rsub__(self, right):
        return right - self
    
    def __mul__(self, right):
        return SiUnitQuantity(self.magnitude * right.magnitude, exponents = {unit: self.exponents[unit] + right.exponents[unit] for unit in self.exponents})

    def __truediv__(self, right):
        return SiUnitQuantity(self.magnitude / right.magnitude, exponents = {unit: self.exponents[unit] - right.exponents[unit] for unit in self.exponents})

    def __rtruediv__(self, right):
        return right / self

    def __pow__(self, right):
        if not isinstance(right, (int, float, SiUnitQuantity)):
            raise ValueError('Only number can be a power.')
        if isinstance(right, (int, float)):
            return SiUnitQuantity(magnitude = self.magnitude ** right, exponents = {unit: self.exponents[unit] * right for unit in self.exponents})
        elif isinstance(right, SiUnitQuantity) and right.is_unitless():
            return SiUnitQuantity(magnitude = self.magnitude ** right.magnitude, exponents = {unit: self.exponents[unit] * right.magnitude for unit in self.exponents}) 
        else:
            raise ValueError('Needs unitless number for a power.')
    
    def __rpow__(self, right):
        if self.is_unitless():
            return right ** self.magnitude
        else:
            raise ValueError('Needs unitless number for a power.')
           

if __name__ == '__main__':
    x = 2
    #x = SiUnitQuantity(5, len_exp = 1, time_exp = -1)
    y = SiUnitQuantity(2)
    x = x ** y
    print(x)
