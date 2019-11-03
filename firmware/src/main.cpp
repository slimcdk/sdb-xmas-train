#include <Arduino.h>


// IO PIN CONFIGURATION
#define MOTOR_PULSE_PIN   2
#define MOTOR_PWM_PIN 		3
#define MOTOR_DIR_PIN 		4
#define TRAIN_MODE_PIN    11


/** TRAIN TIMING SCHEME
 * |-- boot --|-- run --|-- break --|-- stop --|
 * |-- run progress  ------------------------- |
 * |-- motor on time -------------- |
**/
#define TRAIN_T_BOOT      2000
#define TRAIN_T_RUN       36000
#define TRAIN_T_BREAK     1000
#define TRAIN_T_STOP      600000

#define TRAIN_S_BOOT      1   
#define TRAIN_S_MAX		    0.5
#define TRAIN_S_MIN		    0

#define MOTOR_SAMPLES     30
#define MOTOR_SAMPLE_TOL  5



bool is_motor_running, run_train, boot_mode, normal_mode, breaking_mode, nonstop_mode, motor_run_samples[MOTOR_SAMPLES];
uint64_t run_progress, current_millis;
uint8_t motor_sample_index, sample_tolerance;
double speed_scale;



/**
 * Checks whether the motor is actual running or not.
 */
bool isMotorRunning() {

  motor_run_samples[motor_sample_index] = digitalRead(MOTOR_PULSE_PIN);
  motor_sample_index = (motor_sample_index + 1) % MOTOR_SAMPLES;

  uint16_t _sample_sum = 0;
  for (uint8_t i = 0; i < MOTOR_SAMPLES; i++)
    _sample_sum = _sample_sum + motor_run_samples[i];

  return (MOTOR_SAMPLE_TOL < _sample_sum && _sample_sum < (MOTOR_SAMPLES-MOTOR_SAMPLE_TOL));
}


void setup() {
  Serial.begin(9600);
  Serial.println("SDB Train booting..");

  nonstop_mode = false;
  speed_scale = 0.0;
  run_progress = 0;
  run_train = true;
  motor_sample_index = 0;


  pinMode(TRAIN_MODE_PIN, INPUT_PULLUP);
  pinMode(MOTOR_PWM_PIN, OUTPUT);
  pinMode(MOTOR_DIR_PIN, OUTPUT);
  pinMode(MOTOR_PULSE_PIN, INPUT);


  Serial.println("Setup finished");
}


void loop () {

  // variables to be used throughout the program loop
  current_millis = millis();
  is_motor_running = isMotorRunning();
  nonstop_mode = digitalRead(TRAIN_MODE_PIN);

  // compute current run progress
  run_progress = current_millis % (TRAIN_T_BOOT+TRAIN_T_RUN+TRAIN_T_BREAK+TRAIN_T_STOP);
  run_train = run_progress < (TRAIN_T_BOOT+TRAIN_T_RUN+TRAIN_T_BREAK);

  // determine motor mode
  boot_mode = (run_train && run_progress < TRAIN_T_BOOT && !nonstop_mode);
  normal_mode = ((run_train && run_progress < ((TRAIN_T_BOOT+TRAIN_T_RUN+TRAIN_T_BREAK)-TRAIN_T_BREAK)) || nonstop_mode);
  breaking_mode = (run_train && run_progress > ((TRAIN_T_BOOT+TRAIN_T_RUN+TRAIN_T_BREAK)-TRAIN_T_BREAK) && !nonstop_mode);

  // set motor speed scales
  // boot motor
  if (boot_mode) {
    Serial.print("BOOT");
    speed_scale = TRAIN_S_BOOT;


  // run motor
  } else if (normal_mode) {
    Serial.print("RUN");
    speed_scale = TRAIN_S_MAX;
  

  // break motor
  } else if (breaking_mode) {
    Serial.print("BREAK");
    int run_progress_break = map(run_progress, (TRAIN_T_BOOT+TRAIN_T_RUN+TRAIN_T_BREAK)-TRAIN_T_BREAK, (TRAIN_T_BOOT+TRAIN_T_RUN+TRAIN_T_BREAK),  TRAIN_T_BREAK, 0);
    speed_scale = ((double)run_progress_break / (double)TRAIN_T_BREAK) * TRAIN_S_MAX;


  // motor stop
  } else {
    Serial.print("STOP");
    speed_scale = TRAIN_S_MIN;
  }


  // set outputs
  digitalWrite(MOTOR_DIR_PIN, HIGH);
  //analogWrite(MOTOR_PWM_PIN, (int)(255 * speed_scale));
  digitalWrite(LED_BUILTIN, run_train);


  Serial.print("\t");
  Serial.print((uint32_t)current_millis);
  Serial.print("\t");
  Serial.print((uint32_t)run_progress);
  Serial.print("\t");
  Serial.print(speed_scale);
  Serial.println();

}