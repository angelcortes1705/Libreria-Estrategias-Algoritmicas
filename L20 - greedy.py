import heapq

from functools import total_ordering


@total_ordering
class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.__build_repr())

    def __build_repr(self):
        # Recursively build the dictionary of symbol encodings
        if self.symbol is not None:
            return {self.symbol: ""}
        else:
            left_encoding = self.left.__build_repr()
            right_encoding = self.right.__build_repr()
            # Combine encodings for left and right children
            return {
                **{key: "0" + value for key, value in left_encoding.items()},
                **{key: "1" + value for key, value in right_encoding.items()},
            }

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency


# 1) Activity Selection Problem:
# Proof that Greedy Approach Works:
# The greedy approach selects activities with the earliest finish times.
# It ensures the maximum number of non-overlapping activities can be scheduled.


def recursive_activity_selection(start, finish, n):
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected_activities = []

    def select_activities(k, activities):
        m = k + 1
        while m < len(activities) and activities[m][0] < activities[k][1]:
            m += 1
        if m < len(activities):
            selected_activities.append(activities[m])
            select_activities(m, activities)

    if activities:
        selected_activities.append(activities[0])
        select_activities(0, activities)
    return selected_activities


def greedy_activity_selection(start, finish):
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected = []
    last_finish = 0

    for s, f in activities:
        if s >= last_finish:
            selected.append((s, f))
            last_finish = f

    return selected


# 2) Fractional Knapsack:
# Proof that Greedy Approach Works:
# The greedy approach selects items with the maximum value-to-weight ratio.
# It maximizes the total value within the knapsack's capacity.


def recursive_fractional_knapsack(items, capacity):
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)

    def helper(index, remaining):
        if index == len(sorted_items) or remaining <= 0:
            return 0, []
        weight, value = sorted_items[index]
        if weight <= remaining:
            v, lst = helper(index + 1, remaining - weight)
            return v + value, [(weight, value)] + lst
        else:
            fraction = remaining / weight
            return value * fraction, [(weight, value * fraction)]

    return helper(0, capacity)


def greedy_fractional_knapsack(items, capacity):
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    total_value = 0.0
    selected_items = []

    for weight, value in sorted_items:
        if capacity >= weight:
            selected_items.append((weight, value))
            total_value += value
            capacity -= weight
        else:
            fraction = capacity / weight
            selected_items.append((weight, value * fraction))
            total_value += value * fraction
            break

    return total_value, selected_items


# 3) Huffman Codes:
# The greedy approach constructs a binary tree to minimize the weighted path length.
# It guarantees an optimal prefix-free code for symbols with given frequencies.


def recursive_huffman_coding(symbols, frequencies):
    nodes = [HuffmanNode(sym, freq) for sym, freq in zip(symbols, frequencies)]

    def build_tree(nodes):
        if len(nodes) == 1:
            return nodes[0]
        nodes = sorted(nodes, key=lambda node: node.frequency)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(None, left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        nodes.append(merged)
        return build_tree(nodes)

    return build_tree(nodes)


def iterative_huffman_coding(symbols, frequencies):
    heap = [HuffmanNode(sym, freq) for sym, freq in zip(symbols, frequencies)]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


if __name__ == "__main__":
    # Example usage for Activity Selection Problem:
    start_times = [1, 3, 0, 5, 8, 5]
    finish_times = [2, 4, 6, 7, 9, 9]
    n = len(start_times)
    result = recursive_activity_selection(start_times, finish_times, n)
    print("Activity Selection (Recursive):", result)
    # Activity Selection (Recursive): [(1, 2), (3, 4), (5, 7), (8, 9)]
    result = greedy_activity_selection(start_times, finish_times)
    print("Activity Selection (Greedy):", result)
    # Activity Selection (Greedy): [(1, 2), (3, 4), (5, 7), (8, 9)]

    # Example usage for Fractional Knapsack:
    items = [(10, 60), (20, 100), (30, 120)]
    capacity = 50
    result, selected_items = recursive_fractional_knapsack(items, capacity)
    print(
        "Fractional Knapsack (Recursive): Max value:",
        result,
        "Selected items:",
        selected_items,
    )
    # Fractional Knapsack (Recursive): Max value: 240.0 Selected items: [(10, 60), (20, 100), (30, 80.0)]
    result, selected_items = greedy_fractional_knapsack(items, capacity)
    print(
        "Fractional Knapsack (Greedy): Max value:",
        result,
        "Selected items:",
        selected_items,
    )
    # Fractional Knapsack (Greedy): Max value: 240.0 Selected items: [(10, 60), (20, 100), (30, 80.0)]

    # Example usage for Huffman Codes:
    symbols = ["A", "B", "C", "D", "E"]
    frequencies = [45, 13, 12, 16, 9]
    root_recursive = recursive_huffman_coding(symbols, frequencies)
    print(f"Encoding: {root_recursive}")
    # Encoding: {'A': '0', 'E': '100', 'C': '101', 'B': '110', 'D': '111'}
    root_iterative = iterative_huffman_coding(symbols, frequencies)
    print(f"Encoding: {root_iterative}")
    # Encoding: {'A': '0', 'E': '100', 'C': '101', 'B': '110', 'D': '111'}
