import heapq


class EventScheduler:

    def can_attend_all(self, events: list[tuple]) -> bool:
        if not events:
            return True

        sorted_events = sorted(events, key=lambda x: x[0])

        for i in range(1, len(sorted_events)):
            # strict overlap only - adjacent is allowed
            if sorted_events[i][0] < sorted_events[i - 1][1]:
                return False

        return True

    def min_rooms_required(self, events: list[tuple]) -> int:
        if not events:
            return 0

        sorted_events = sorted(events, key=lambda x: x[0])

        room_end_times = []  # min-heap of room end times

        for start, end in sorted_events:
            if room_end_times and room_end_times[0] <= start:
                # reuse the room that becomes available first
                heapq.heapreplace(room_end_times, end)
            else:
                # all rooms are busy, allocate a new one
                heapq.heappush(room_end_times, end)

        return len(room_end_times)
