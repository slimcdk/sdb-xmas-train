#include <Arduino.h>


// MOTOR IO
#define MOTOR_SENSE_PIN           2
#define MOTOR_CTRL_PIN 		        3
#define MOTOR_DIR_PIN 		        4
#define TRAIN_MODE_SW_PIN         11
#define RPI_ACTIVATE_MUSIC_PIN    10


// train durations in seconds
//#define TRAIN_LAP_TIME 		      30
#define TRAIN_RUN_DURATION 	      10000
#define TRAIN_DURATION	  	      20000
#define TRAIN_MOTOR_BOOT_TIME     2500
#define TRAIN_MOTOR_CHECK_UPSTART 2000


#define TRAIN_BOOT_SPEED          255   // 100% duty cycle
#define TRAIN_MAX_SPEED		        127 	// 50% duty cycle
#define TRAIN_MIN_SPEED		        0	    // 0% duty cycle

#define TRAIN_MOTOR_SAMPLES       30




bool is_motor_running, run_train, boot_motor, motor_run_samples[TRAIN_MOTOR_SAMPLES];
uint32_t run_progress, motor_speed, stop_motor_boot, current_millis, check_motor_state, motor_reboot_off;
uint8_t motor_sample_index = 0;


bool isMotorRunning() {

  motor_run_samples[motor_sample_index] = digitalRead(MOTOR_SENSE_PIN);
  motor_sample_index = (motor_sample_index + 1) % TRAIN_MOTOR_SAMPLES;

  uint8_t sample_sum = 0;
  for (uint8_t i = 0; i < TRAIN_MOTOR_SAMPLES; i++)
    sample_sum = sample_sum + motor_run_samples[i];

  return (5 < sample_sum && sample_sum < (TRAIN_MOTOR_SAMPLES-5));
}



void setup() {
  Serial.begin(9600);
  Serial.println("SDB Train booting..");

  pinMode(TRAIN_MODE_SW_PIN, INPUT_PULLUP);

  /** MOTOR SETUP **/
  Serial.println("Setting up motor..");
  pinMode(MOTOR_CTRL_PIN, OUTPUT);
  pinMode(MOTOR_DIR_PIN, OUTPUT);
  pinMode(MOTOR_SENSE_PIN, INPUT);
  for (uint8_t i = 0; i < TRAIN_MOTOR_SAMPLES; i++)
  {
    isMotorRunning();
  }

  Serial.println("Motor ready");

  boot_motor = true;
  run_progress = millis() % TRAIN_DURATION;
  run_train = run_progress < TRAIN_RUN_DURATION;
  Serial.println("Setup finished");
}


void loop () {

  current_millis = millis();
  is_motor_running = isMotorRunning();

  // evaluate if train should run 
  run_progress = current_millis % TRAIN_DURATION;
  run_train = run_progress < TRAIN_RUN_DURATION;

  // run train all the time if switched
  if (digitalRead(TRAIN_MODE_SW_PIN) == true) {
    run_train = true;
  }
  
  // set new time for motor boot to stop
  if (motor_speed == TRAIN_MIN_SPEED && run_train == true) {
    stop_motor_boot = current_millis + TRAIN_MOTOR_BOOT_TIME;
    check_motor_state = current_millis + TRAIN_MOTOR_CHECK_UPSTART;
  }
  
  // determine motor speed
  boot_motor = (current_millis < stop_motor_boot);
  motor_speed = (run_train == true) ? TRAIN_MAX_SPEED : TRAIN_MIN_SPEED;
  //motor_speed = (boot_motor == true) ? TRAIN_BOOT_SPEED : motor_speed;

/*
  // time to check if motor is running
  if (run_train == true && current_millis > check_motor_state) {
    
    // validate if motor is running
    if (is_motor_running == false) {
      motor_speed = TRAIN_MIN_SPEED;
    } else {
      // set next check
      check_motor_state = current_millis + TRAIN_MOTOR_CHECK_UPSTART;
    }
  }
  */


  // output to motor
  digitalWrite(MOTOR_DIR_PIN, HIGH);
  //analogWrite(MOTOR_CTRL_PIN, motor_speed);
  digitalWrite(LED_BUILTIN, run_train);
  digitalWrite(RPI_ACTIVATE_MUSIC_PIN, run_train);


  Serial.print(run_train ? "KØR" : "STOP");
  Serial.print("\t");
  Serial.print(current_millis);
  Serial.print("\t");
  Serial.print(stop_motor_boot);
  Serial.print("\t");
  Serial.print(run_progress);
  Serial.print("\t");
  Serial.print(motor_speed);
  Serial.print("\t");
  Serial.print(is_motor_running);
  Serial.println();

}