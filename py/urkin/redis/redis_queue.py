import redis


class RedisQueueHelper:

    def __init__(self):
        print("init redis client")
        self.client = redis.Redis(
                        host="localhost",
                        port=6379,
                        password="pass"
                        )
        print("init redis client success")

    def push_notification(self, userid, notification):
        self.client.lpush(userid, notification)

    def get_notifications(self, userid):
        notification_len = self.client.llen(userid)

        notifications = []
        for i in range(1, notification_len):
            notifications.append(self.client.lpop(userid))

        return notifications

if __name__ == "__main__":

    r = RedisQueueHelper()
    r.push_notification(123, "test1")
    r.push_notification(123, "test2")
    r.push_notification(123, "test3")
    r.push_notification(123, "test4")

#    print(r.get_notifications(123))
