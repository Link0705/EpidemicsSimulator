from typing import List


class Node:
    # Class variable to store instances
    all_instances_by_id: dict[str, "Node"] = {}

    def __init__(self, group: "node_group.NodeGroup"):
        self.id: str = (
            f"{group.id}-{group.node_id_counter}"  # auto set new id
        )
        group.node_id_counter += 1
        self.group: "node_group.NodeGroup" = group
        self.connections: List["Node"] = []  # node ids this node is connected to
        self.infected: bool = False
        self.num_of_infections: int = 0
        # other properties, e.g. infected, was infected x times, etc.
        Node.all_instances_by_id[self.id] = self
        self.available_internal_connections = -1  # Randomly generated by the group

    @property
    def siblings(self) -> List["Node"]:
        # return all siblings from parent group
        return self.connections

    def get_num_of_connections(self) -> int:
        return len(self.connections)

    def is_fully_internal_connected(self) -> bool:
        if self.available_internal_connections == -1:
            return (
                False  # If this number is -1 the all connections have been established
            )
        return self.available_internal_connections == 0

    def add_connection(self, node_id: str, added_on_target: bool = False) -> bool:
        if node_id not in Node.all_instances_by_id.keys():
            return False
        target = Node.all_instances_by_id[node_id]
        if target in self.connections:
            return False
        self.connections.append(target)
        if not added_on_target:
            target.add_connection(
                self.id, added_on_target=True
            )
        if target.group.id == self.group.id:
            self.available_internal_connections -= 1
        return True

    def has_connection(self, node_id: str) -> bool:
        if node_id not in Node.all_instances_by_id.keys():
            return False
        target = Node.all_instances_by_id[node_id]
        if target in self.connections:
            return True
        return False

    def remove_connection(self, node_id: str, removed_on_target: bool = False) -> bool:
        if node_id not in Node.all_instances_by_id.keys():
            return False
        target = Node.all_instances_by_id[node_id]
        if target not in self.connections:
            return False
        self.connections.remove(target)
        if not removed_on_target:
            target.remove_connection(
                self.id, removed_on_target=True
            )
        if target.group.id == self.group.id:
            self.available_internal_connections += 1
        return True

    def clear_connections(self) -> None:
        for connection in self.connections.copy():
            self.remove_connection(connection.id)
        self.available_internal_connections = -1
        # TODO should the available_connections variable also reset back to -1? If not after a reset the noes will have the same amount of connections

    def infect_node(self) -> None:
        self.infected = True
        self.num_of_infections += 1

    def cure_node(self) -> None:
        self.infected = False

    def __str__(self):
        tmp = f'ID: {self.id}, Connections: ['
        for con in self.connections:
            tmp += f'{con.id}, '
        if tmp.endswith(', '):
            tmp = tmp[0: -2]
        return tmp + ']'
