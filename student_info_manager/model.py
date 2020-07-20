class StudentModel:
    """
        学生数据模型
        对具体学生信息进行抽象
    """

    def __init__(self, name="", age=0, score=0, sid=0):
        self.name = name
        self.age = age
        self.score = score
        # 学生编号：对数据进行唯一标识(全球唯一标识符)
        self.sid = sid  # 自增长1001   1002   1003

    # 对某个数据进行有效性验证
    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.__score = value
