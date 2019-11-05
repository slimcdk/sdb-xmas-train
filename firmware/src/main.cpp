#include <Arduino.h>


// IO PIN CONFIGURATION
#define MOTOR_PULSE_PIN		2
#define MOTOR_PWM_PIN 		3
#define MOTOR_DIR_PIN 		4
#define TRAIN_MODE_PIN    	11


/** TRAIN TIMING SCHEME
 * |-- boot --|-- run --|-- break --|-- stop --|
 * |-- run progress  ------------------------- |
 * |-- motor on time -------------- |
**/
#define TRAIN_T_BOOT      	0
#define TRAIN_T_RUN       	30000
#define TRAIN_T_BREAK     	2000
#define TRAIN_T_STOP      	180000

#define TRAIN_S_BOOT      	1.0
#define TRAIN_S_MAX		0.5
#define TRAIN_S_MIN		0.0

#define MOTOR_SAMPLES     	35
#define MOTOR_SAMPLE_TOL  	5



// stores data for the motor timings and speeds
struct CONFIG {
  uint64_t boot_tm;
  uint64_t run_tm;
  uint64_t break_tm;
  uint64_t stop_tm;
  float boot_spd;
  float max_spd;
  float min_spd;
  bool direction;
};


// data structure for Arduino <-> RPi serial communication
struct TRAIN_DATA {
  uint16_t progress;
  uint8_t motor_speed;
  bool motor_sense;
};


union TX_PACK {
  TRAIN_DATA S_Packet_t;
  TRAIN_DATA data;
  char ser_data[sizeof(TRAIN_DATA)];
};



uint64_t current_millis;
uint32_t run_progress;
uint8_t motor_sample_index;
float speed_scale, last_speed_scale;
bool boot_mode, normal_mode, breaking_mode, nonstop_mode, is_motor_running, run_train, motor_run_samples[MOTOR_SAMPLES];


TRAIN_DATA train_data;
CONFIG motor;


/**
 * Checks whether the motor is actual running or not.
 */
bool isMotorRunning() {

  motor_run_samples[motor_sample_index] = digitalRead(MOTOR_PULSE_PIN);
  motor_sample_index = (motor_sample_index + 1) % MOTOR_SAMPLES;

  uint16_t _sample_sum = 0;
  for (uint8_t i = 0; i < MOTOR_SAMPLES; i++)
    _sample_sum = _sample_sum + motor_run_samples[i];

  // if motor sensor fluctuates it must be running
  return (MOTOR_SAMPLE_TOL < _sample_sum && _sample_sum < (MOTOR_SAMPLES-MOTOR_SAMPLE_TOL));
}


void setup() {
  Serial.begin(115200);
  //Serial.println("SDB Train booting..");

  pinMode(TRAIN_MODE_PIN, INPUT_PULLUP);
  pinMode(MOTOR_PWM_PIN, OUTPUT);
  pinMode(MOTOR_DIR_PIN, OUTPUT);
  pinMode(MOTOR_PULSE_PIN, INPUT);

  nonstop_mode = false;
  speed_scale = 0.0;
  run_progress = 0;
  run_train = true;

  motor_sample_index = 0;
  train_data = {(uint16_t)(run_progress/1000), (uint8_t)(speed_scale*100.0),  is_motor_running};
  motor = {TRAIN_T_BOOT, TRAIN_T_RUN, TRAIN_T_BREAK, TRAIN_T_STOP, TRAIN_S_BOOT, TRAIN_S_MAX, TRAIN_S_MIN, true};

  //Serial.println("Setup finished");
}


void loop () {

  // variables to be used throughout the program loop
  last_speed_scale = speed_scale;
  current_millis = millis();
  is_motor_running = isMotorRunning();
  nonstop_mode = digitalRead(TRAIN_MODE_PIN);

  // compute current run progress
  run_progress = current_millis % (motor.boot_tm + motor.run_tm + motor.break_tm + motor.stop_tm);
  run_train = run_progress < (motor.boot_tm + motor.run_tm + motor.break_tm);

  // determine motor mode
  boot_mode = (run_train && run_progress < motor.boot_tm && !nonstop_mode);
  normal_mode = ((run_train && run_progress < (motor.boot_tm+motor.run_tm)) || nonstop_mode);
  breaking_mode = (run_train && run_progress > ((motor.boot_tm+motor.run_tm)) && !nonstop_mode);

  // set motor speed scales
  // boot motor
  if (boot_mode) {
    speed_scale = motor.boot_spd;

  // run motor
  } else if (normal_mode) {
    speed_scale = motor.max_spd;

  // break motor
  } else if (breaking_mode) {
    int run_progress_break = map(run_progress, (motor.boot_tm+motor.run_tm), (motor.boot_tm+motor.run_tm+motor.break_tm),  motor.break_tm, 0);
    speed_scale = ((double)run_progress_break / (double)motor.break_tm) * motor.max_spd;

  // motor stop
  } else {
    speed_scale = motor.min_spd;
  }


  // write outputs
  digitalWrite(MOTOR_DIR_PIN, motor.direction);
  analogWrite(MOTOR_PWM_PIN, (uint8_t)(speed_scale * 255));
  digitalWrite(LED_BUILTIN, run_train);

  // prepare data packages for transmission
  train_data.progress = (uint16_t) (run_progress / 1000);
  train_data.motor_speed = (uint8_t)(speed_scale*100.0) ;
  train_data.motor_sense = is_motor_running;

  char b[sizeof(train_data)];
  memcpy(b, &train_data, sizeof(train_data));
  Serial.write(b, sizeof(b));

/*
  //Serial.print(current_millis);
  //Serial.print(",");
  Serial.print(run_progress);
  Serial.print(",");
  Serial.print((uint8_t) (speed_scale * 100));
  Serial.print(",");
  Serial.print(is_motor_running);
  Serial.println(",");
*/
}
