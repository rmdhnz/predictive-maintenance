#!/usr/bin/env python3

from src.model.PostModel import PostModel

def app() : 
    post = PostModel('posts')
    data = post.findAll()
    for row in data:
        print(row)  
    post.close()