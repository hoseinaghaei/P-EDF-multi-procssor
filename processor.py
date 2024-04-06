
class Processor:
    def __init__(self, id):
        self.id = id
        self.tasks = []

    def get_execution_time(self):
        execution_time = sum([task.execution_time for task in self.tasks])
        if len(self.tasks) == 0:
            return execution_time

        return execution_time + self.tasks[0].new_release

    def schedule(self):
        current_time = 0
        task_queue = [(task.new_deadline, task) for task in self.tasks]
        task_queue.sort(key=lambda x: x[0])

        while task_queue:
            _, current_task = task_queue.pop(0)

            if current_time < current_task.new_release:
                current_time = current_task.new_release

            current_task.start_time = current_time
            current_task.finish_time = current_time + current_task.execution_time
            current_time = current_task.finish_time

        return self.tasks

    def title(self):
        return f'Processor {self.id}'


def assign_nodes_to_processor(processors, removed_nodes):
    for processor in processors:
        if len(processor.tasks) == 0:
            processor.tasks += removed_nodes
            return

    min_execution_time, min_execution_processor = int(1e10), processors[0]
    for processor in processors:
        if processor.get_execution_time() < min_execution_time:
            min_execution_time = processor.get_execution_time()
            min_execution_processor = processor

    min_execution_processor.tasks += removed_nodes
