import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # строим граф из соединений
    graph = defaultdict(list)
    gateways = set()

    for n1, n2 in edges:
        graph[n1].append(n2)
        graph[n2].append(n1)

        # определяем шлюзы по заглавным буквам
        if n1.isupper():
            gateways.add(n1)
        if n2.isupper():
            gateways.add(n2)

    # текущая позиция вируса
    virus_pos = 'a'
    result = []

    # функция для нахождения ближайшего шлюза и следующего шага вируса
    def find_virus_move(position):
        queue = deque([position])
        visited = {position: None}
        found_gateways = []

        while queue and not found_gateways:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                current = queue.popleft()

                for neighbor in sorted(graph[current]):  # сортируем для детерминированности
                    if neighbor not in visited:
                        visited[neighbor] = current

                        if neighbor in gateways:
                            found_gateways.append(neighbor)
                        else:
                            queue.append(neighbor)

            # если на этом уровне нашли шлюзы, прекращаем поиск
            if found_gateways:
                break

        if not found_gateways:
            return None, None

        # выбираем лексикографически наименьший шлюз
        target_gateway = min(found_gateways)

        # восстанавливаем путь к выбранному шлюзу
        path = []
        current = target_gateway
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()

        # следующий шаг вируса - второй элемент пути
        if len(path) >= 2:
            return target_gateway, path[1]
        else:
            return target_gateway, None

    # основной игровой цикл
    while True:
        # 1. определяем, куда пойдет вирус
        target_gateway, next_move = find_virus_move(virus_pos)

        # если вирус не может двигаться, заканчиваем
        if next_move is None:
            break

        # 2. отключаем коридор, который предотвратит достижение целевого шлюза
        # находим все соединения с целевым шлюзом
        gateway_connections = []
        for neighbor in sorted(graph[target_gateway]):
            gateway_connections.append((target_gateway, neighbor))

        # сортируем по лексикографическому порядку
        gateway_connections.sort(key=lambda x: (x[0], x[1]))

        # отключаем соединение, которое находится на пути вируса к шлюзу
        cut_found = False

        for gateway, node in gateway_connections:
            # проверяем, является ли этот узел частью пути к шлюзу
            if node == next_move or (virus_pos == next_move and node in graph[next_move]):
                result.append(f"{gateway}-{node}")
                graph[gateway].remove(node)
                graph[node].remove(gateway)
                cut_found = True
                break

        # если не нашли конкретное соединение на пути, отключаем первое доступное
        if not cut_found and gateway_connections:
            gateway, node = gateway_connections[0]
            result.append(f"{gateway}-{node}")
            graph[gateway].remove(node)
            graph[node].remove(gateway)
            cut_found = True

        # 3. вирус делает ход
        if next_move in graph[virus_pos]:
            virus_pos = next_move
        else:
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