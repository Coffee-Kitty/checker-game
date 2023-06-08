import copy

import numpy as np

from checkers.src.mode_enumerate import Three_Mode


class CheckerBoard(object):
    board_width_check_nums = 10  # 棋盘宽为10   国跳100
    board_height_check_nums = 10  # 棋盘高为10   国跳100
    start_row = 4  # 每方拥有的棋子所占行数  如国跳100占据4行   国跳64占据3行

    white_color = 0  # 白方为0
    black_color = 1  # 黑方为1
    my_has_win = 1
    enemy_has_win = 2
    none_has_win = 3

    def transition_to_drawboard(self, mode: Three_Mode):
        """
        对于此 0，0 位置
        由于硬性要求  需要更改为  x,y -> x,9-y
        """
        new_checker_board = CheckerBoard(self.board_width_check_nums, self.board_height_check_nums, self.my_color, None)
        new_checker_board.board = np.zeros(shape=(2, self.board_width_check_nums, self.board_height_check_nums), dtype=np.int32)
        if mode == Three_Mode.mode1_i_j_transition:
            for i in range(self.board_width_check_nums):
                for j in range(self.board_height_check_nums):
                    if self.board[self.white_color][i][j] == 1:
                        new_checker_board.board[self.white_color][i][self.board_height_check_nums-1-j] = 1
                    elif self.board[self.white_color][i][j] == 2:
                        new_checker_board.board[self.white_color][i][self.board_height_check_nums-1-j] = 2
                    elif self.board[self.black_color][i][j] == 1:
                        new_checker_board.board[self.black_color][i][self.board_height_check_nums-1-j] = 1
                    elif self.board[self.black_color][i][j] == 2:
                        new_checker_board.board[self.black_color][i][self.board_height_check_nums-1-j] = 2
        elif mode == Three_Mode.mode2_OneToN_transition:
            pass
        elif mode == Three_Mode.mode3_ABC_transition:
            pass
        return new_checker_board


    def __init__(self, width: int, height: int, my_color=white_color, init_board=None):
        """
        初始化棋盘   如果init_board不为None   则给予那时棋盘状态
        """
        self.board_width_check_nums = width
        self.board_height_check_nums = height
        self.my_color = my_color  # 当前轮到my_color走棋

        self.white_color_check = set()
        self.black_color_check = set()
        self.white_boss_check = set()  # 记录所有的王棋
        self.black_boss_check = set()  # 记录所有的王棋

        self.white_color_backward = 1
        self.black_color_backward = -1

        if init_board is not None:
            self.board = init_board
            for i in range(self.board_width_check_nums):
                for j in range(self.board_height_check_nums):
                    if self.board[self.white_color][i][j] == 1:
                        self.white_color_check.add((i, j))
                    elif self.board[self.white_color][i][j] == 2:
                        self.white_boss_check.add((i, j))
                    elif self.board[self.black_color][i][j] == 1:
                        self.black_color_check.add((i, j))
                    elif self.board[self.black_color][i][j] == 2:
                        self.black_boss_check.add((i, j))
        else:
            # 如果没有提供初始棋盘 默认没开始 提供初始board
            self.board = np.zeros(shape=(2, self.board_width_check_nums, self.board_height_check_nums), dtype=np.int32)

            for x in range(self.board_width_check_nums):
                for y in range(0, self.start_row):
                    if (x + y) % 2 == 1:
                        self.board[self.black_color][x][y] = 1
                        self.black_color_check.add((x, y))


            for x in range(self.board_width_check_nums):
                for y in range(self.board_height_check_nums - self.start_row, self.board_height_check_nums):
                    if (x + y) % 2 == 1:
                        self.board[self.white_color][x][y] = 1
                        self.white_color_check.add((x, y))


    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        pass

    def show_board(self) -> None:
        for i in range(self.board_width_check_nums):
            for j in range(self.board_height_check_nums):
                if self.board[self.white_color][i][j] == 1:
                    print(f"white{(i, j)}", end='\t')
                elif self.board[self.black_color][i][j] == 1:
                    print(f"black{(i, j)}", end='\t')
                elif self.board[self.white_color][i][j] == 2:
                    print(f"white-boss{(i, j)}", end='\t')
                elif self.board[self.black_color][i][j] == 2:
                    print(f"black-boss{(i, j)}", end='\t')
                else:
                    print(f"empty{(i, j)}", end='\t')
            print(end='\n')

    def getNextAction(self) -> (bool, [((int, int), [((int, int), bool)])]):
        """
        返回当前局面 my_color可以行棋的位置
        及是否可以吃子
        return           (是否可吃子，[(最终位置),[((吃子位置),吃子是否为王棋)]])
        """
        can_eat, end_list = self.there_can_eat_or_move()
        boss_can_eat, boss_end_list = False, []
        try:
            boss_can_eat, boss_end_list = self.there_boss_can_eat_or_move()
        except Exception as e:
            self.err_log()

        flag = can_eat or boss_can_eat
        if flag:
            # 存在可以吃子的
            eat_list = []
            if can_eat:
                eat_list += end_list
            if boss_can_eat:
                eat_list += boss_end_list

            eat_len = [len(tmp[1]) for tmp in eat_list]
            max_len = max(eat_len)
            return True, [tmp for tmp in eat_list if len(tmp[1]) == max_len]
        else:
            # 都不能吃子
            return False, end_list + boss_end_list

    def there_boss_can_eat_or_move(self) -> (bool, [((int, int), [((int, int), bool)])]):
        """
        :return:  返回当前局面王棋的 如果当前局面有能够吃子的，必须吃子且吃最多
                                否则返回所有可以走的位置
        return           (是否可吃子，[(最终位置),[((吃子位置),吃子是否为王棋)]])
        """
        # 遍历所有王棋集合，然后搜索王棋是否可以走
        un_eat = []
        eat_flag = False
        if_eat = []
        if self.my_color == self.white_color:
            for (x, y) in self.white_boss_check:
                eat_nums, end_list = self.boss_position_can_move(x, y)
                if eat_nums > 0:
                    eat_flag = True
                    if_eat += end_list
                else:
                    un_eat += end_list
        else:
            for (x, y) in self.black_boss_check:
                eat_nums, end_list = self.boss_position_can_move(x, y)
                if eat_nums > 0:
                    eat_flag = True
                    if_eat += end_list
                else:
                    un_eat += end_list
        if eat_flag:
            # 查看每个可以吃子的能力集合
            # 确保在有可以吃最多子的情况下吃最多子
            eat_len = [len(eat[1]) for eat in if_eat]
            max_len = max(eat_len)
            if_eat = [eat for eat in if_eat if len(eat[1]) == max_len]
            return True, if_eat
        return False, un_eat

    def there_can_eat_or_move(self) -> (bool, [((int, int), [((int, int), bool)])]):
        """
        返回当前局面我方普通棋子是否可以吃子,如果当前局面有能够吃子的，必须吃子且吃最多
        否则返回所有可以走的位置
        return           (是否可吃子，[(最终位置),[((吃子位置),吃子是否为王棋)]])
        """
        un_eat = []
        eat_flag = False
        if_eat = []
        if self.my_color == self.white_color:
            for (x, y) in self.white_color_check:
                eat_nums, end_list = self.position_can_move(x, y)
                if eat_nums > 0:
                    eat_flag = True
                    if_eat += end_list
                else:
                    un_eat += end_list
        else:
            for (x, y) in self.black_color_check:
                eat_nums, end_list = self.position_can_move(x, y)
                if eat_nums > 0:
                    eat_flag = True
                    if_eat += end_list
                else:
                    un_eat += end_list
        if eat_flag:
            # 查看每个可以吃子的能力集合
            # 确保在有可以吃最多子的情况下吃最多子
            eat_len = [len(eat[1]) for eat in if_eat]
            max_len = max(eat_len)
            if_eat = [eat for eat in if_eat if len(eat[1]) == max_len]
            return True, if_eat
        return False, un_eat

    def position_can_move(self, x, y) -> (bool, [((int, int), [((int, int), bool)])]):
        """
        检查棋子四个对角线
        先遇到直接为空则直接可以下
        若为my_color肯定不能下
        若为1-my_color则需进一步检查是否能够跳吃

        注意规则    有子可吃必须吃子
                   能多吃子必须吃最多
                   还有如果不是吃子，那么不能后退
         return           (是否可吃子，[(最终位置),[((吃子位置),吃子是否为王棋)]])
        """
        can_eat = None
        can_eat_nums = 0  # 默认一个子也吃不了然后搜索最大的可吃子数
        un_eat = []
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direct in directions:
            new_x = x + direct[0]
            new_y = y + direct[1]
            if self.check_bound(new_x, new_y):
                # 如果新位置有己方棋子  显然该位置不能走
                if self.board[self.my_color][new_x][new_y] != 0:
                    continue

                # 如果新位置有敌方棋子，那么需要检查是否可以吃子
                elif self.board[1 - self.my_color][new_x][new_y] != 0:  # 考虑王棋为2
                    if self.if_can_eat(x, y, x + direct[0] + direct[0], y + direct[1] + direct[1]):
                        # 已经明确可以吃子了, 返回当前位置可以吃最大子
                        can_eat_nums, can_eat = self.check_max_eats(x, y, x + direct[0] + direct[0],
                                                                    y + direct[1] + direct[1])

                # 如果新位置没有任何棋子  显然该位置能走
                else:
                    # 由于除非吃子，否则兵不能后退，所以需要抛弃掉当前位置后退的位置
                    if self.my_color == self.white_color:
                        # 前进后退 仅仅与y 有关  ，所以仅需比较当前颜色后退方向与目前y方向即可
                        if self.white_color_backward != direct[1]:
                            un_eat.append(((new_x, new_y), []))
                    else:
                        if self.black_color_backward != direct[1]:
                            un_eat.append(((new_x, new_y), []))

        if can_eat is not None:
            return can_eat_nums, can_eat
        else:
            return 0, un_eat

    def boss_position_can_move(self, x, y) -> (bool, [((int, int), [((int, int), bool)])]):
        """
        return           (是否可吃子，[(最终位置),[((吃子位置),吃子是否为王棋)]])
        """

        # 1. 检查四个方向，查看是否能够无视距离吃子
        flag = False
        un_eat = []
        end_eat = []
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direct in directions:
            tmp_x, tmp_y = x + direct[0], y + direct[1]
            while self.check_bound(tmp_x, tmp_y) and self.check_bound(tmp_x + direct[0], tmp_y + direct[1]):
                # 1.1如果有己方棋子  显然该方向不能走
                if self.board[self.my_color][tmp_x][tmp_y] != 0:
                    break
                # 1.2 如果新位置有敌方棋子，则需查看是否可以吃子
                elif self.board[1 - self.my_color][tmp_x][tmp_y] != 0:
                    if self.if_can_eat(tmp_x - direct[0], tmp_y - direct[1], tmp_x + direct[0], tmp_y + direct[1]):
                        # 已经明确可以吃子了,返回从当前位置可以吃最大子
                        flag = True
                        can_eat_nums, can_eat = self.check_boss_max_eat(tmp_x - direct[0], tmp_y - direct[1],
                                                                        tmp_x + direct[0], tmp_y + direct[1])
                        # 直接将吃子情况加入集合即可  因为在there_boss_can_move中才进行排序选最大
                        end_eat += can_eat
                    break
                # 1.3如果新位置没有任何棋子  则需要接着检查
                else:
                    un_eat.append(((tmp_x, tmp_y), []))
                    tmp_x, tmp_y = tmp_x + direct[0], tmp_y + direct[1]
            # 发现了边界小bug，为了吃子判断导致无法下到边界
            if self.check_bound(tmp_x, tmp_y) and not self.check_bound(tmp_x + direct[0], tmp_y + direct[1]):
                # 如果边界没有子则可以吃
                if self.board[self.white_color][tmp_x][tmp_y] == 0 and self.board[self.black_color][tmp_x][tmp_y] == 0:
                    un_eat.append(((tmp_x, tmp_y), []))


        if flag:
            return True, end_eat
        # 否则将可以走的地方返回
        return False, un_eat

    def check_bound(self, x, y) -> bool:
        """
        查看棋盘是否越界
        """
        return 0 <= x < self.board_width_check_nums and 0 <= y < self.board_height_check_nums

    def check_max_eats(self, x, y, new_x, new_y) -> (bool, [((int, int), [((int, int), bool)])]):
        """
        调用递归函数计算
        从 x,y 开始 吃子
        返回最大吃子数，及相应list
         return           (是否可吃子，[(最终位置),[((吃子位置),吃子是否为王棋)]])
        """
        if not self.if_can_eat(x, y, new_x, new_y):
            return 0, [((x, y), [])]

        # 否则递归此函数检查 四个方向（不能包含原来方向） 查看能否再次跳吃
        max_eat = 1
        middle_x, middle_y = int((new_x + x) / 2), int((new_y + y) / 2)
        end_list = [((new_x, new_y), [((middle_x, middle_y), self.board[1 - self.my_color][middle_x][middle_y] == 2)])]

        for direct in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            # 不可重复
            if (new_x + direct[0] * 2, new_y + direct[1] * 2) == (x, y):
                continue
            else:
                tem_eat, tem_eaten = self.check_max_eats(new_x, new_y, new_x + direct[0] * 2, new_y + direct[1] * 2)
                if tem_eat > 0:
                    if max_eat < tem_eat + 1:
                        max_eat = tem_eat + 1
                        for eat in tem_eaten:
                            eat[1].append(
                                ((middle_x, middle_y), self.board[1 - self.my_color][middle_x][middle_y] == 2))
                        end_list = tem_eaten
                    elif max_eat == tem_eat + 1:
                        for eat in tem_eaten:
                            eat[1].append(
                                ((middle_x, middle_y), self.board[1 - self.my_color][middle_x][middle_y] == 2))
                        end_list += tem_eaten

        return max_eat, end_list

    def check_boss_max_eat(self, x, y, new_x, new_y) -> (bool, [((int, int), [((int, int), bool)])]):
        """
            需要非常注意，boss跳吃了一个子后，之后的接着跳吃同样无视距离
        """
        if not self.if_can_eat(x, y, new_x, new_y):
            return 0, [((x, y), [])]

        # 否则递归此函数检查 四个方向（不能包含原来方向） 查看能否再次跳吃
        max_eat = 1
        middle_x, middle_y = int((new_x + x) / 2), int((new_y + y) / 2)
        end_list = [((new_x, new_y), [((middle_x, middle_y), self.board[1 - self.my_color][middle_x][middle_y] == 2)])]

        for direct in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            # 不可重复
            if (new_x + direct[0] * 2, new_y + direct[1] * 2) == (x, y):
                continue
            else:
                """
                否则沿着一个方向检查，检查如果能够吃一个子，那么就接着递归check就可以
                """
                tmp_x, tmp_y = new_x + direct[0], new_y + direct[1]
                can_eat_flag = False
                """沿着此方向直到遇到第一个敌方棋子"""
                while self.check_bound(tmp_x, tmp_y) and self.check_bound(tmp_x + direct[0], tmp_y + direct[1]) and \
                        self.board[1 - self.my_color][tmp_x][tmp_y] == 0:
                    tmp_x, tmp_y = tmp_x + direct[0], tmp_y + direct[1]
                    # 如果率先遇到了我方棋子，直接没了
                    if self.board[self.my_color][tmp_x][tmp_y] == 1:
                        break

                if self.check_bound(tmp_x, tmp_y) and self.board[self.my_color][tmp_x][tmp_y] != 1:
                    if self.check_bound(tmp_x, tmp_y) and self.check_bound(tmp_x + direct[0],
                                                                           tmp_y + direct[1]) and self.if_can_eat(
                            tmp_x - direct[0], tmp_y - direct[1], tmp_x + direct[0], tmp_y + direct[1]):
                        # 已经明确可以吃子了
                        can_eat_flag = True
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!
                        # 有幸遇到一个环我卡！！！！！所以干脆判断新的子是否为原集合的子集，然后如果是的话game over
                        # 详见../log/circle.txt
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!
                        # 判断是否成环
                        for has_eaten in end_list[1]:
                            if has_eaten[0] == (tmp_x, tmp_y):
                                can_eat_flag = False

                if can_eat_flag:
                    tem_eat, tem_eaten = self.check_boss_max_eat(tmp_x - direct[0], tmp_y - direct[1],
                                                                 tmp_x + direct[0], tmp_y + direct[1])


                    if tem_eat > 0:
                        if max_eat < tem_eat + 1:
                            max_eat = tem_eat + 1
                            for eat in tem_eaten:
                                eat[1].append(
                                    ((middle_x, middle_y), self.board[1 - self.my_color][middle_x][middle_y] == 2))
                            end_list = tem_eaten
                        elif max_eat == tem_eat + 1:
                            for eat in tem_eaten:
                                eat[1].append(
                                    ((middle_x, middle_y), self.board[1 - self.my_color][middle_x][middle_y] == 2))
                            end_list += tem_eaten

        return max_eat, end_list

    def if_can_eat(self, x, y, new_x, new_y) -> bool:
        """
        查看能否从  从 x,y 能否吃子到 new_x,new_y  位置仅仅相差两格
        用于check_max_eats调用
        """
        # 如果越界 则直接结束判断
        if not self.check_bound(new_x, new_y):
            return False
        if self.board[self.my_color][new_x][new_y] != 0 or self.board[1 - self.my_color][new_x][new_y] != 0:
            return False
        middle_x, middle_y = int((new_x + x) / 2), int((new_y + y) / 2)
        if not self.check_bound(middle_x, middle_y):
            return False
        if self.board[1 - self.my_color][middle_x][middle_y] == 0:
            return False
        return True

    def check_if_my_lose(self) -> bool:
        """
        1.我方没有子了，输掉
        2.我方不能走子也不能吃子，则我方输掉比赛
        :return  返回我方是否已经输掉必赛    已经输掉返回True
        """
        if self.my_color == self.white_color:
            if len(self.white_color_check) == 0 and len(self.white_boss_check) == 0:
                return True
        else:
            if len(self.black_color_check) == 0 and len(self.black_boss_check) == 0:
                return True

        can_eat, end_list = self.getNextAction()
        if len(end_list) == 0:
            return True
        return False

    def player(self, color, x, y, new_x, new_y):
        """
        订正 需查看新位置之后能否成为王棋
        还需查看旧位置是否本来就是王棋
        """
        if self.board[color][x][y] == 1:
            # 需注意查看能否升级为王棋
            self.board[color][x][y] = 0
            if color == self.white_color:
                self.white_color_check.remove((x, y))
                # 如果说白棋往 黑棋后退的方向走了一步，将会导致越界，那么说明白棋将会升级为王棋
                if not self.check_bound(new_x, new_y + self.black_color_backward):
                    self.board[color][new_x][new_y] = 2
                    self.white_boss_check.add((new_x, new_y))
                else:
                    self.board[color][new_x][new_y] = 1
                    self.white_color_check.add((new_x, new_y))
            if color == self.black_color:
                self.black_color_check.remove((x, y))
                # 如果说黑棋往 白棋后退的方向走了一步，将会导致越界，那么说明黑棋将会升级为王棋
                if not self.check_bound(new_x, new_y + self.white_color_backward):
                    self.board[color][new_x][new_y] = 2
                    self.black_boss_check.add((new_x, new_y))
                else:
                    self.board[color][new_x][new_y] = 1
                    self.black_color_check.add((new_x, new_y))
        elif self.board[color][x][y] == 2:
            # 旧位置本来就是王琪
            self.board[color][x][y] = 0
            if color == self.white_color:
                self.white_boss_check.remove((x, y))
                self.white_boss_check.add((new_x, new_y))

            if color == self.black_color:
                self.black_boss_check.remove((x, y))
                self.black_boss_check.add((new_x, new_y))
            self.board[color][new_x][new_y] = 2

        self.my_color = 1 - self.my_color

    def player_goback_history(self, color, old_x, old_y, x, y):
        flag = False
        if self.board[color][x][y] == 2:
            flag = True  # 王棋
        self.board[color][x][y] = 0
        if not flag:
            self.board[color][old_x][old_y] = 1
            if color == self.white_color:
                self.white_color_check.remove((x, y))
                self.white_color_check.add((old_x, old_y))
            elif color == self.black_color:
                self.black_color_check.remove((x, y))
                self.black_color_check.add((old_x, old_y))
        else:
            self.board[color][old_x][old_y] = 2
            if color == self.white_color:
                self.white_boss_check.remove((x, y))
                self.white_boss_check.add((old_x, old_y))
            elif color == self.black_color:
                self.black_boss_check.remove((x, y))
                self.black_boss_check.add((old_x, old_y))
            # 本身是王琪 需要查看是否会变成一般棋
            # 在上面操作的基础上进行  注意！！！
            # 不好抉择  所以将由history决定把

        self.my_color = 1 - self.my_color

    def eat(self, color, old_x, old_y, new_x, new_y, eaten_list):
        flag = False
        # 考虑是否本身就是王琪吃子
        if self.board[color][old_x][old_y] == 2:
            flag = True
            self.board[color][new_x][new_y] = 2
        else:
            self.board[color][new_x][new_y] = 1
        self.board[color][old_x][old_y] = 0

        # 考虑吃子后能否升级为王琪
        if color == self.white_color:
            if flag:
                self.white_boss_check.remove((old_x, old_y))
            else:
                self.white_color_check.remove((old_x, old_y))
            # 如果说白棋往 黑棋后退的方向走了一步，将会导致越界，那么说明白棋将会升级为王棋
            if not self.check_bound(new_x, new_y + self.black_color_backward):
                flag = True
            if flag:
                self.board[color][new_x][new_y] = 2
                self.white_boss_check.add((new_x, new_y))
            else:
                self.board[color][new_x][new_y] = 1
                self.white_color_check.add((new_x, new_y))
            # 接着将被吃掉的子进行操作
            for eat, boss_flag in eaten_list:
                self.board[1 - color][eat[0]][eat[1]] = 0
                if boss_flag:
                    self.black_boss_check.remove(eat)
                else:
                    self.black_color_check.remove(eat)
        elif color == self.black_color:
            if flag:
                self.black_boss_check.remove((old_x, old_y))
            else:
                self.black_color_check.remove((old_x, old_y))

            # 如果说黑棋往 白棋后退的方向走了一步，将会导致越界，那么说明黑棋将会升级为王棋
            if not self.check_bound(new_x, new_y + self.white_color_backward):
                flag = True

            if flag:
                self.board[color][new_x][new_y] = 2
                self.black_boss_check.add((new_x, new_y))
            else:
                self.board[color][new_x][new_y] = 1
                self.black_color_check.add((new_x, new_y))
            # 接着将被吃掉的子进行操作
            for eat, boss_flag in eaten_list:
                self.board[1 - color][eat[0]][eat[1]] = 0
                if not boss_flag:
                    self.white_color_check.remove(eat)
                else:
                    self.white_boss_check.remove(eat)

        self.my_color = 1 - self.my_color

    def eat_goback_history(self, color, old_x, old_y, x, y, eaten_list):
        """
        对此应该注意
        如果本身是王琪，  如果回退后可能变成一般棋的！！！！
        """
        flag = False
        if self.board[color][x][y] == 2:
            flag = True  # 王棋
        self.board[color][x][y] = 0
        if not flag:
            self.board[color][old_x][old_y] = 1
            if color == self.white_color:
                self.white_color_check.remove((x, y))
                self.white_color_check.add((old_x, old_y))
                # 接着将被吃掉的子进行操作 恢复即可
                for eat, boss_flag in eaten_list:
                    if boss_flag:
                        self.board[1 - color][eat[0]][eat[1]] = 2
                        self.black_boss_check.add(eat)
                    else:
                        self.board[1 - color][eat[0]][eat[1]] = 1
                        self.black_color_check.add(eat)
            elif color == self.black_color:
                self.black_color_check.remove((x, y))
                self.black_color_check.add((old_x, old_y))
                # 接着将被吃掉的子进行操作
                for eat, boss_flag in eaten_list:
                    if not boss_flag:
                        self.board[1 - color][eat[0]][eat[1]] = 1
                        self.white_color_check.add(eat)
                    else:
                        self.board[1 - color][eat[0]][eat[1]] = 2
                        self.white_boss_check.add(eat)
        else:
            self.board[color][old_x][old_y] = 2
            if color == self.white_color:
                self.white_boss_check.remove((x, y))
                self.white_boss_check.add((old_x, old_y))
                # 接着将被吃掉的子进行操作 恢复即可
                for eat, boss_flag in eaten_list:
                    if boss_flag:
                        self.board[1 - color][eat[0]][eat[1]] = 2
                        self.black_boss_check.add(eat)
                    else:
                        self.board[1 - color][eat[0]][eat[1]] = 1
                        self.black_color_check.add(eat)
            elif color == self.black_color:
                self.black_boss_check.remove((x, y))
                self.black_boss_check.add((old_x, old_y))
                # 接着将被吃掉的子进行操作
                for eat, boss_flag in eaten_list:
                    if boss_flag:
                        self.board[1 - color][eat[0]][eat[1]] = 2
                        self.white_boss_check.add(eat)
                    else:
                        self.board[1 - color][eat[0]][eat[1]] = 1
                        self.white_color_check.add(eat)
            # 本身是王琪 需要查看是否会变成一般棋
            # 在上面操作的基础上进行  注意！！！
            # 不好抉择  所以将由history决定把

        self.my_color = 1 - self.my_color

    def err_log(self):
        """
        debug使用
        :return:
        """
        import os

        f = None
        print(os.getcwd())
        if not os.path.exists('../err/err.txt'):
            os.makedirs(os.path.dirname("../err/err.txt"), exist_ok=True)

        with open("../err/err.txt", mode='w', encoding='utf-8') as ff:
            ff.write("below are white board"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            for i in range(self.board_width_check_nums):
                line = ""
                for j in range(self.board_height_check_nums):
                    line += str(self.board[self.white_color][i][j]) + ", "
                line += "\n"
                ff.write(line)
            ff.write("below are black board"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            for i in range(self.board_width_check_nums):
                line = ""
                for j in range(self.board_height_check_nums):
                    line += str(self.board[self.black_color][i][j]) + ", "
                line += "\n"
                ff.write(line)
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")

    def log(self):
        """
        为后续日志功能书写
        :return:
        """
        import os

        f = None
        print(os.getcwd())
        if not os.path.exists('../log/log.txt'):
            os.makedirs(os.path.dirname("../log/log.txt"), exist_ok=True)

        with open("../log/log.txt", mode='w', encoding='utf-8') as ff:
            ff.write("below are white board"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            for i in range(self.board_width_check_nums):
                line = ""
                for j in range(self.board_height_check_nums):
                    line += str(self.board[self.white_color][i][j]) + ", "
                line += "\n"
                ff.write(line)
            ff.write("below are black board"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            for i in range(self.board_width_check_nums):
                line = ""
                for j in range(self.board_height_check_nums):
                    line += str(self.board[self.black_color][i][j]) + ", "
                line += "\n"
                ff.write(line)
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")
            ff.write("-----------------------------"+"\n")

    """
    #######################################################################################
                                    下面对王棋引入
                                    规定普通棋子为1，现在规定王棋为2
                                    使用self.boss_check集合记录在线的王棋数
    #######################################################################################
    """
