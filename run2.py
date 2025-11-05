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

    # функция для нахождения пути вируса к ближайшему шлюзу
    def find_virus_path(pos):
        # BFS для поиска кратчайшего пути к любому шлюзу
        queue = deque([pos])
        visited = {pos: None}
        target_gateway = None

        while queue:
            current = queue.popleft()

            if current in gateways:
                target_gateway = current
                break

            for neighbor in sorted(graph[current]):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)

        if target_gateway is None:
            return None, None

        # восстанавливаем путь
        path = []
        node = target_gateway
        while node is not None:
            path.append(node)
            node = visited[node]
        path.reverse()

        return target_gateway, path

    # основной цикл
    while True:
        # находим путь вируса к ближайшему шлюзу
        target_gateway, path = find_virus_path(virus_pos)

        # если пути нет, вирус заблокирован
        if path is None or len(path) < 2:
            break

        # следующий шаг вируса
        next_move = path[1]

        # находим все соединения шлюзов с узлами
        gateway_connections = []
        for gateway in sorted(gateways):
            for neighbor in sorted(graph[gateway]):
                gateway_connections.append(f"{gateway}-{neighbor}")

        # сортируем по лексикографическому порядку
        gateway_connections.sort()

        # отключаем соединение между последним узлом и шлюзом в пути
        if len(path) >= 2:
            last_node = path[-2]  # предпоследний узел перед шлюзом
            gateway = path[-1]  # шлюз

            cut_candidate = f"{gateway}-{last_node}"

            # проверяем, существует ли такое соединение
            if cut_candidate in gateway_connections:
                result.append(cut_candidate)
                graph[gateway].remove(last_node)
                graph[last_node].remove(gateway)
            else:
                # если прямого соединения нет, отключаем первый доступный коридор
                if gateway_connections:
                    result.append(gateway_connections[0])
                    gateway, node = gateway_connections[0].split('-')
                    graph[gateway].remove(node)
                    graph[node].remove(gateway)

        # вирус делает ход
        if next_move in graph[virus_pos]:
            virus_pos = next_move
        else:
            # если вирус не может двигаться, заканчиваем
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