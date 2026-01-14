class Graf:
    def __init__(self):
        self.graf = {}

    def add_edge(self, u, v):
        if u not in self.graf:
            self.graf[u] = []
        self.graf[u].append(v)


    def print_graf(self):
        for node in self.graf:
            print(node, "->", " -> ".join(map(str, self.graf[node])))

g = Graf()
g.add_edge(0, 1)
g.add_edge(0, 4)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 3)
g.add_edge(3, 4)


g.print_graf()
