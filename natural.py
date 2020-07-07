class SiUnitQuantity:
    def __init__(self, mass_exp = 0, len_exp = 0, time_exp = 0, curr_exp = 0, temp_exp = 0, magnitude = 1.):
        self.mass_exp = mass_exp
        self.len_exp = len_exp
        self.time_exp = time_exp
        self.curr_exp = curr_exp
        self.temp_exp = temp_exp
        self.magnitude = magnitude

    def is_unitless(self):
        return self.mass_exp == self.len_exp == self.time_exp == self.curr_exp == self.temp_exp == 0

    def match_units(self, other):
        return self.mass_exp == other_mass_exp and self.len_exp == other.len_exp and self.time_exp == other.time_exp and self.curr_exp == other.curr_exp and self.temp_exp == other.temp_exp

    def __str__(self):
        

    def __add__(self, right):
        if not isinstance(right, SiUnitQuantity):
            if self.is_unitless():
                return SiUnitQuantity(magnitude = self.magnitude + right)
            else:
                raise TypeError("Unit mismatch in adding SiUnitQuantity and a non-SiUnitQuantity")
        if not self.match_units(other):
            raise TypeError("Unit mismatch in adding two SiUnitQuantities")
        return SiUnitQuantity(mass_exp = self.mass_exp, len_exp = self.len_exp, time_exp = self.time_exp, curr_exp = self.curr_exp, temp_exp = self.temp_exp, magnitude = self.magnitude + other.magnitude)

    def __radd__(self, right):
        return self + right

#    def __sub__(self, right):
#        return Sub(self, right)

#    def __mul__(self, right):
#        return Mul(self, right)

 #   def __truediv__(self, right):
 #       return Div(self, right)

  #  def __rtruediv__(self, right):
  #      return Div(right, self)
