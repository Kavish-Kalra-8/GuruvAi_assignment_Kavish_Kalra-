'''
Both functions share the same first step — sorting events by start time. Once events are in order, reasoning about overlaps and room assignments becomes straightforward because we're always looking at things in the sequence they actually happen.
For can_attend_all, after sorting, the only thing that needs checking is whether any event starts before the previous one ends. If the list is sorted and no consecutive pair overlaps, then no pair anywhere in the list overlaps either. One linear pass is enough. The adjacent case where one event ends exactly when the next begins is not treated as an overlap — the check is strict, so end time equal to start time passes fine.
For min_rooms_required, sorting alone isn't enough because multiple events can run simultaneously and we need to track all of them. The key observation is that we don't need to know which specific room is free — we just need to know whether any room is free at all. The earliest-ending room is the best candidate for reuse, so we use a min-heap to always have that value instantly available at the top.
As each event is processed, we check the heap top. If the earliest-ending room has already finished, we reuse it. If not, every room is still busy and we open a new one. Rooms are never created upfront — they come into existence only when no existing room can be reused. By the end, the heap size equals the number of rooms that were allocated. Since a new room is only created when no existing room can be reused, this is also the minimum number of rooms needed to schedule all events without conflicts.
'''



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