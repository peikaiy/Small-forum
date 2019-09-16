import time

from django.core.cache import cache
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class IPmiddleware(MiddlewareMixin):

    # -------------------
    # 1. 1533096000.00   t0
    # 2. 1533096000.37   t1
    # 3. 1533096000.95   t2
    # -------------------
    # 4. 1533096000.99   now
    # -------------------
    # 5. 1533096002.03
    # 6. 1533096003.03
    # 7. 1533096004.03
    # 8. 1533096005.03
    # 9. 1533096006.

   def process_request(self, request):
    # 取出用户ip 并设置相关key
    user_ip = request.META["REMOTE_ADDR"]
    request_key = "RequestTime-%s" % user_ip
    ip_key = "IP-%s" % user_ip

    # 检查用户是否被封禁
    if cache.get(ip_key):
        return render(request, "bbs/post/ipfengjin.html")

    # 取出当前时间和历史时间
    now = time.time()
    t0, t1, t2 = cache.get(request_key, [0, 0, 0])

    if (now - t0) < 0.5:
        # 访问过频，封禁
        cache.set(ip_key, 1, 5)
        return render(request, "bbs/post/ipfengjin.html")
    else:
        # 没有封禁，更新访问时间
        cache.set(request_key, [t1, t2, now])



