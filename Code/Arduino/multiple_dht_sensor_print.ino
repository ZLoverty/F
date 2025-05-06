// This sketch reads the humidity / temperature data from multiple DHT sensors.
// It also sends out digital signal to the nebulizer and peltier relays.
// Nebulizer control is based on the humidity data.
// Peltier control is based on preset time cycles. 

#include "DHT.h"

// User settings
// humidity settings


////////////////
int h_low = 85;
int h_high = 95;
///////////////


// temperature time cycle

long t_room = 30; // minutes at room temperature, peltier off
long t_low = 30; // minutes at low temperature, peltier onM



// long t_total = 100; // minutes of the whole experiment, not implemented
// signal pin number
int nebulizer_pin = 12;
int peltier_pin = 11;
// sensor, pin mapping
DHT sensors[8] = {DHT(9, DHT11),
                  DHT(2, DHT11),
                  DHT(3, DHT11),
                  DHT(4, DHT11),
                  DHT(5, DHT11),
                  DHT(6, DHT11),
                  DHT(7, DHT11),
                  DHT(8, DHT11),};

DHT sensor1 = sensors[0];
DHT sensor2 = sensors[1];

// flags
int nebulizer_switch = false;
int peltier_switch = true;
// start time (in millisecond)
long t0 = millis();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  sensor1.begin();
  sensor2.begin();
  pinMode(nebulizer_pin, OUTPUT);
  pinMode(peltier_pin, OUTPUT);
  digitalWrite(nebulizer_pin, LOW);
  digitalWrite(peltier_pin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(10000);
  long t_now = millis();
  Serial.print(String((t_now-t0)/1000) + ",");
  // read DHT sensor data
  
  float T = sensor1.readTemperature();
  float H1 = sensor1.readHumidity(); 
  float H2 = sensor2.readHumidity();
  float H = H2;//(H1 + H2) / 2.0;
  Serial.print(String(T) + "," + String(H));

  bool evaporation_cycle = (t_now-t0)%((t_room+t_low)*60*1000) >= t_low*60*1000;
  bool condensation_cycle = (t_now-t0)%((t_room+t_low)*60*1000) < t_low*60*1000;

  // control nebulizer
  if (H < h_low & nebulizer_switch == false & condensation_cycle) { // if humidity is lower than set low value, turn on nebulizer
    digitalWrite(nebulizer_pin, HIGH);
    nebulizer_switch = true;
  }
  if (H >= h_high) {// if humidity is higher than set high value, turn off nebulizer
    digitalWrite(nebulizer_pin, LOW);
    nebulizer_switch = false;
  }
  Serial.print(",nebu " + String(nebulizer_switch));

  // control peltier
  // somehow, the IN1 in the relay triggers when connected to GND
  // so here, when signal is LOW, the relay 1 is triggered
  // take caution with this counter intuitive relay
  
  if (evaporation_cycle & peltier_switch == true) {
    digitalWrite(peltier_pin, HIGH);
    peltier_switch = false;
  } 
  if (condensation_cycle & peltier_switch == false) {
    digitalWrite(peltier_pin, LOW);
    peltier_switch = true;
  }
  Serial.print(",peltier " + String(peltier_switch) + "\n");
  

  // }
}