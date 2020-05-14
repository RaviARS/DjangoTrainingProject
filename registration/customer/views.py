from .models import Customer
from .serializers import CustomerSerializers
from .tasks import celery_task
import paho.mqtt.client as mqtt
from django.conf import settings
import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


def publish_mqtt_msg(topic, mqtt_msg):
    """  To publish the message to Mqtt broker """

    MQTT_HOST = settings.MQTT_HOST
    MQTT_PORT = settings.MQTT_PORT
    MQTT_KEEPALIVE_INTERVAL = settings.MQTT_KEEPALIVE_INTERVAL

    MQTT_TOPIC = topic

    MQTT_MSG = json.dumps(mqtt_msg)

    """  Celery task to create a password for the user """

    celery_task.delay(MQTT_MSG)

    def on_publish(client, userdata, mid):
        print("Message Published...")

    def on_connect(client, userdata, flags, rc):
        client.subscribe(MQTT_TOPIC)
        client.publish(MQTT_TOPIC, MQTT_MSG)

    def on_message(client, userdata, msg):
        print(msg.topic)
        print(msg.payload)
        payload = json.loads(msg.payload)
        print(payload['sepalWidth'])
        client.disconnect()

    mqttc = mqtt.Client()
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


class CustomerList(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializers(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetails(APIView):

    def get_boject(self, id):
        try:
            return Customer.objects.get(id=id)

        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        customer = self.get_boject(id)
        serializer = CustomerSerializers(customer)
        print(serializer.data)

        publish_mqtt_msg("notificationPayload", serializer.data)

        return Response(serializer.data)

    def put(self, request, id):
        customer = self.get_boject(id)
        serializer = CustomerSerializers(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        customer = self.get_boject(id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
