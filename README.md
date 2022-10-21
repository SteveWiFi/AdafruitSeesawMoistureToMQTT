# AdafruitSeesawMoistureToMQTT
Sending MQTT data for Adafruit's Seesaw Soil Moisture Sensor https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test

**Dependencies**

Requires the Adafruit Seesaw library. It can be installed via pip3:

    sudo pip3 install adafruit-circuitpython-seesaw

You'll also need PyYAML which you can also get via pip3:

    sudo pip3 install pyyaml
    
I also installed the Python3 Paho MQTT library on Raspberry Pi OS:

    sudo apt-get install python3-paho-mqtt

If you'd like to create a systemd service, pop it into /etc/systemd/system/ as say temperature-and-moisture-sensor.service with the following text:

    [Unit]
    Description=python script to run the temp and soil sensor
    After=network-online.target

    [Service]
    ExecStart=python /home/username/adafruit-moisture-sensor-mqtt.py
    Type=simple

    [Install]
    WantedBy=network-online.target
    
Please remember to use absolute paths to locations (especially in the Python script since it's relative), if you wish to run it as a systemd service. This includes the config file.

Once you've added the script, run the following commands:

    systemctl daemon-reload
    
    systemctl enable temperature-and-moisture-sensor.service
    
    systemctl start temperature-and-moisture-sensor.service

That should be it!

If you'd like to integrate it into Home Assistant (https://www.home-assistant.io), you can also add this to your configuration.yaml file:

    mqtt:
      sensor:
        - name: "Adafruit Shed Greenhouse Temperature"
          state_topic: "shed/seesaw/temperature"
          unit_of_measurement: "°C"
        - name: "Adafruit Shed Greenhouse Moisture"
          state_topic: "shed/seesaw/moisture"
          unit_of_measurement: "%"
