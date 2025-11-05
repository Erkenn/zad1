import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # строим граф
    graph = defaultdict(list)
    gateways = set()

    for n1, n2 in edges:
        graph[n1].append(n2)
        graph[n2].append(n1)

        # определяем шлюзы
        if n1.isupper():
            gateways.add(n1)
        if n2.isupper():
            gateways.add(n2)

    virus_pos = 'a'
    result = []

    # функция для определения следующего шага вируса
    def get_virus_next_move(pos):
        # находим все ближайшие шлюзы
        queue = deque([pos])
        dist = {pos: 0}
        prev = {pos: None}
        closest_gateways = []
        min_dist = float('inf')

        while queue:
            current = queue.popleft()
            current_dist = dist[current]

            if current in gateways:
                if current_dist < min_dist:
                    min_dist = current_dist
                    closest_gateways = [current]
                elif current_dist == min_dist:
                    closest_gateways.append(current)
                continue

            if current_dist > min_dist:
                continue

            for neighbor in sorted(graph[current]):
                if neighbor not in dist:
                    dist[neighbor] = current_dist + 1
                    prev[neighbor] = current
                    queue.append(neighbor)

        if not closest_gateways:
            return None, None

        # выбираем лексикографически наименьший шлюз
        target_gateway = min(closest_gateways)

        # восстанавливаем путь к шлюзу
        path = []
        node = target_gateway
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()

        # следующий шаг - второй узел в пути
        if len(path) > 1:
            return target_gateway, path[1]
        return target_gateway, None

    # основной цикл
    while True:
        # определяем, куда пойдет вирус
        target_gateway, next_move = get_virus_next_move(virus_pos)

        # если вирус не может двигаться, заканчиваем
        if next_move is None:
            break

        # находим все возможные отключаемые коридоры (шлюз-узел)
        available_cuts = []
        for gateway in sorted(gateways):
            for neighbor in sorted(graph[gateway]):
                available_cuts.append(f"{gateway}-{neighbor}")

        # сортируем по лексикографическому порядку
        available_cuts.sort()

        # проверяем, можем ли мы отключить коридор на пути вируса
        cut_made = False

        # сначала пытаемся отключить коридор, который ведет к целевому шлюзу от следующей позиции
        potential_cut = f"{target_gateway}-{next_move}"
        if potential_cut in available_cuts:
            result.append(potential_cut)
            graph[target_gateway].remove(next_move)
            graph[next_move].remove(target_gateway)
            cut_made = True
        else:
            # если не можем отключить прямой путь, ищем любой коридор, который замедлит вирус
            for cut in available_cuts:
                gateway, node = cut.split('-')

                # временно удаляем этот коридор
                graph[gateway].remove(node)
                graph[node].remove(gateway)

                # проверяем, изменился ли путь вируса
                new_target, new_next = get_virus_next_move(virus_pos)

                # если путь изменился или вирус заблокирован, оставляем отключение
                if new_next != next_move or new_next is None:
                    result.append(cut)
                    cut_made = True
                    break
                else:
                    # возвращаем коридор
                    graph[gateway].append(node)
                    graph[node].append(gateway)

        # если не нашли подходящий отключаемый коридор, берем первый доступный
        if not cut_made and available_cuts:
            cut = available_cuts[0]
            gateway, node = cut.split('-')
            result.append(cut)
            graph[gateway].remove(node)
            graph[node].remove(gateway)
            cut_made = True

        # вирус делает ход
        if next_move in graph[virus_pos]:
            virus_pos = next_move

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()