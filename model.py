from relation import Relator
from relation.map import create_graph
from pyvis.network import Network

class Subject:
    def __init__(self, name, string=""):
        self.name = name
        self.topics = {}
        self.convert_from_string(string)
        # self.verbs = set()
        # self.adjectives = set()
    def get(self, name, relations=None, children=None, parents=None):
        if name in self.topics:
            existing = self.topics[name]
            existing |= Topic(name, relations, children, parents)
            return existing
        else:
            instance = Topic(name, relations, children, parents)
            self.topics[name] = instance
            return instance
    def convert_from_string(self, str):
        sentences = str.splitlines()
        for sentence in sentences:
            if ":" in sentence:
                parts = sentence.split(":")
                topic_name = parts[0].strip()
                description = parts[1].strip()
                if ">" in description:
                    desc_parts = description.split(">")
                    function_name = desc_parts[0].strip()
                    topic2_name = desc_parts[1].strip()
                    topic = self.get(topic_name)
                    topic * Description(function_name, children=[self.get(topic2.strip()) for topic2 in topic2_name.split(",")])
                    # self.verbs.add(function_name)
                else:
                    topic = self.get(topic_name)
                    for desc in description.split(","):
                        desc = desc.strip()
                        topic * Description(desc)
                        # self.adjectives.add(desc)
            elif ">" in sentence:
                parts = sentence.split(">")
                topic_name = parts[0].strip()
                topic2_name = parts[1].strip()
                topic = self.get(topic_name)
                topic + [self.get(topic2.strip()) for topic2 in topic2_name.split(",")]
    def make_graph(self):
        graph = Network(directed=True)
        visited = set()
        drawn_edges = set()
        for topic in self.topics.values():
            create_graph(topic, net=graph, visited=visited, drawn_edges=drawn_edges)
        return graph
    
    def convert_to_string(self):
        """Convert the subject's relations back to string format."""
        lines = []
        
        for topic in self.topics.values():
            # Handle direct children relationships (Topic > Child1, Child2)
            if hasattr(topic, 'children') and topic.children:
                children_names = [child.name for child in topic.children]
                lines.append(f"{topic.name} > {', '.join(children_names)}")
            
            # Handle descriptions/relations
            if hasattr(topic, 'relations') and topic.relations:
                for relation in topic.relations:
                    if hasattr(relation, 'name'):
                        # Check if this description has children (Topic: description > Child1, Child2)
                        if hasattr(relation, 'children') and relation.children:
                            children_names = [child.name for child in relation.children]
                            lines.append(f"{topic.name}: {relation.name} > {', '.join(children_names)}")
                        else:
                            # Simple description (Topic: description)
                            lines.append(f"{topic.name}: {relation.name}")
        
        return '\n'.join(lines)
        

class Topic(Relator):
    def make_graph(self):
        graph = create_graph(self)
        return graph

class Description(Relator):
    pass

