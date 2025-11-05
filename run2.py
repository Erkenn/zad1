import sys
from collections import defaultdict, deque
import heapq


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # строим граф
    graph = defaultdict(list)
    gateways = set()
    nodes = set()

    for n1, n2 in edges:
        graph[n1].append(n2)
        graph[n2].append(n1)
        nodes.add(n1)
        nodes.add(n2)

        # определяем шлюзы
        if n1.isupper():
            gateways.add(n1)
        if n2.isupper():
            gateways.add(n2)

    # текущая позиция вируса
    virus_pos = 'a'
    result = []

    # функция для поиска кратчайшего пути до любого шлюза
    def find_shortest_path(start):
        queue = deque([(start, [start])])
        visited = {start}
        target_gateways = []
        min_distance = float('inf')

        while queue:
            current, path = queue.popleft()
            distance = len(path) - 1

            if current in gateways:
                if distance <= min_distance:
                    if distance < min_distance:
                        target_gateways = []
                        min_distance = distance
                    target_gateways.append((current, path))
                continue

            if distance > min_distance:
                continue

            for neighbor in sorted(graph[current]):  # сортируем для детерминированности
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        if not target_gateways:
            return None, None

        # выбираем лексикографически наименьший шлюз
        target_gateways.sort(key=lambda x: (x[0], x[1][1] if len(x[1]) > 1 else ''))
        return target_gateways[0][0], target_gateways[0][1]

    # функция для определения следующего шага вируса
    def get_virus_next_move(position):
        target_gateway, path = find_shortest_path(position)
        if not path or len(path) < 2:
            return None
        return path[1]  # следующий узел

    # основной игровой цикл
    while True:
        # 1. определяем, куда пойдет вирус
        next_move = get_virus_next_move(virus_pos)

        # если вирус не может двигаться, заканчиваем
        if next_move is None:
            break

        # 2. определяем, какой коридор отключить
        # находим все возможные отключаемые коридоры (шлюз-узел)
        available_cuts = []
        for gateway in gateways:
            for neighbor in sorted(graph[gateway]):
                available_cuts.append((gateway, neighbor))

        # сортируем по лексикографическому порядку
        available_cuts.sort(key=lambda x: (x[0], x[1]))

        # пробуем отключить каждый возможный коридор, пока не найдем безопасный
        cut_made = False
        for gateway, node in available_cuts:
            # временно удаляем коридор
            graph[gateway].remove(node)
            graph[node].remove(gateway)

            # проверяем, может ли вирус все еще достичь шлюза
            can_reach_gateway = False
            for g in gateways:
                queue = deque([virus_pos])
                visited = {virus_pos}
                found = False

                while queue:
                    current = queue.popleft()
                    if current == g:
                        can_reach_gateway = True
                        found = True
                        break
                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                    if found:
                        break

            # если вирус не может достичь ни одного шлюза после отключения
            # или если мы предотвращаем его достижение шлюза
            if not can_reach_gateway:
                # этот откл коридор безопасен
                result.append(f"{gateway}-{node}")
                cut_made = True
                break
            else:
                # возвращаем коридор обратно
                graph[gateway].append(node)
                graph[node].append(gateway)

        # если не нашли безопасный отключаемый коридор
        if not cut_made:
            # отключаем коридор на пути вируса к ближайшему шлюзу
            target_gateway, path = find_shortest_path(virus_pos)
            if path and len(path) >= 2:
                # ищем соединение между последним узлом и шлюзом
                last_node = path[-2] if path[-1] in gateways else path[-1]
                gateway = path[-1] if path[-1] in gateways else None

                if gateway and last_node in graph[gateway]:
                    result.append(f"{gateway}-{last_node}")
                    graph[gateway].remove(last_node)
                    graph[last_node].remove(gateway)
                    cut_made = True

            # если все еще не нашли, отключаем первый доступный коридор
            if not cut_made and available_cuts:
                gateway, node = available_cuts[0]
                result.append(f"{gateway}-{node}")
                graph[gateway].remove(node)
                graph[node].remove(gateway)
                cut_made = True

        # 3. вирус делает ход
        if next_move and next_move in graph[virus_pos]:
            virus_pos = next_move
        else:
            # если вирус не может сделать запланированный ход, пересчитываем
            new_next_move = get_virus_next_move(virus_pos)
            if new_next_move and new_next_move in graph[virus_pos]:
                virus_pos = new_next_move
            else:
                # вирус заблокирован
                break

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