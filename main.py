from copy import deepcopy

from graph import generate_tree_from_matrix, remove_nodes_with_longest_path, update_deadline_release
from plot import plot_tasks
from processor import Processor, assign_nodes_to_processor
from task import calculate_new_release_deadline

matrix = [
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

execution_times = [3, 18, 12, 9, 11, 12, 19, 3, 8, 1]
deadlines = [20, 50, 50, 50, 50, 50, 70, 70, 70, 110]
PROCESSOR_COUNT = 3


def main():
    global matrix, execution_times, deadlines, PROCESSOR_COUNT

    processors = [Processor(i) for i in range(PROCESSOR_COUNT)]
    matrix_to_schedule = deepcopy(matrix)

    seen_nodes = set()
    nodes = generate_tree_from_matrix(matrix_to_schedule, execution_times, deadlines, seen_nodes)
    calculate_new_release_deadline(nodes)
    nodes_count = len(nodes)
    roots = [node for node in nodes if len(node.parents) == 0]

    while len(seen_nodes) < nodes_count:
        removed_nodes = remove_nodes_with_longest_path(roots)
        update_deadline_release(removed_nodes)
        assign_nodes_to_processor(processors, removed_nodes)
        removed_nodes_ids = [node.id for node in removed_nodes]
        seen_nodes.update(removed_nodes_ids)
        for node in removed_nodes:
            for i in range(len(matrix_to_schedule)):
                matrix_to_schedule[node.id][i] = 0
                matrix_to_schedule[i][node.id] = 0

        nodes = generate_tree_from_matrix(matrix_to_schedule, execution_times, deadlines, seen_nodes)
        roots = [node for node in nodes if len(node.parents) == 0]

    for processor in processors:
        processor.schedule()

    tasks = []
    titles = []
    for processor in processors:
        tasks.append(processor.tasks)
        titles.append(processor.title())

    plot_tasks(tasks, titles)


if __name__ == "__main__":
    main()
