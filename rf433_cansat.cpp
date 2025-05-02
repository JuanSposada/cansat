#include <RH_ASK.h>           // Usa la librería RadioHead
#include <SPI.h>              // Necesaria aunque no se use directamente

RH_ASK driver;

void setup() {
  Serial.begin(9600);
  if (!driver.init()) {
    Serial.println("init failed");
  }
}

void loop() {
  // Simular lectura de sensores (puedes sustituir por lecturas reales)
  float temperatura = 25.4;
  float altitud = 100.5;
  float co2 = 400.0;
  float co = 25.0;

  // Empaquetar los datos como una cadena separada por comas
  char mensaje[50];
  snprintf(mensaje, sizeof(mensaje), "%.1f,%.1f,%.1f,%.1f", temperatura, altitud, co2, co);
  
  // Enviar el mensaje
  driver.send((uint8_t *)mensaje, strlen(mensaje));
  driver.waitPacketSent();

  Serial.println(mensaje);  // Para depuración por USB
  delay(1000);              // Espera 1 segundo
}
