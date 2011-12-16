#! /usr/bin/env python2

import tvdb_api

db = tvdb_api.Tvdb()

class Node():
    
    def __init__(self, name, obj):
        self.name = name
        self.obj = obj
        self.parent = None
        self.children = []
        
    def __repr__(self):
        return self.parent.__repr__()+"/"+self.name if self.parent else ""
    
    def add(self, node):
        if node.parent == None:
            node.parent = self
        
        self.children.append(node)


root = Node("", None)

for show_name in SHOWS:
    show = db[show_name]
    show_node = Node(show_name, show)
    root.add(show_node)
    
    for season_index in show:
        
        season = show[season_index]
        season_node = Node("s%02d"%(season_index), season)
        show_node.add(season_node)
        
        for episode_index in season:
            
            episode = season[episode_index]
            episode_node = Node("e%02d"%(episode_index), episode)
            season_node.add(episode_node)
            
            print(episode_node)

