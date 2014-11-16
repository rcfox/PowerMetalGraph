import json
import networkx as nx
from pprint import pprint

data = []
with open('scraper/items.json') as f:
    data.extend(json.load(f))

nodes = {}

status_colours = {'Active': 'green',
                  'Unknown': 'green',
                  'On hold': 'red',
                  'Split-up': 'red',
                  'Changed name': 'orange'}

relation_colours = {'Current': 'green',
                    'Current (Live)': 'green',
                    'Last known': 'green',
                    'Last known (Live)': 'green',
                    'Past': 'red',
                    'Past (Live)': 'red'}

relation_weights = {'Current': 1.2,
                    'Current (Live)': 1,
                    'Last known': 1.2,
                    'Last known (Live)': 1,
                    'Past': 0.8,
                    'Past (Live)': 0.5}


G = nx.Graph()
for band in data:
    bid = band['band_id']
    if bid not in nodes:
        name = band['name']
        status = band['status']
        G.add_node(bid, label=name, color=status_colours[status])
        nodes[bid] = True

    for member_type, members in band['members'].items():
        for member in members:
            mid = member['member_id']
            if mid not in nodes:
                G.add_node(mid, label=member['name'], color='blue')
                nodes[mid] = True
            G.add_edge(bid, mid,
                       color=relation_colours[member_type])

for i, subgraph in enumerate(nx.connected_component_subgraphs(G)):
    if len(subgraph.nodes()) > 200:
        print 'graph %d' % i
        H = subgraph.subgraph([n for n in subgraph if G.degree(n) > 1])
        nx.write_dot(H, 'graph%d.dot' % i)
