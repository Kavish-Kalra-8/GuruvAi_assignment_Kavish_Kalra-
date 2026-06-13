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
        
'''
The core idea is greedy scheduling. We want to reuse rooms as aggressively as possible, and only open a new room when there is genuinely no other option.
The first step is sorting all events by start time. This ensures we always process meetings in the order they begin, which is the natural order for making room assignment decisions.
We then use a min-heap to track the end times of all currently allocated rooms. The reason we use a min-heap specifically is that at any point we only care about one thing — which room becomes free the soonest. The min-heap always keeps that value at the top, giving us O(log n) access to the earliest-ending meeting.
For each event we process, there are exactly two situations:
If the earliest-ending room finishes at or before the current event's start time, that room is free. We reuse it by replacing its end time in the heap with the current event's end time via heapreplace. The heap size stays the same — no new room is opened.
If every room is still occupied when the current event starts, we have no choice but to open a new room. We push the new end time into the heap via heappush, increasing the heap size by one.
At the end, the heap size gives us the answer. The heap only ever grows when heappush is called — that is, only when no free room was available and a new one had to be allocated. heapreplace never changes the size. So the final heap size is simply the total number of rooms we were forced to open throughout the entire scheduling process, which is exactly the minimum number of rooms required.
The adjacent case where one meeting ends exactly when another begins is handled correctly — a room whose end time equals the new event's start time is considered free, so no extra room is opened unnecessarily.
Overall complexity is O(n log n) — dominated by the sort, with each heap operation costing O(log n) across n events.'''