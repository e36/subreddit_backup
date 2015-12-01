import praw


def get_post_data(reddit_session, thread_id):
    """
    Gets all comments and post data from a thread.
    :param thread_id: reddit thread ID
    :return: flat comments and post data
    """

    # init containers where we will hold the thread info)
    thread_data = dict()

    # status stuff
    print('Getting thread ' + thread_id)

    # get thread info and add to thread_list
    print('Getting thread information.')

    # get submission
    thread = reddit_session.get_submission(submission_id=thread_id)

    thread_data = dict(created_utc=thread.created_utc, id=thread.id, name=thread.name, domain=thread.domain,
                       link_flair_text=thread.link_flair_text, num_comments=thread.num_comments,
                       permalink=thread.permalink, score=thread.score, selftext=thread.selftext,
                       selftext_html=thread.selftext_html, title=thread.title, upvote_ratio=thread.upvote_ratio)

    # test for author, because if the thread is deleted then the author will simply be none
    if thread.author:
        thread_data['author'] = thread.author
    else:
        thread_data['author'] = '[DELETED]'

    # convert the archived value from True/False to 1/0
    if thread.archived:
        thread_data['archived'] = 1
    else:
        thread_data['archived'] = 0

    # return
    return thread_data


def get_comments(reddit_session, thread_id):
    """
    Gets all comments for a particular thread_id
    :param reddit_session: praw session for connecting to reddit
    :param thread_id: the thread id (not name) to be captured
    :return: A list of flat comment data
    """

    print('Getting comment data.')

    # init list of comment data to be returned
    comment_list = []

    # init the 'already done' set
    already_done = set()

    # get submission
    thread = reddit_session.get_submission(submission_id=thread_id)

    # get comments and flatten
    thread.replace_more_comments(limit=None, threshold=1)
    # comments = thread.comments
    flat_comments = praw.helpers.flatten_tree(thread.comments)

    # iterate through comments and add them to comment list before adding to thread_list for json serialization
    for comment in flat_comments:

        comment_dict = dict()

        if comment.id not in already_done:

            comment_dict = dict(created_utc=comment.created_utc, body=comment.body, body_html=comment.body_html,
                                id=comment.id, link_id=comment.link_id, name=comment.name, parent_id=comment.parent_id,
                                score=comment.score)

            # check for author == None for deleted comments
            if comment.author:
                comment_dict['author'] = comment.author.name
            else:
                comment_dict['author'] = '[Deleted]'

            already_done.add(comment.id)
            comment_list.append(comment_dict)

    # return
    return comment_list


def get_posts(reddit_session, subreddit_name):
    """
    Gets thread IDs and thread data from as many posts as possible.  Since praw/reddit won't allow more than 1,000
    results from methods like get_top_from_all we're going to run the following:
        get_top_from_all
        get_hot
        get_controversial
        get_rising
        get_new
    We'll grab all unique posts and process them for entirely new posts, or updated to existing posts in the database.
    :param reddit_session:
    :param subreddit:
    :return:
    """

    print("Getting posts.")

    # init lists and sets
    thread_data_list = dict()
    thread_data_dict = dict()
    already_done = []

    # init praw objects
    subreddit = reddit_session.get_subreddit(subreddit_name)

    thread_data_dict['top'] = subreddit.get_top_from_all(limit=None)
    thread_data_dict['hot'] = subreddit.get_hot(limit=None)
    thread_data_dict['rising'] = subreddit.get_rising(limit=None)
    thread_data_dict['controversial'] = subreddit.get_controversial(limit=None)
    thread_data_dict['hot'] = subreddit.get_new(limit=None)

    # iterate through the dictionary and all posts
    # make sure that only unique posts are captured.  This will grab ALL post data, so we will have to pare that down
    # at another time
    for key in thread_data_dict:

        # crawl through each post in this key
        for post in thread_data_dict[key]:

            if post.id not in already_done:
                # if this post id (i.e. 'cz4j2') isn't in already_done, then we haven't added it to the list yet
                # add the post id to already_done so we don't hit it again
                # add the post object to thread_data_list[post.id]
                already_done.append(post.id)
                thread_data_list[post.id] = post

    print("{0} posts found.".format(len(thread_data_list)))

    # return
    return thread_data_list


