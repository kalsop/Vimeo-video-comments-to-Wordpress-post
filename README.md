Vimeo Video Comments To Wordpress Post
======================================

This Python script takes comments (containing the text '#highlight') from publicly available Vimeo videos and converts them to Wordpress posts with the Vimeo video embedded. 

A separate file called 'credentials.py' will need to be created in the script directory in the following format:

```python
wp_user = [Wordpress username]
wp_password = [Wordpress password]
wp_url = [Wordpress URL>/xmlrpc.php]
token_key = [Vimeo API token key]
token_secret = [Vimeo API token secret]
consumer_key = [Vimeo API consumer key]
consumer_secret = [Vimeo API consumer secret]
```



Usage: ```python vimeo_wp.py <video_id> <parent_post_id>```

[Katherine Alsop](http://github.com/kalsop) / [John Cowie](http://github.com/johncowie)



Copyright (C) 2013 Government Digital Service

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



