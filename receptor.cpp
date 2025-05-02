#include <VirtualWire.h>

void setup() {
  Serial.begin(9600);           // Comunicación con la PC (Python)
  vw_setup(2000);               // Velocidad de RF (en baudios)
  vw_set_rx_pin(11);            // Pin de datos del receptor RF (ajusta según tu conexión)
  vw_rx_start();                // Iniciar el receptor
}

void loop() {
  uint8_t buf[VW_MAX_MESSAGE_LEN];
  uint8_t buflen = VW_MAX_MESSAGE_LEN;

  // Si hay mensaje recibido
  if (vw_get_message(buf, &buflen)) {
    // Convertir a string y enviarlo al puerto serial
    String mensaje = "";
    for (int i = 0; i < buflen; i++) {
      mensaje += (char)buf[i];
    }

    Serial.println(mensaje); // Python leerá esto
  }
}
