from django.utils.deprecation import MiddlewareMixin


class MyCors(MiddlewareMixin):
    def process_response(self, requesst, response):
        response['Access-Control-Allow-Origin'] = '*'
        if requesst.method == 'OPTIONS':
            response["Access-Control-Allow-Headers"] = "*"
            response['Access-Control-Allow-Methods'] = 'PUT,DELETE'
        return response
