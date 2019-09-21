class Node:
    def __init__(self, string, parent=None, level=0, num_in_level=0):
        """Инициализация"""
        self.string = string

        self.parent = parent
        self.childs = []

        self.level = level
        self.num_in_level = num_in_level

    def replace_this_node(self, string):
        """Замена строки нода вместо текущей"""
        # new_node = node(string=string,
        #                 parent=self.parent,
        #                 level=self.level,
        #                 num_in_level=self.num_in_level)

        self.string = string

        return self

    def make_child(self, string):
        """Создание потомка"""
        new_node = Node(string=string,
                        parent=self,
                        level=self.level + 1,
                        num_in_level=len(self.childs))

        return new_node

    def drop_to_childs(self, string, child1_string, child2_string):
        """Разбиение нода на потомков"""
        pass

    def __repr__(self):
        """Представление нода"""
        return self.__str__()

    def __str__(self):
        """Строковое представление"""
        return self.string

    def _search_in_childs(self, string):
        """Поиск строки в потомках"""
        for child in self.childs:
            # Ищем во всех потомках
            child_elem, child_resp = child.search_str(string)
            if child_resp:
                # Если что-то нашли, значит нужно вернуть найденный нод
                return child_elem, child_resp
            elif child_elem:
                # Если ничего не найдено, но последний нод в цепи не является
                #    непосредственным потомком, значит нужно его вернуть
                return child_elem, child_resp
            # Если ничего не нашлось, то ищем дальше
        else:
            # Если не нашли вообще ничего, то текущий нод последний в цепочке
            return self, None

    def search_str(self, string):
        """Поиск строки в текущем ноде"""
        if self.string == string:
            # Сравнение строки с собственной
            #    Если равны, значит нужный нод найден
            return self, string
        elif self.string == string[:len(self.string)]:
            # Содержится ли строка нода в начале искомой строки
            #    Если да, то ищем в потомках
            return self._search_in_childs(string[len(self.string):])
        elif self.string[0] == string[0]:
            return self, None
        else:
            # Если ничего не найдено, значит общего нет
            return None, None

    def add_string(self, string):
        """Поиск в дереве и добавление строки"""
        found_node, str_result = self.search_str(string)

        if not str_result:
            node_string = found_node.string
            compare_list = zip(node_string, string)
            compare_result = [num for num, pair in enumerate(compare_list)
                              if pair[0] != pair[1]]

            if compare_result:
                # Если в списке сравнения есть элементы,
                #    значит одно слово не заключено в другом
                if compare_result[0] > 0:
                    # Если первый элемент списка сравнения больше нуля,
                    #    значит у слов есть одинаковая основа
                    same_len = compare_result[0]
                    same_string = node_string[:same_len]
                    first_substr = node_string[same_len:]
                    second_substr = string[same_len:]

                    new_parent_node = found_node.replace_this_node(same_string)
                    first_child = new_parent_node.make_child(first_substr)
                    second_child = new_parent_node.make_child(second_substr)

                    first_child.childs = found_node.childs
                    new_parent_node.childs = [first_child, second_child]

                    # print('Разбит на потомков')
                else:
                    # Если первый элемент списка сравнения равен нулю,
                    #    значит у слов нет одинаковой основы
                    pass

                    # print('Соседи')
            else:
                # Если список пуст, значит одна строка содержит другую
                node_string = found_node.string
                node_string_len = len(node_string)
                string_len = len(string)
                if node_string_len < string_len:
                    # Если строка нода короче, значит нужно добавить потомка
                    new_child_string = string[node_string_len:]
                    new_child_node = found_node.make_child(new_child_string)

                    found_node.childs.append(new_child_node)
                else:
                    # Если строка нода длинее, значит надо его разбить
                    new_parent_string = string
                    new_child_string = node_string[string_len:]

                    new_parent_node = found_node.replace_this_node(new_parent_string)
                    new_child = new_parent_node.make_child(new_child_string)

                    new_child.childs = found_node.childs
                    new_parent_node.childs.append(new_child)

                # print('Содержит')
        else:
            pass
            # print('    Строка "{}" уже здесь'.format(string))


class Tree:
    def __init__(self):
        self.root = Node('')


if __name__ == '__main__':
    new_tree = Tree()
    new_tree.root.add_string('hello')
    new_tree.root.add_string('hell')
    new_tree.root.add_string('hal')

    new_tree.root.add_string('boo')
    new_tree.root.add_string('boom')
    new_tree.root.add_string('bool')

    a = 1

