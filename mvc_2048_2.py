class GameView:
    def __init__(self):
        self.map = [
                [2, 0, 0, 2],
                [4, 2, 0, 2],
                [2, 4, 2, 4],
                [0, 4, 0, 4],]
        self.__controller=GameController()
    def move_left(self):
        for line in self.map:
            self.__controller.merge(line)
    def move_right(self):
        for line in self.map:
            line[::-1]=self.__controller.merge(line[::-1])
    def move_up(self):
        self.__controller.square_matrix_transposition(self.map)
        self.move_left()
        self.__controller.square_matrix_transposition(self.map)
    def move_down(self):
        self.__controller.square_matrix_transposition(self.map)
        self.move_right()
        self.__controller.square_matrix_transposition(self.map)
class GameController:
    def zero_to_end(self,list_merge):
        for i in range(len(list_merge)-1,-1,-1):
            if list_merge[i]==0:
                del list_merge[i]
                list_merge.append(0)
    def merge(self,list_merge):
        self.zero_to_end(list_merge)
        for i in range(len(list_merge)-1):
            if list_merge[i]==list_merge[i+1]:
                list_merge[i]+=list_merge[i+1]
                del list_merge[i+1]
                list_merge.append(0)
        return list_merge
    def square_matrix_transposition(self,map):
        for c in range(1, len(map)):  # 1 2 3
            for r in range(c, len(map)):
                map[r][c - 1],map[c - 1][r] = map[c - 1][r],map[r][c - 1]


#入口

view=GameView()
view.move_down()
print(view.map)

