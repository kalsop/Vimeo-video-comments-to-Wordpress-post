#!/usr/bin/env python
# encoding: utf-8
"""
Script that takes comments from a vimeo video with a #highlight tag and converts them to wordpress posts.
"""

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import codecs
import credentials as cr
import json
import locale
import logging
import oauth2 as oauth
import optparse
import os
import sys
import warnings

__author__ = '$USER'
__version__="0.1"

script_name = os.path.basename(sys.argv[0])
usage = '[options] <video_id> <parent_post_id>'
description = '''
Script that takes comments from a vimeo video with a #highlight tag and converts them to wordpress posts.
'''

logger = logging.getLogger(script_name)

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
    #logger.info("Created post with ID [%s]", wp.call(NewPost(post)))
    print "Created post with ID [%s]" % wp.call(NewPost(post))

def video_url(video_id, comment_text):
    url = 'http://player.vimeo.com/video/%s#t=%s' % (video_id, strip_time(comment_text))
    logger.debug("Video URL: %s", url)
    return url

def strip_time(text):
    return text[0:2] + 'm' + text[3:5] + 's'

def get_options(argv):
    '''Get options and arguments from argv string.'''
    parser = optparse.OptionParser(usage=usage, version=__version__)
    parser.description=description
    parser.add_option("-v", "--verbosity", action="count", default=0,
        help="Specify up to three times to increase verbosity, i.e. -v to see warnings, -vv for information messages, or -vvv for debug messages.")
    
    # Extra script options here...
    
    options, args = parser.parse_args(list(argv))
    script, args = args[0], args[1:]
    return options, script, args, parser.format_help()

def init_logger(verbosity, stream=sys.stdout):
    '''Initialize logger and warnings according to verbosity argument.
    Verbosity levels of 0-3 supported.'''
    is_not_debug = verbosity <= 2
    level = [logging.ERROR, logging.WARNING, logging.INFO][verbosity] if is_not_debug else logging.DEBUG
    format = '%(message)s' if is_not_debug else '%(asctime)s %(levelname)-8s %(name)s %(module)s.py:%(funcName)s():%(lineno)d %(message)s'
    logging.basicConfig(level=level, format=format, stream=stream)
    if is_not_debug: warnings.filterwarnings('ignore')

def wrap_stream_for_tty(stream):
    if stream.isatty():
        # Configure locale from the user's environment settings.
        locale.setlocale(locale.LC_ALL, '')
        
        # Wrap stdout with an encoding-aware writer.
        lang, encoding = locale.getdefaultlocale()
        logger.debug('Streaming to tty with lang, encoding = %s, %s', lang, encoding)
        if encoding:
            return codecs.getwriter(encoding)(stream)
        else:
            logger.warn('No tty encoding found!')
    
    return stream

def main(*argv):
    options, script, args, help = get_options(argv)
    init_logger(options.verbosity)
    convert_comments_to_posts(args[0], args[1])

if __name__ == '__main__':
    sys.exit(main(*sys.argv))


