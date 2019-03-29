#! /usr/bin/env python
# -*- coding:utf-8 -*-

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--title', type=str, default='My new title', help="Post Title")
parser.add_argument('-c', '--content', type=str, default='This is the body of my new post.', help='Post Content')
args = parser.parse_args()

wp = Client('http://wordpress.tst/xmlrpc.php', 'admin', '123')
print('Get Posts:')
print(wp.call(GetPosts()))
print('Current User:')
print(wp.call(GetUserInfo()))
print("Publish a New Post:")
post = WordPressPost()
post.title = args.title.encode(encoding='utf-8')
post.content = args.content.encode(encoding='utf-8')
post.terms_names = {
  'post_tag': ['test', 'firstpost'],
  'category': ['Introductions', 'Tests']
}
post.post_status = 'publish'
wp.call(NewPost(post))
print('Publish Done.')

if __name__ == "__main__":
    pass