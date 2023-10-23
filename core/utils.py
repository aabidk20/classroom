def response_payload(success: bool, data=None, message=None):
    if success:
        return {
            "success": True,
            "message": message,
            "data": data,
        }
    else:
        return {
            "success": False,
            "message": message,
            "errors": data,
        }
