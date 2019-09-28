class Node:
    def __init__(self, string, parent=None, level=0, num_in_level=0):
        """Инициализация"""
        self.string = string

        self.parent = parent
        self.childs = []

        self.level = level
        self.num_in_level = num_in_level

        self.score = 0
        self.total_childs_count = 0

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

    def __int__(self):
        """Числовое представление хранимой информации"""
        return sum(map(ord, self.string))

    def __counts__(self):
        """Числовое предстваление. Показывает число детей во всех ветвях"""
        local_childs = len(self.childs)

        for child in self.childs:
            local_childs += child.__counts__()

        self.total_childs_count = local_childs
        return local_childs

    def __eq__(self, other):
        """Равенство нодов"""
        return self.string == other.string

    def __ne__(self, other):
        """Не равны"""
        return self.string != other.string

    def __lt__(self, other):
        """Текущий меньше"""
        return self.string < other.string

    def __gt__(self, other):
        """Текущий больше"""
        return self.string > other.string

    def __le__(self, other):
        """Текущий меньше или равен"""
        return self.string <= other.string

    def __ge__(self, other):
        """Текущий больше или равен"""
        return self.string >= other.string

    def __deep_sorted__(self):
        """Сортировка всех детей в алфавитном порядке"""
        self.childs = sorted(self.childs)

        for child in self.childs:
            child.__deep_sorted__()

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

    def repair_string_form_chain(self):
        """Восстановление строки из отдельного нода"""
        repaired_string = []
        target_node = self
        while target_node:
            repaired_string.insert(0, str(target_node))
            target_node = target_node.parent

        return repaired_string

    def refresh_levels(self):
        """Обновление уровня в дереве"""
        for child in self.childs:
            child.level = self.level + 1
            child.refresh_levels()

    def refresh_count(self):
        """Обновление количества нодов в дереве"""
        return self.__counts__()

    def full_sort(self):
        """Полная сортировка"""
        self.__deep_sorted__()

    def print_node(self):
        """Рекурсивная распечатка текущего нода и его потомков"""
        spaces = '_' * self.level
        node_map = '{}{}:\n'.format(spaces, self)
        for child in self.childs:
            node_map += child.print_node()

        return node_map


class Tree:
    def __init__(self):
        self.root = Node('')

    def add_string(self, string):
        """Поиск в дереве и добавление строки"""
        found_node, str_result = self.root.search_str(string)

        if not str_result:
            node_substr_list = found_node.repair_string_form_chain()
            node_substr_len = len(''.join(node_substr_list[:-1]))

            node_string = found_node.string
            target_string = string[node_substr_len:]

            compare_list = zip(node_string, target_string)
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
                    second_substr = target_string[same_len:]

                    new_parent_node = found_node.replace_this_node(same_string)
                    first_child = new_parent_node.make_child(first_substr)
                    second_child = new_parent_node.make_child(second_substr)

                    first_child.childs = found_node.childs.copy()
                    new_parent_node.childs = [first_child, second_child]

                    first_child.score = new_parent_node.score
                    second_child.score += 1
                    new_parent_node.score = 0

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
                string_len = len(target_string)
                if node_string_len < string_len:
                    # Если строка нода короче, значит нужно добавить потомка
                    new_child_string = target_string[node_string_len:]
                    new_child_node = found_node.make_child(new_child_string)

                    found_node.childs.append(new_child_node)

                    new_child_node.score += 1
                else:
                    # Если строка нода длинее, значит надо его разбить
                    new_parent_string = target_string
                    new_child_string = node_string[string_len:]

                    new_parent_node = found_node.replace_this_node(new_parent_string)
                    new_child = new_parent_node.make_child(new_child_string)

                    new_child.childs = found_node.childs.copy()
                    new_parent_node.childs.append(new_child)

                    new_parent_node.score += 1
                    pass

                # print('Содержит')
        else:
            found_node.score += 1
            # print('    Строка "{}" уже здесь'.format(string))

    def print_tree(self):
        """Распечатка дерева"""
        self.root.refresh_levels()
        tree_map = self.root.print_node()

        return tree_map

    def find_string(self, string):
        """Поиск строки в дереве и возвращение её параметров"""
        found_node, str_result = self.root.search_str(string)
        string_path = found_node.repair_string_form_chain()
        string_path = '-'.join(string_path)[1:]

        if any([not str_result, found_node.score < 1]):
            string_path += '~'
            print('Строка не найдена')

        return string_path, found_node.level, found_node.num_in_level


if __name__ == '__main__':
    new_tree = Tree()
    new_tree.add_string('табак')
    new_tree.add_string('тяпка')
    new_tree.add_string('татуировочного')
    new_tree.add_string('татуировочному')

    new_tree.add_string('татуировочный')
    new_tree.add_string('татуировочным')
    new_tree.add_string('татуировочном')

    new_tree.root.refresh_levels()
    counts = new_tree.root.refresh_count()
    new_tree.root.full_sort()

    # path, node_lev, node_num = new_tree.find_string('та')
    # print(path)
    print(counts)
    print(new_tree.print_tree())

    a = 1

