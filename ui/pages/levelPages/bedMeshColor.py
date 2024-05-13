class BedMeshColor:
    def __init__(self):
        self.__color_map = []
        self.__palette_top = (165, 0, 38)
        self.__palette_center = (255, 255, 192)
        self.__palette_bottom = (49, 54, 149)

        self.__color_map.append(self.__palette_bottom)
        for i in range(50):
            self.__color_map.append(
                (int(self.__palette_bottom[0] + (self.__palette_center[0] - self.__palette_bottom[0]) / 50 * (i + 1)),
                 int(self.__palette_bottom[1] + (self.__palette_center[1] - self.__palette_bottom[1]) / 50 * (i + 1)),
                 int(self.__palette_bottom[2] + (self.__palette_center[2] - self.__palette_bottom[2]) / 50 * (i + 1))))
        for i in range(49):
            self.__color_map.append(
                (int(self.__palette_center[0] + (self.__palette_top[0] - self.__palette_center[0]) / 49 * (i + 1)),
                 int(self.__palette_center[1] + (self.__palette_top[1] - self.__palette_center[1]) / 49 * (i + 1)),
                 int(self.__palette_center[2] + (self.__palette_top[2] - self.__palette_center[2]) / 49 * (i + 1))))
        self.__color_map.append(self.__palette_top)

    def get_color_map(self, num: int):
        return {'r': self.__color_map[num][0], 'g': self.__color_map[num][1], 'b': self.__color_map[num][2]}
        # return self.__color_map[num]
