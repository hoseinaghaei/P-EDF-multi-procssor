from task import Task, new_releases, new_deadlines

nodes_first_version = {}


def add_edge(parent, child):
    parent.children.append(child)
    child.parents.append(parent)


def generate_tree_from_matrix(graph, execution_times, deadlines, seen_nodes):
    global nodes_first_version
    num_nodes = len(graph)
    nodes = []
    for i in range(num_nodes):
        if i in seen_nodes:
            continue
        node = Task(execution_times[i], deadlines[i], i)
        nodes.append(node)

        if i not in nodes_first_version.keys():
            nodes_first_version[i] = node

    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            row = nodes[i].id
            column = nodes[j].id
            if graph[row][column] == 1:
                add_edge(nodes[i], nodes[j])

    return nodes


def longest_path_with_sum(node):
    if not node.children:
        return node.execution_time, [node]

    max_sum = 0
    max_path = []

    for child in node.children:
        child_sum, child_path = longest_path_with_sum(child)
        if child_sum > max_sum:
            max_sum = child_sum
            max_path = child_path

    max_sum += node.execution_time
    max_path.insert(0, node)

    return max_sum, max_path


def remove_nodes_with_longest_path(roots):
    max_sum = 0
    max_path = []

    for root in roots:
        node_max_sum, node_max_path = longest_path_with_sum(root)
        if node_max_sum > max_sum:
            max_sum = node_max_sum
            max_path = node_max_path

    print("Longest path with sum of values:", [node.execution_time for node in max_path])
    print("Sum of values in the longest path:", max_sum)

    max_path_set = set(max_path)

    # DFS to remove nodes in max_path from children and parent lists
    def dfs_remove(node):
        if node in max_path_set:
            return None

        node.children = [child for child in node.children if child not in max_path_set]
        node.parent = [parent for parent in node.parents if parent not in max_path_set]
        for child in node.children:
            dfs_remove(child)

    for root in roots:
        dfs_remove(root)

    return max_path


def update_deadline_release(removed_nodes):
    global nodes_first_version
    for node in removed_nodes:
        node.new_deadline = new_deadlines[node.id]
        node.new_release = new_releases[node.id]
        node.parents = nodes_first_version[node.id].parents
        node.children = nodes_first_version[node.id].children
