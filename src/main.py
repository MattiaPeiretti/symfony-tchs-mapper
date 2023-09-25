import glob
import os
import uuid
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Node:
    id: str
    filepath: str
    type: str
    calls: str
    is_called_by: str
    filename: str
    class_name: str
    file_content: str


@dataclass
class Relation:
    caller: str
    callee: str


NODE_TYPES = [
    'handler',
    'command',
    'subscriber',
    'event',
    'controller'
]

NODETYPE_TO_COLOR = {
    'handler': 'red',
    'command': 'blue',
    'subscriber': 'green',
    'event': 'yellow',
    'controller': 'orange'
}

NODETYPE_WEIGHT = {
    'handler': '50',
    'command': '40',
    'subscriber': '20',
    'event': '30',
    'controller': '100'
}


def getNodeFromId(id_: str, nodes: list) -> Node:
    for node in nodes:
        if node.id == id_:
            return node


def main():
    dir_path = input('select project src directory: ')
    files = glob.glob(dir_path + '/**/*.php',
                      recursive=True)

    nodes = list()

    for file in files:
        base_filename = os.path.basename(file)
        class_name = base_filename.replace('.php', '')

        for node_type in NODE_TYPES:
            if node_type in base_filename.lower():
                with open(file, "r+") as f:
                    # Reading from a file
                    content = f.read()

                nodes.append(Node(str(uuid.uuid4()), file, node_type, '', '', base_filename, class_name, content))

    pprint(nodes)

    relations = list()

    for nodeA in nodes:
        for nodeB in nodes:
            if 'new ' + nodeB.class_name in nodeA.file_content:
                relations.append(Relation(nodeA.id, nodeB.id))

            if '__invoke(' + nodeB.class_name in nodeA.file_content:
                relations.append(Relation(nodeB.id, nodeA.id))

            if nodeB.class_name + '::class' in nodeA.file_content:
                relations.append(Relation(nodeB.id, nodeA.id))

    pprint(relations)

    for node in nodes:
        print(node.class_name + f'[color="{NODETYPE_TO_COLOR[node.type]}"]')
    for relation in relations:
        print(f'{getNodeFromId(relation.caller, nodes).class_name} -> {getNodeFromId(relation.callee, nodes).class_name} [weight={NODETYPE_WEIGHT[getNodeFromId(relation.caller, nodes).type]}]')


if __name__ == '__main__':
    main()
