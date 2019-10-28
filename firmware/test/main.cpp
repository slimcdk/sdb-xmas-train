#include <Arduino.h>


// MOTOR IO
#define MOTOR_CTRL_PIN 		9
#define MOTOR_DIR_PIN 		8


// train durations in seconds
//#define TRAIN_LAP_TIME 		30
#define TRAIN_RUN_DURATION 	30000
#define TRAIN_DURATION	  	40000

#define TRAIN_MAX_SPEED		127 	// 50% of 8-bit value
#define TRAIN_MIN_SPEED		0	// 0% of 8-bit value

#define TRAIN_DEBUG_SW_PIN 7




bool run_train, motor_boot;
uint32_t run_progress;


void setup() {
  Serial.begin(9600);
  Serial.println("SDB Train booting..");

  pinMode(TRAIN_DEBUG_SW_PIN, INPUT_PULLUP);

  /** MOTOR SETUP **/
  Serial.println("Setting up motor..");
  pinMode(MOTOR_CTRL_PIN, OUTPUT);
  pinMode(MOTOR_DIR_PIN, OUTPUT);
  Serial.println("Motor ready");

  motor_boot = true;
  run_progress = millis() % TRAIN_DURATION;
  run_train = run_progress < TRAIN_RUN_DURATION;

  Serial.println("Setup finished");
}


void loop () {
  
  // no interval run, if debugging switch enabled
  if ( digitalRead(TRAIN_DEBUG_SW_PIN)) {
    run_train = true;
    motor_boot = false;
  } else {
    run_progress = millis() % TRAIN_DURATION;
    run_train = run_progress < TRAIN_RUN_DURATION;

    if ( run_progress > TRAIN_RUN_DURATION && motor_boot == false) {
      motor_boot = true;
    }
  }

  // boot motor with full speed
  if (motor_boot == true && run_train == true) {
    motor_boot = false;
    digitalWrite(MOTOR_DIR_PIN, HIGH);
    analogWrite(MOTOR_CTRL_PIN, 255);
    delay(3000);
    Serial.println("BOOTED!");
  }


  // output to motor
  digitalWrite(MOTOR_DIR_PIN, HIGH);
  analogWrite(MOTOR_CTRL_PIN, (run_train == true) ? TRAIN_MAX_SPEED : TRAIN_MIN_SPEED);
  digitalWrite(LED_BUILTIN, run_train);


  Serial.print(run_train);
  Serial.print(" ");
  Serial.print(digitalRead(TRAIN_DEBUG_SW_PIN));
  Serial.print(" ");
  Serial.println(run_progress);
  

  //digitalWrite(MOTOR_DIR_PIN, HIGH);
  //analogWrite(MOTOR_CTRL_PIN, 127);
}
