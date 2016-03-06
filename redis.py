import redis

class RedisHandler:

    def __init__(self, settings):
        """
        Connects to redis instance
        :param settings: hostname, port, password
        :return: nothing
        """

        self.r = redis.Redis(
            host=settings['hostname'],
            port=settings['port']
        )

        # set the redis list name for storing jobs
        self.joblist = settings['joblistname']


    def get_next(self):
        """
        Gets the next item in the list
        :return: the item or 0 if nothing
        """

        # pop the next item off the front of the list
        item = self.r.lpop(self.joblist)

        # if nothing comes out of the list, then it's empty and return 0
        # otherwise return whatever is next
        if not item:
            return 0
        else:
            return item


    def add_to_queue(self, items):
        """
        Add items list to the redis list
        :param items: list of items to be added
        :return: nothin
        """

        for i in items:
            self.r.rpush(self.joblist, i)

    def lpush(self, item):
        """
        pushes the item back onto the front of the queue
        :param item:
        :return:  nothing
        """

        self.r.lpush(self.joblist, item)

    def get_list_size(self):
        """
        returns the size of the redis queue
        :return: how many items are in the queue
        """

        return self.r.llen(self.joblist)