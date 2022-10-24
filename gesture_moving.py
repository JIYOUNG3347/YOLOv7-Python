import math

class Moving():
    def __init__(self):
        self.count = 0
        self.p_x = 0
        self.p_y = 0

    def distance(self, c_x, c_y):
        c = math.sqrt(math.pow(self.p_x - c_x, 2) + math.pow(self.p_y - c_y, 2))
        return c

    def moving(self, position_x, position_y):
        c = Moving.distance(self, position_x, position_y)
        if((c > 5) and (self.count < 20)):
            self.count += 1
            # print("past: ", self.p_x, self.p_y)
            # print("current: ", position_x, position_y)
            self.p_x = position_x
            self.p_y = position_y

        else:
            self.count = 0

        return self.count
