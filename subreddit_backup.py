__author__ = 'e36'
__version__ = '0.5'


import praw
import json

print('***Subreddit Backup***')

# TODO: Create a new method of inputting post IDs.  I'd like to be able to specify a list of IDs.
thread_id = '33qfpf'    # we're just going to use this one for now, so I don't have to keep tying it in

# init praw stuff
r = praw.Reddit(user_agent='backup script by /u/e36')

# get submission
thread = r.get_submission(submission_id=thread_id)

# get top comments
# this will look at all parent comments and get their score, and read off the top 10

# init containers where we will hold the thread info
thread_list = dict()
comment_list = []

# init the 'already done' set
already_done = set()

# status stuff
print('Getting thread ' + thread_id)

# get comments and flatten
thread.replace_more_comments(limit=None, threshold=1)
# comments = thread.comments
flat_comments = praw.helpers.flatten_tree(thread.comments)

# get thread info and add to thread_list
print('Getting thread information.')
thread_data = {
    'created_utc': thread.created_utc,
    'id': thread.id,
    'name': thread.name,
    'author': thread.author.name,
    'domain': thread.domain,
    'link_flair_text': thread.link_flair_text,
    'num_comments': thread.num_comments,
    'permalink': thread.permalink,
    'score': thread.score,
    'selftext': thread.selftext,
    'selftext_html': thread.selftext_html,
    'title': thread.title,
    'upvote_ratio': thread.upvote_ratio,
}

# iterate through comments and add them to comment list before adding to thread_list for json serialization
print('Getting comment data.')
for comment in flat_comments:

    comment_dict = dict()

    if comment.id not in already_done:

        comment_dict = {
            'created_utc': comment.created_utc,
            'body': comment.body,
            'body_html': comment.body_html,
            'id': comment.id,
            'link_id': comment.link_id,
            'name': comment.name,
            'parent_id': comment.parent_id,
            'score': comment.score,
        }

        # check for author == None for deleted comments
        if comment.author != None:
            comment_dict['author'] = comment.author.name
        else:
            comment_dict['author'] = 'None'

        already_done.add(comment.id)
        comment_list.append(comment_dict)

# add it to thread_list
thread_list['thread_data'] = thread_data
thread_list['comments'] = comment_list

# create file name from thread data, and save the json dump
filename = thread_data['author'] + '-' + thread_data['id'] + '.json'

f = open(filename, 'w')
f.write(json.dumps(thread_list))
f.close()

print('Done.')

