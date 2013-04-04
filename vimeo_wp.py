#!/usr/bin/env python
# encoding: utf-8
import json
import oauth2 as oauth
import credentials as cr
import sys
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

usage = '[options] <video_id> <parent_post_id>'
description = '''
Script that takes comments from a vimeo video with a #highlight tag and converts them to wordpress posts
'''

def convert_comments_to_posts(video_id, parent_post_id):
	token = oauth.Token(key=cr.token_key, secret=cr.token_secret)
	consumer = oauth.Consumer(key=cr.consumer_key, secret=cr.consumer_secret)
	url = "http://vimeo.com/api/rest/v2?format=json&method=vimeo.videos.comments.getList&video_id=" + str(video_id) 
	client = oauth.Client(consumer, token)
	resp, content = client.request(url)
	data = json.loads(content)
	process_comments(video_id, parent_post_id, data['comments']['comment'])

def process_comments(video_id, parent_post_id, comments):
	wp = Client(cr.wp_url, cr.wp_user, cr.wp_password)
	for comment in comments:
		if '#highlight' in comment['text']:
			process_comment(wp, video_id, parent_post_id, comment)

def get_post_content(video_id, comment):
	text = comment['text'].replace('#highlight','')
	return '<p>' + text + '</p><iframe src="' + video_url(video_id, text) + '" width="625" height="368" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe><p><a href="' + comment['permalink'] + '">View comment on Vimeo</a> '

def process_comment(wp, video_id, parent_post_id, comment):
	post = WordPressPost()
	post.title = comment['text'][6:50]
	post.content = get_post_content(video_id,comment)
	post.post_type = 'video-highlight'
	post.post_status = 'publish'
	post.parent_id = parent_post_id
	print "Created post with ID [" + wp.call(NewPost(post)) + "]"

def video_url(video_id, comment_text):
	return 'http://player.vimeo.com/video/' + str(video_id) + '#t=' + strip_time(comment_text)   
	
def strip_time(text):
	return text[0:2] + 'm' + text[3:5] + 's'
	
def print_intro():
	print 'VIMEO COMMENTS TO WORDPRESS'
	print description
	print "Usage: " + usage
	print "---------------------"

def main(*argv):
	print_intro()
	convert_comments_to_posts(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	sys.exit(main(*sys.argv))


