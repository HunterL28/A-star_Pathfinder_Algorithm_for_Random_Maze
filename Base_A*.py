import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, open_position_list, closed_position_list):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            open_position_list.extend((node.g, node.position) for node in open_list)
            closed_position_list.extend((node.g, node.position) for node in closed_list)

            return path[::-1]  # Return reversed path


        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if any(closed_child.position == child.position for closed_child in closed_list):
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if not any(open_node.position == child.position and open_node.g < child.g for open_node in open_list):
                # Add the child to the open list
                open_list.append(child)
    closed_position_list.extend((node.g, node.position) for node in closed_list)
    return[]

def main():
    list_values = [1, 2, 3, 4, 5, 6, 7, 8]
    values = [0, 1]
    maze_size = 10

    maze = [[0 for _ in range(maze_size)] for _ in range(maze_size)]

    for i in range(maze_size):
        for j in range(maze_size):
            maze[i][j] = random.choices(values, weights = [3, 2], k = 1)[0]


    start = (random.choice(list_values), random.choice(list_values))
    end = (random.choice(list_values), random.choice(list_values))
    while maze[start[0]][start[1]] == 1 or maze[end[0]][end[1]] == 1:
        start = (random.choice(list_values), random.choice(list_values))
        end = (random.choice(list_values), random.choice(list_values))


    open_position_list = []
    closed_position_list = []

    path = astar(maze, start, end, open_position_list, closed_position_list)
    while not path:
        for i in range(maze_size):
            for j in range(maze_size):
                maze[i][j] = random.choices(values, weights=[3, 2], k=1)[0]
        path = astar(maze, start, end, open_position_list, closed_position_list)

    def plot_maze_with_path(maze, path, open_path, closed_path):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', 'box')

        # Plotting maze
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == 1:
                    rect = patches.Rectangle((j, len(maze) - i - 1), 1, 1, linewidth=.5, edgecolor='black',
                                             facecolor='black')
                    ax.add_patch(rect)

        # Plotting path
        for position in path:
            rect = patches.Rectangle((position[1], len(maze) - position[0] - 1), .4, .4, linewidth=.4, edgecolor='red',
                                     facecolor='red')
            ax.add_patch(rect)

        # Connecting red dots with a line
        if len(path) > 1:
            path_x, path_y = zip(*[(pos[1] + 0.2, len(maze) - pos[0] - 0.8) for pos in path])
            ax.plot(path_x, path_y, color='red', linestyle='-', linewidth=4)

        for position in open_path:
            rect = patches.Rectangle((position[1], len(maze) - position[0] - 1), .4, .4, linewidth=.4, edgecolor='blue',
                                     facecolor='blue')
            ax.add_patch(rect)

        for position in closed_path:
            rect = patches.Rectangle((position[1], len(maze) - position[0] - 1), .2, .2, linewidth=.2, edgecolor='blue',
                                     facecolor='green')
            ax.add_patch(rect)

        plt.xlim(0, len(maze[0]))
        plt.xticks(range(len(maze[0])))
        plt.ylim(len(maze), 0)
        plt.yticks(range(len(maze)))
        plt.show()

    # Example maze and path
    maze_example = maze

    path_example = path

    open_path = [pos for g, pos in open_position_list]

    closed_path = [pos for g, pos in closed_position_list]

    # Plotting the maze with path
    plot_maze_with_path(maze_example, path_example, open_path, closed_path)

    print('Closed List:', closed_position_list)
    print ('Open List:', open_position_list)
    print('Path', path)


if __name__ == '__main__':
    main()