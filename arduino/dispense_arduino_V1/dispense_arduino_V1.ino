#include <Servo.h>

// Broches de contrôle des servomoteurs
const int PIN_SERVO_1 = 8;
const int PIN_SERVO_2 = 9;
const int PIN_SERVO_3 = 10;

// Déclaration des 3 objets servomoteurs
Servo servo1;
Servo servo2;
Servo servo3;

// Paramètres de mouvement (ajustables selon ton mécanisme mécanique)
const int ANGLE_REPOS = 0;          // Position fermée
const int ANGLE_DISTRIBUTION = 500;  // Position ouverte
const int TEMPS_OUVERTURE = 500;    // Temps en position ouverte (ms)
const int TEMPS_RETOUR = 350;       // Temps pour revenir et se stabiliser (ms)

void setup() {
  Serial.begin(9600);

  // Initialisation et rattachement des servos aux broches
  servo1.attach(PIN_SERVO_1);
  servo2.attach(PIN_SERVO_2);
  servo3.attach(PIN_SERVO_3);

  // Mise en position repos fermée immédiate
  servo1.write(ANGLE_REPOS);
  servo2.write(ANGLE_REPOS);
  servo3.write(ANGLE_REPOS);

  Serial.println("ARDUINO_PRET");
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    // Décodage de la commande formatée "CMD:qte1,qte2,qte3"
    if (msg.startsWith("CMD:")) {
      msg = msg.substring(4);

      int v1 = msg.indexOf(',');
      int v2 = msg.indexOf(',', v1 + 1);

      if (v1 > 0 && v2 > v1) {
        int qte1 = msg.substring(0, v1).toInt();
        int qte2 = msg.substring(v1 + 1, v2).toInt();
        int qte3 = msg.substring(v2 + 1).toInt();

        traiterCommande(qte1, qte2, qte3);
      }
    }
  }
}

// Fonction générique pour actionner n'importe quel servomoteur
void dispenserAvecServo(Servo &moteur, int angleRepos, int angleDistribution, int dureeOuvertureMs) {
  // 1. Déplacement vers l'angle d'ouverture
  moteur.write(angleDistribution);
  delay(dureeOuvertureMs);

  // 2. Retour en position fermée
  moteur.write(angleRepos);
  delay(TEMPS_RETOUR);
}

// Traitement séquentiel de la commande complète
void traiterCommande(int q1, int q2, int q3) {
  Serial.println("DEBUT_COMMANDE");

  // Servomoteur 1 (Réservoir 1)
  for (int i = 0; i < q1; i++) {
    Serial.print("Distribution R1 (Servo 1) - ");
    Serial.print(i + 1);
    Serial.print("/");
    Serial.println(q1);
    dispenserAvecServo(servo1, ANGLE_REPOS, ANGLE_DISTRIBUTION, TEMPS_OUVERTURE);
  }

  // Servomoteur 2 (Réservoir 2)
  for (int i = 0; i < q2; i++) {
    Serial.print("Distribution R2 (Servo 2) - ");
    Serial.print(i + 1);
    Serial.print("/");
    Serial.println(q2);
    dispenserAvecServo(servo2, ANGLE_REPOS, ANGLE_DISTRIBUTION, TEMPS_OUVERTURE);
  }

  // Servomoteur 3 (Réservoir 3)
  for (int i = 0; i < q3; i++) {
    Serial.print("Distribution R3 (Servo 3) - ");
    Serial.print(i + 1);
    Serial.print("/");
    Serial.println(q3);
    dispenserAvecServo(servo3, ANGLE_REPOS, ANGLE_DISTRIBUTION, TEMPS_OUVERTURE);
  }

  // Signal renvoyé à Python pour débloquer le bouton
  Serial.println("COMMANDE_TERMINEE");
}