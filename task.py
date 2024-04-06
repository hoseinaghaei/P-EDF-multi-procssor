from collections import deque

new_deadlines = {}
new_releases = {}


class Task:
    def __init__(self, execution_time, deadline, id):
        self.id = id
        self.execution_time = execution_time
        self.deadline = deadline
        self.new_release = 0
        self.new_deadline = 0
        self.parents = []
        self.children = []
        self.start = 0
        self.finish = 0


def calculate_new_release_deadline(nodes):
    global new_releases, new_deadlines
    _calculate_new_release(nodes)
    _calculate_new_deadline(nodes)

    for node in nodes:
        new_deadlines[node.id] = node.new_deadline
        new_releases[node.id] = node.new_release


def _calculate_new_release(nodes):
    tasks_to_deque = deque([node for node in nodes if len(node.parents) == 0])
    while tasks_to_deque:
        current_node = tasks_to_deque.popleft()
        if current_node.parents:
            current_node.new_release = max(0,
                                           max(
                                               [parent.new_release + parent.execution_time for parent in
                                                current_node.parents]
                                           ))
        else:
            current_node.new_release = 0

        for child in current_node.children:
            tasks_to_deque.append(child)


def _calculate_new_deadline(nodes):
    tasks_to_deque = deque([node for node in nodes if len(node.children) == 0])
    while tasks_to_deque:
        current_node = tasks_to_deque.popleft()
        if current_node.children:
            current_node.new_deadline = min(current_node.deadline,
                                            min(
                                                [child.new_deadline - child.execution_time for child in
                                                 current_node.children]
                                            ))
        else:
            current_node.new_deadline = current_node.deadline

        for parent in current_node.parents:
            tasks_to_deque.append(parent)
