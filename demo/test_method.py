# coding=utf-8

# 参考https://www.php.cn/python-tutorials-411684.html

import redis
import json, sys
import threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed


class RedisManager:
    MSG_TYPE_READ_BOOK = 0
    MSG_TYPE_PLAY_GAME = 1
    MSG_TYPE_SING_SONG = 2

    def __init__(self):
        self.redisPwd = 123456
        self.redisPort = 6379
        self.redisHost = '127.0.0.1'
        self.connect = self.connectRedis()
        self.connect.flushall()  # 清空redis 所有db
        # self.connect.flushdb()  # 清空当前环境的db

    def connectRedis(self):
        pool = redis.ConnectionPool(host=self.redisHost, port=self.redisPort, password=self.redisPwd, db=0)
        connect = redis.StrictRedis(connection_pool=pool)  # 可以传输已经创建的连接池
        return connect

    def makeMessage(self, m_id, m_type):  # 产生一个消息
        mess_dict = {"id": m_id, "type": m_type}
        return json.dumps(mess_dict)

    def parseMessage(self, js_data):  # 将消息队列中的消息解析成字典
        return json.loads(js_data)

    def pushMsg(self, type):  # 生产消息放进消息队列
        print('push:', type)
        print('push?:', threading.currentThread().name)
        con = self.connectRedis()
        for i in range(1, 10):
            jsonData = self.makeMessage(i, i % 3)  # 生产消息
            print("push message:%s" % jsonData)
            con.lpush('msgQueue', jsonData)

    def handleMsg(self, type):
        print('handle:', type)
        print('handle?:', threading.current_thread().name)
        conn = self.connectRedis()
        print("开始等待消息队列")
        while True:
            msg = conn.brpop("msgQueue")
            print(msg)
            msg = msg[1]
            msg = str(msg, encoding="utf-8")  # 将byte装换为str
            msg_dict = self.parseMessage(msg)
            m_id = msg_dict["id"]
            m_type = msg_dict["type"]
            if m_type == self.MSG_TYPE_PLAY_GAME:
                print("消息{}：我要打游戏".format(m_id))
            elif m_type == self.MSG_TYPE_READ_BOOK:
                print("消息{}：我要读书".format(m_id))
            else:
                print("消息{}：我要唱歌".format(m_id))

    def printSomewords(self, a):
        for i in range(10):
            print("hello: " + a)

    def testQueue(self):
        pushThread = threading.Thread(target=self.pushMsg, name='push_thread', args=(1,))
        handleThread = threading.Thread(target=self.handleMsg, name='hand_thread', args=(2,))
        pushThread.start()
        handleThread.start()
        seed = ['hjh', 'zr', 'zm']
        objList = []
        with ThreadPoolExecutor(3) as excutor:  # 线程池最多同时运行3个线程
            for a in seed:
                # excutor.map() # 可以保证输出顺序
                obj = excutor.submit(self.printSomewords, a)  # 不保证输出顺序
                objList.append(obj)
            for future in as_completed(objList):
                data = future.result()
            print('ThreadPoolExecutor: end')
        print('main thread end')

    def operateMap(self):
        r = self.connectRedis()
        r.hset('n1', 'k1', 'v1')  # hset(name, key, value),name对应的hash中设置一个键值对（不存在，则创建；否则，修改）
        print(r.hget('n1', 'k1').decode("utf-8"))
        r.hmset('n2', {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})  # hmset(name, mapping),在name对应的hash中批量设置键值对
        print(r.hmget('n2', 'k2'))  # [i.decode("utf-8") for i in self.r.hmget(name, args)] args可以为list
        print(r.hgetall('n2'))  # 获取name对应hash的所有键值
        print(r.hlen('n2'))  # 获取name对应的hash中键值对的个数
        print(r.hkeys('n2'))  # 获取name对应的hash中所有的key的值
        print(r.hvals('n2'))  # 获取name对应的hash中所有的value的值
        print(r.hexists('n2', 'k4'))  # 检查name对应的hash是否存在当前传入的key
        r.hdel('n2', 'k3')  # 将name对应的hash中指定key的键值对删除
        r.hset('n3', 'k1', 1)
        r.hincrby('n3', 'k1', amount=1)  # hincrby(name, key, amount=1),自增name对应的hash中的指定key的value的值，不存在则创建key=amount
        print(r.hgetall('n3'))

    def operateList(self):
        r = self.connectRedis()
        r.lpush('oo', 11)  # 保存顺序为: 33,22,11
        r.lpushx('oo', 00)  # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
        print(r.llen('oo'))  # name对应的list元素的个数
        r.linsert('oo', 'before', 11, 99)  # 在11之前插入值99
        r.lset('oo', 1, 88)  # 对name对应的list中的某一个索引位置重新赋值

        print(r.lrange('oo', 0, -1))  # 在name对应的列表分片获取数据
        r.lrem('oo', 88, num=1)  # 在name对应的list中删除指定的值.num=0，删除列表中所有的指定值；num=2,从前到后，删除2个；num=-2,从后向前，删除2个
        print(r.lrange('oo', 0, -1))
        print(r.lpop('oo'))  # 在name对应的列表的左侧获取第一个元素并在列表中移除，返回值则是第一个元素
        print(r.lindex('oo', 0))  # 在name对应的列表中根据索引获取列表元素
        r.lpush('l1', 11)  # index为0
        r.rpush('l1', 22)
        r.rpush('l1', 33)
        r.rpush('l1', 44)
        r.rpush('l1', 55)  # index为4
        r.ltrim('l1', 1, 3)  # 在name对应的列表中移除没有在[start-end]索引之间的值
        print(r.lrange('l1', 0, -1))
        r.rpoplpush('l1', 'l1')  # 从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边;src要取数据的列表的name, dst要添加数据的列表的name
        print(r.lrange('l1', 0, -1))
        r.brpoplpush('l1', 'l1', timeout=3)  # # timeout，当src对应的列表中没有数据时，阻塞等待其有数据的超时时间（秒），0 表示永远阻塞
        print(r.lrange('l1', 0, -1))
        print(r.blpop('l1', 3))  # 从列表头部取出第一个元素，返回该元素值并从列表删除（l代表left，左边）
        print(r.lrange('l1', 0, -1))

        '''
            # 由于redis类库中没有提供对列表元素的增量迭代，如果想要循环name对应的列表的所有元素，那么就需要：
            # 1、获取name对应的所有列表
            # 2、循环列表
            # 但是，如果列表非常大，那么就有可能在第一步时就将程序的内容撑爆，所有有必要自定义一个增量迭代的功能：
        '''

        print('自定义增量迭代：')
        r.flushall()
        r.lpush('l1', 11)  # index为0
        r.rpush('l1', 22)
        r.rpush('l1', 33)
        r.rpush('l1', 44)
        r.rpush('l1', 55)  # index为4

        def list_iter(name):
            list_count = r.llen(name)
            for index in range(list_count):
                yield r.lindex(name, index)

        for item in list_iter('l1'):
            print(item)

    def operateStrings(self):
        r = self.connectRedis()
        r.setex('name', value='hjh', time=2)  # 设置新值，过期时间为3s
        r.mset(k1='v1', k2='v2', k3='v3')  # 批量设置新值
        print(r.mget('k1', 'k2', 'k3', 'k4'))  # 批量获取新值
        print(r.getset('name', 'hjhh'))  # 设置新值并获取原来的值
        print(r.getrange('name', 0, 1))  # 获取子序列 0 <= x <= 1
        r.setrange('name', 0, 'he')  # 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加），返回值的长度
        i = 0

        while i < 4:
            print(r.get('name'))
            time.sleep(1)
            i += 1
        source = 'foo'
        r.set('n1', source)
        r.setbit('n1', 7, 1)

        '''
        注：如果在Redis中有一个对应： n1 = "foo"，
            那么字符串foo的二进制表示为：01100110 01101111 01101111
            所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，
            那么最终二进制则变成 01100111 01101111 01101111，即："goo"
        '''
        print(r.get('n1'))
        print(r.getbit('n1', 7))  # 获取n1对应的值的二进制表示中的某位的值 （0或1）
        r.set('n2', 'hjh')
        print(r.strlen('n2'))  # 返回对应的字节长度（一个汉字3个字节）
        r.set('num', 1)
        r.incr('num', amount=10)
        r.decr('num', amount=1)
        print(r.get('num'))  # 自增num对应的值，当name不存在时，则创建name＝amount，否则，则自增。
        r.append('num', 111)
        print(r.get('num'))  # 在redis num对应的值后面追加内容

    def operateSet(self):
        r = self.connectRedis()
        r.sadd('s1', 'v1', 'v1', 'v2', 'v3')  # name对应的集合中添加元素
        r.sadd('s2', 'v2', 'v4')  # name对应的集合中添加元素
        print(r.scard('s1'))  # 获取name对应的集合中元素个数
        print(r.sdiff('s1', 's2'))  # 在第一个name对应的集合中且不在其他name对应的集合的元素集合
        r.sdiffstore('s3', 's1', 's2')  # 获取第一个name对应的集合中且不在其他name对应的集合，再将其新加入到dest对应的集合中
        print(r.smembers('s3'))  # 获取s3对应的集合的所有成员
        print(r.sinter('s1', 's2'))  # 获取s1, s2对应集合的交集
        r.sinterstore('s4', 's1', 's2')  # 获取s1, s2对应集合的交集，并将其存放到集合是s4中
        print(r.smembers('s4'))
        print(r.sunion('s1', 's2'))  # 获取s1, s2对应集合的并集
        r.sunionstore('s5', 's1', 's2')  # 获取s1, s2对应集合的交集，并将其存放到集合是s5中
        print(r.smembers('s5'))
        print(r.sismember('s4', 'v4'))  # 检查value是否是name对应的集合的成员
        r.smove('s2', 's1', 'v4')  # 将集合s2中成员v4移至集合s1中
        print(r.smembers('s1'))
        r.srem('s1', 'v1')  # 在name对应的集合中删除某些值
        print(r.spop('s1'))  # 从集合的右侧（尾部）移除一个成员，并将其返回 注意：集合是无序的，故结果随机！
        print(r.srandmember('s1'))  # 从name对应的集合中随机获取 numbers 个元素(Redis 2.6+)

    def operateSortSet(self):
        r = self.connectRedis()
        r.zadd('z1', '11', 1, '22', 2, '33', 3, '44', 4, '55', 5, '66', 6, '66', 7)  # 在name对应的有序集合中添加元素
        print(r.zcard('z1'))  # 获取name对应的有序集合元素的数量
        print(r.zcount('z1', 1, 2))  # 获取name对应的有序集合中分数 在 [min,max] 之间的个数
        r.zincrby('z1', '11', amount=5)  # 自增name对应的有序集合的 name 对应的分数
        print(r.zrange('z1', 0, -1, desc=False, withscores=True))  # 值11被排序到最后;此处表示按元素的值升序排列
        print(r.zrank('z1', 33))  # 获取某个值在 name对应的有序集合中的排行（从 0 开始）
        r.zrem('z1', '66')  # 删除name对应的有序集合中值是values的成员
        print(r.zrange('z1', 0, -1, desc=False, withscores=True))
        r.zremrangebyrank('z1', 0, 1)  # 根据排行范围删除
        print(r.zrange('z1', 0, -1, desc=False, withscores=True))
        r.zremrangebyscore('z1', 4.5, 5.5)  # 根据分数范围删除
        print(r.zrange('z1', 0, -1, desc=False, withscores=True))
        print(r.zscore('z1', 11))  # 获取name对应有序集合中 value 对应的分数
        r.zadd("zset_name", "a1", 6, "a2", 2, "a3", 5)
        r.zadd('zset_name1', a1=7, b1=10, b2=5)

        '''
            获取两个有序集合的交集并放入dest集合，如果遇到相同值不同分数，则按照aggregate进行操作
            aggregate的值为: SUM  MIN  MAX
        '''

        r.zinterstore('zset_name2', ('zset_name', 'zset_name1'), aggregate='Sum')
        print(r.zrange('zset_name2', 0, -1, desc=False, withscores=True))


def redisTest():
    manager = RedisManager()
    manager.testQueue()
    pass


if __name__ == '__main__':
    redisTest()
