class SiUnitQuantity:
    def __init__(self, magnitude = 1.0, mass_exp = 0, len_exp = 0, time_exp = 0, curr_exp = 0, temp_exp = 0):
        self.mass_exp = mass_exp
        self.len_exp = len_exp
        self.time_exp = time_exp
        self.curr_exp = curr_exp
        self.temp_exp = temp_exp
        self.magnitude = magnitude

    def is_unitless(self):
        return self.mass_exp == self.len_exp == self.time_exp == self.curr_exp == self.temp_exp == 0

    def match_units(self, other):
        return self.mass_exp == other.mass_exp and self.len_exp == other.len_exp and self.time_exp == other.time_exp and self.curr_exp == other.curr_exp and self.temp_exp == other.temp_exp


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

        
        out_func(self.mass_exp, 'kg')
        out_func(self.len_exp, 'm')
        out_func(self.time_exp, 's')
        out_func(self.curr_exp, 'A')
        out_func(self.temp_exp, 'K')

        
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
        return SiUnitQuantity(magnitude = self.magnitude + right.magnitude, mass_exp = self.mass_exp, len_exp = self.len_exp, time_exp = self.time_exp, curr_exp = self.curr_exp, temp_exp = self.temp_exp)

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
        return SiUnitQuantity(magnitude = self.magnitude - right.magnitude, mass_exp = self.mass_exp, len_exp = self.len_exp, time_exp = self.time_exp, curr_exp = self.curr_exp, temp_exp = self.temp_exp)

    def __rsub__(self, right):
        return right - self
    
    def __mul__(self, right):
        return SiUnitQuantity(self.magnitude * right.magnitude, mass_exp = self.mass_exp + right.mass_exp, len_exp = self.len_exp + right.len_exp, time_exp = self.time_exp + right.time_exp, curr_exp = self.curr_exp + right.curr_exp, temp_exp = self.temp_exp + right.temp_exp)

    def __truediv__(self, right):
        return SiUnitQuantity(self.magnitude / right.magnitude, mass_exp = self.mass_exp - right.mass_exp, len_exp = self.len_exp - right.len_exp, time_exp = self.time_exp - right.time_exp, curr_exp = self.curr_exp - right.curr_exp, temp_exp = self.temp_exp - right.temp_exp)

    def __rtruediv__(self, right):
        return right / self

    def __pow__(self, right):
        if not isinstance(right, (int, float, SiUnitQuantity)):
            raise ValueError('Only number can be a power.')
        if isinstance(right, (int, float)):
            return SiUnitQuantity(magnitude = self.magnitude ** right, mass_exp = self.mass_exp * right, len_exp = self.len_exp  * right, time_exp = self.time_exp * right, curr_exp = self.curr_exp * right, temp_exp = self.temp_exp * right)
        elif isinstance(right, SiUnitQuantity) and right.is_unitless():
            return SiUnitQuantity(magnitude = self.magnitude ** right.magnitude, mass_exp = self.mass_exp * right.magnitude, len_exp = self.len_exp  * right.magnitude, time_exp = self.time_exp * right.magnitude, curr_exp = self.curr_exp * right.magnitude, temp_exp = self.temp_exp * right.magnitude) 
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