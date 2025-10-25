import sys
import heapq

# стоимость посещения
COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
# позиции комнат
room_pos = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
room_idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def solve(lines: list[str]) -> int:
    # глубина комнат
    room_size = len(lines) - 3

    # парсим начальные комнаты
    rooms = []
    for i in range(room_size):
        rooms.append([
            lines[2 + i][3],
            lines[2 + i][5],
            lines[2 + i][7],
            lines[2 + i][9],
        ])

    # транспонируем комнаты и преобразуем в кортежи
    rooms = tuple(tuple(room) for room in zip(*rooms))

    hallway = '.' * 11
    init_state = (0, hallway, rooms)  # (cost, hallway, rooms)

    # цель
    target_rooms = []
    for room_type in 'ABCD':
        room = tuple([room_type] * room_size)
        target_rooms.append(room)
    target_rooms = tuple(target_rooms)

    heap = [init_state]
    visited = set()

    while heap:
        cost, hallway, rooms = heapq.heappop(heap)

        # приводим к хешируемому виду
        state_key = (hallway, rooms)
        if state_key in visited:
            continue
        visited.add(state_key)

        if rooms == target_rooms:
            return cost

        # ход из комнаты в коридор
        for room_i in range(4):
            room_type = 'ABCD'[room_i]
            r_pos = room_pos[room_type]
            room = rooms[room_i]

            pod_depth = -1
            for depth in range(room_size):
                if room[depth] != '.':
                    pod_depth = depth
                    break

            if pod_depth == -1:
                continue

            pod = room[pod_depth]

            should_move = False
            for depth in range(pod_depth, room_size):
                if room[depth] != room_type:
                    should_move = True
                    break

            if not should_move:
                continue

            # перемещаем в коридор
            for target_pos in range(11):
                if target_pos in [2, 4, 6, 8]:
                    continue

                if hallway[target_pos] == '.' and is_path_clear(hallway, r_pos, target_pos):
                    steps = pod_depth + 1 + abs(r_pos - target_pos)
                    new_cost = cost + steps * COST[pod]
                    new_hallway = hallway[:target_pos] + pod + hallway[target_pos + 1:]

                    # создаем новую комнату как список, изменяем, потом обратно в кортеж
                    new_room_list = list(room)
                    new_room_list[pod_depth] = '.'
                    new_room = tuple(new_room_list)

                    new_rooms_list = list(rooms)
                    new_rooms_list[room_i] = new_room
                    new_rooms = tuple(new_rooms_list)

                    heapq.heappush(heap, (new_cost, new_hallway, new_rooms))

        # ход из коридора в комнату
        for pos in range(11):
            if hallway[pos] != '.':
                pod = hallway[pos]
                room_i = room_idx[pod]
                r_pos = room_pos[pod]
                room = rooms[room_i]

                # проверяем можно ли войти в комнату
                if not can_enter(room, pod, room_size):
                    continue

                if not is_path_clear(hallway, pos, r_pos):
                    continue

                # находим глубину, на которую можно войти
                target_depth = -1
                for depth in range(room_size - 1, -1, -1):
                    if room[depth] == '.':
                        target_depth = depth
                        break

                if target_depth == -1:
                    continue

                steps = abs(pos - r_pos) + target_depth + 1
                new_cost = cost + steps * COST[pod]
                new_hallway = hallway[:pos] + '.' + hallway[pos + 1:]

                # создаем новую комнату как список, изменяем, потом обратно в кортеж
                new_room_list = list(room)
                new_room_list[target_depth] = pod
                new_room = tuple(new_room_list)

                new_rooms_list = list(rooms)
                new_rooms_list[room_i] = new_room
                new_rooms = tuple(new_rooms_list)

                heapq.heappush(heap, (new_cost, new_hallway, new_rooms))

    return 0


def is_path_clear(hallway, start, end):
    step = 1 if start < end else -1
    for pos in range(start + step, end + step, step):
        if hallway[pos] != '.':
            return False
    return True


def can_enter(room, pod_type, room_size):
    for cell in room:
        if cell != '.' and cell != pod_type:
            return False
    return True


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()