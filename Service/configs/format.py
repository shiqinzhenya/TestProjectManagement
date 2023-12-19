#format.py
#创建一个统一的格式类， 统一response的返回

resp_format_success = {
    "code": 20000,
    "message": "success",
    "data": [],
    "total": 0
}

resp_format_failed = {
    "code": 20001,
    "message": "failed"
}