#include <DHT.h>  // Biblioteca para el sensor de temperatura y humedad DHT11 o DHT22
#include <Wire.h> // Para la comunicación con sensores de altitud
#include <Adafruit_Sensor.h> 
#include <Adafruit_BME280.h> // Sensor de temperatura, humedad y presión barométrica
#include <MQ135.h> // Sensor MQ para CO2
#include <MQ7.h> // Sensor MQ para CO

// Definir pines de los sensores
#define DHTPIN 2        // Pin del DHT (sensor de temperatura y humedad)
#define DHTTYPE DHT11   // Tipo de sensor DHT (puede ser DHT22 o DHT11)
#define BME280_I2C_ADDR 0x76 // Dirección I2C del sensor BME280 (para altitud, temperatura, humedad)

DHT dht(DHTPIN, DHTTYPE);  // Crear objeto DHT para leer el sensor DHT
Adafruit_BME280 bme;       // Crear objeto BME280 para leer el sensor de presión (y altitud)
MQ135 co2Sensor(A0);      // Crear objeto MQ135 para CO2 (analog input pin A0)
MQ7 coSensor(A1);         // Crear objeto MQ7 para CO (analog input pin A1)

void setup() {
  Serial.begin(9600);  // Inicializar comunicación serial con la estación terrestre
  dht.begin();         // Inicializar el sensor DHT
  if (!bme.begin()) {
    Serial.println(F("No se pudo encontrar un sensor BME280"));
    while (1);
  }
  delay(2000);  // Esperar un poco para que los sensores se estabilicen
}

void loop() {
  // Leer sensores
  float temperatura = dht.readTemperature(); // Temperatura en grados Celsius
  float humedad = dht.readHumidity();        // Humedad relativa
  float altitud = bme.readAltitude(1013.25); // Altitud en metros (presión estándar 1013.25 hPa)
  
  // Leer los sensores de gases
  float co2 = co2Sensor.readSensor();  // Concentración de CO2
  float co = coSensor.readSensor();    // Concentración de CO
  
  // Verificar si las lecturas fueron correctas
  if (isnan(temperatura) || isnan(co2) || isnan(co) || isnan(altitud)) {
    Serial.println("Error al leer los sensores");
    return;
  }

  // Enviar los datos al puerto serial en el formato adecuado
  Serial.print(temperatura);
  Serial.print(",");
  Serial.print(altitud);
  Serial.print(",");
  Serial.print(co2);
  Serial.print(",");
  Serial.println(co);
  
  // Esperar 2 segundos antes de la siguiente lectura
  delay(2000);
}
