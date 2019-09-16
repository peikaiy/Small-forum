from redis import Redis
from BBS import settings
# 连接redis
rds = Redis(**settings.REDIS)