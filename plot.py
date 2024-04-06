import numpy as np
from matplotlib import pyplot as plt


def plot_tasks(tasks_list: list, titles: list):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # Create a 1x3 grid of subplots

    for idx, (tasks, title) in enumerate(zip(tasks_list, titles)):
        ax = axs[idx]
        for task in tasks:
            ax.barh(task.id, width=task.execution_time, left=task.start_time, label=f'Task {task.id + 1}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Task ID')
        ax.set_title(title)
        x_ticks = np.arange(0, max(task.finish_time for task in tasks) + 1, 5)
        ax.set_xticks(x_ticks)
        ax.legend()

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()
