use flaskapis;
db.sensors.drop()
db.sensors.insert(
        { "_id" : "000006c01f0b",
          "serial" : "000006c01f0b",
          "geolocation" : "51.5033630,-0.1276250",
          "location" : "Living Room",
          "address" : "2800 BRAZOS BLVD, EULESS, TX - USA",
          "state" : "UP",
          "name" : "DS18B20",
          "type" : "TEMPERATURE",
          "description": "Dallas Semiconductor digital temperature sensor"
         } );
db.sensors.insert(
        { "_id" : "testing",
          "serial" : "testing",
          "geolocation" : "51.5033630,-0.1276250",
          "location" : "Living Room",
          "address" : "2800 BRAZOS BLVD, EULESS, TX - USA",
          "state" : "UP",
          "name" : "DS18B20",
          "type" : "TEMPERATURE",
          "description": "Dallas Semiconductor digital temperature sensor"
         } );
