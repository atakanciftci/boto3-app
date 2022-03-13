from flask import Flask, jsonify, request
from flask_restx import Api, Resource
import boto3
from config import config
app = Flask(__name__)
api = Api(app)
import logging

logging.basicConfig(filename='record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@api.route('/ec2/list')
class Ec2List(Resource):

    def post(self):

        data = request.get_json()
        aws_access_key_id = data.get("aws_access_key_id")
        aws_secret_access_key = data.get("aws_secret_access_key")
        region_name = data.get("region_name")

        if aws_access_key_id is None or aws_secret_access_key is None or region_name is None:

            return {"message":"Bad request","status":"400"},400

        else:
            try:
                client = boto3.client('ec2',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                )

                response = client.describe_instances()


                instance_ids = []
                for id in range(len(response["Reservations"])):
                    instance_ids.append(response['Reservations'][id]['Instances'][0]['InstanceId'])


            except:
                
                return {"message":"Something got wrong!","status":"401"},401


        return {"instance_ids":instance_ids},200


@api.route("/ec2/start")
class Ec2Start(Resource):

    def post(self):

        data = request.get_json()


        aws_access_key_id = data.get("aws_access_key_id")
        aws_secret_access_key = data.get("aws_secret_access_key")
        region_name = data.get("region_name")
        instance_id = data.get("instance_id")

        if aws_access_key_id is None or aws_secret_access_key is None or region_name is None or instance_id is None:

            return {"message":"Bad request","status":"400"},400

        else:
            try:
                client = boto3.client('ec2',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name
                )

                response = client.start_instances(InstanceIds=instance_id)
            
            except:

                return {"message":"Something got wrong!","status":"401"},401


        return response


@api.route("/ec2/stop")
class Ec2Stop(Resource):


    def post(self):
            data = request.get_json()

            aws_access_key_id = data.get("aws_access_key_id")
            aws_secret_access_key = data.get("aws_secret_access_key")
            region_name = data.get("region_name")
            instance_id = data.get("instance_id")

            if aws_access_key_id is None or aws_secret_access_key is None or region_name is None or instance_id is None:

                
                return {"message":"Bad request","status":"400"},400
            
            else:
                try:
                    client = boto3.client('ec2',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name
                    )

                    response = client.stop_instances(InstanceIds=instance_id)
                
                except:
                    return {"message":"Something got wrong!","status":"401"},401
                    

            return response


if __name__ == '__main__':
    app.run(host=config["host"],port=config["port"],debug=True)
