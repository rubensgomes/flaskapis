=========================
The MQ - Message Queueing
=========================

This project is using the Active MQ - messaging queueing server for
integration.

This project uses an IoT gateway (Raspberry Pi, in this case) that
periodically reads data from the DS18B20 sensor.  And then it publishes
the sensor readings to a topic in the Active MQ server.  The MQTT protocol is
used to publish the sensor reading information messages to the Active MQ
server.

Requirements
------------

ActiveMQ 5.11.1 (or above)


Configuration
-------------

Install Active MQ 5.11.1 (or above).

Ensure that you have the following settings in the activemq.xml file:

<managementContext>
  <managementContext createConnector="true"/>
</managementContext>

Then, start the application server according the ActiveMQ docs.

Once the ActiveMQ server is up and running, it will create publish/subscribe
TOPIC destinations on demand.  The TOPIC name being used by the IoT application
is defined in the application.ini file.


