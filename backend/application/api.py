from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="ninja-extra API",
    description="ninja-extra",
    urls_namespace="ninja",
)


# 统一处理server异常
@api.exception_handler(Exception)
def a(request, exc):
    if hasattr(exc, 'errno'):
        std_data = {
            "code": exc.errno,
            "result": [],
            "message": str(exc),
            "success": True
        }
        return api.create_response(request, data=std_data)
    else:
        std_data = {
            "code": 500,
            "result": [],
            "message": str(exc),
            "success": True
        }
        return api.create_response(request, data=std_data)


api.auto_discover_controllers()
