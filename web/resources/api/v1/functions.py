from flask import request
from time import time


class IPRequestTimeout:
    ip_requests = dict()
    REQUEST_LIMIT_DURATION_SECONDS = 0

    @staticmethod
    def check_ip():
        ip_address = request.remote_addr

        if ip_address in IPRequestTimeout.ip_requests and time() - IPRequestTimeout.ip_requests[
            ip_address
        ] < IPRequestTimeout.REQUEST_LIMIT_DURATION_SECONDS:
            return False

        IPRequestTimeout.ip_requests[ip_address] = time()
        return True
