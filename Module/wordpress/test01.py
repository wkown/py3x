# -*- coding:utf-8 -*-

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

wp = Client('http://wordpress.tst/xmlrpc.php', 'admin', '123')
print(wp.call(GetPosts()))

print(wp.call(GetUserInfo()))

post = WordPressPost()
post.title = 'My new title'
post.content = 'This is the body of my new post.'
post.terms_names = {
  'post_tag': ['test', 'firstpost'],
  'category': ['Introductions', 'Tests']
}
wp.call(NewPost(post))

if __name__ == "__main__":
    pass