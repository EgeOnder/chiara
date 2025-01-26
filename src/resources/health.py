from flask_restful import Resource


class HealthCheck(Resource):
    def get(self):
        return {"status": "healthy", "message": "API is running"}
