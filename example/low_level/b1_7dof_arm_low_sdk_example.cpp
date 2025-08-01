#include <array>
#include <chrono>
#include <iostream>
#include <thread>


#include <booster/idl/b1/LowCmd.h>
#include <booster/idl/b1/MotorCmd.h>
#include <booster/robot/b1/b1_api_const.hpp>
#include <booster/robot/channel/channel_publisher.hpp>


// Before you start to run this example, please make sure the robot is in "Prepare" mode.
// Then start to run this example and press ENTER to start control.
// In the same time, you should change the robot mode to "Custom" by api or controller.

static const std::string kTopicLowSDK = booster::robot::b1::kTopicJointCtrl;
using namespace booster::robot::b1;

int main(int argc, char const *argv[]) {
  if (argc < 2) {
    std::cout << "Usage: " << argv[0] << " networkInterface" << std::endl;
    exit(-1);
  }

  booster::robot::ChannelFactory::Instance()->Init(0, argv[1]);

  booster::robot::ChannelPublisherPtr<booster_interface::msg::LowCmd>
      low_sdk_publisher;
  booster_interface::msg::LowCmd msg;


  low_sdk_publisher.reset(
      new booster::robot::ChannelPublisher<booster_interface::msg::LowCmd>(
          kTopicLowSDK));
  low_sdk_publisher->InitChannel();



  std::array<JointIndexWith7DofArm, 29> low_joints = {
      JointIndexWith7DofArm::kHeadYaw, JointIndexWith7DofArm::kHeadPitch,
      JointIndexWith7DofArm::kLeftShoulderPitch,  JointIndexWith7DofArm::kLeftShoulderRoll,
      JointIndexWith7DofArm::kLeftElbowPitch,    JointIndexWith7DofArm::kLeftElbowYaw,
      JointIndexWith7DofArm::kLeftWristPitch,    JointIndexWith7DofArm::kLeftWristYaw,
      JointIndexWith7DofArm::kLeftHandRoll,
      JointIndexWith7DofArm::kRightShoulderPitch, JointIndexWith7DofArm::kRightShoulderRoll,
      JointIndexWith7DofArm::kRightElbowPitch,   JointIndexWith7DofArm::kRightElbowYaw,
      JointIndexWith7DofArm::kRightWristPitch,   JointIndexWith7DofArm::kRightWristYaw,
      JointIndexWith7DofArm::kRightHandRoll,
      JointIndexWith7DofArm::kWaist,
      JointIndexWith7DofArm::kLeftHipPitch, JointIndexWith7DofArm::kLeftHipRoll, JointIndexWith7DofArm::kLeftHipYaw,
      JointIndexWith7DofArm::kLeftKneePitch, JointIndexWith7DofArm::kCrankUpLeft, JointIndexWith7DofArm::kCrankDownLeft,
      JointIndexWith7DofArm::kRightHipPitch, JointIndexWith7DofArm::kRightHipRoll, JointIndexWith7DofArm::kRightHipYaw,
      JointIndexWith7DofArm::kRightKneePitch, JointIndexWith7DofArm::kCrankUpRight, JointIndexWith7DofArm::kCrankDownRight
      };

  float weight = 0.f;
  float weight_rate = 0.2f;

  float kp = 160.f;
  float kd = 5.5f;
  float dq = 0.f;
  float tau_ff = 0.f;

  float control_dt = 0.02f;
  float max_joint_velocity = 0.5f;

  float weight_margin = weight_rate * control_dt;
  float max_joint_delta = max_joint_velocity * control_dt;
  auto sleep_time =
      std::chrono::milliseconds(static_cast<int>(control_dt / 0.001f));

  // msg.cmd_type(booster_interface::msg::CmdType::SERIAL);
  msg.cmd_type(booster_interface::msg::CmdType::PARALLEL);

  std::array<float, 29> init_pos{};
  
  // define kp for each joint
  std::array<float, 29> kps = {
      5., 5.,
      70., 70., 70., 70., 50., 70., 50.,
      70., 70., 70., 70., 50., 70., 50.,
      100., 
      350., 350., 180., 350., 450., 450.,
      350., 350., 180., 350., 450., 450.,
  };

  // define kd for each joint
  std::array<float, 29> kds = {
      .1, .1,
      1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
      1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
      5.0,
      7.5, 7.5, 3., 5.5, 0.5, 0.5,
      7.5, 7.5, 3., 5.5, 0.5, 0.5,
  };

  // target pos with standing position
  std::array<float, 29> target_pos = { 0.00,  0.00,
                                      0.25, -1.40,  0.00, -0.50, 0.0, 0.0, 0.0,
                                      0.25,  1.40,  0.00,  0.50, 0.0, 0.0, 0.0,
                                      0.0,
                                      -0.1, 0.0, 0.0, 0.2, 0.137, 0.125,
                                      -0.1, 0.0, 0.0, 0.2, 0.137, 0.125
                                    };


  for (size_t i = 0; i < booster::robot::b1::kJointCnt7DofArm; i++) {
    booster_interface::msg::MotorCmd motor_cmd;
    msg.motor_cmd().push_back(motor_cmd);
  }

 
  // wait for control
  std::cout << "Press ENTER to start ctrl ..." << std::endl;
  std::cin.get();

  // start control
  std::cout << "Start low ctrl!" << std::endl;
  float period = 50000.f;
  int num_time_steps = static_cast<int>(period / control_dt);

  // init joints with standing position
  std::array<float, 29> current_jpos_des{
                                          0.00,  0.00,
                                          0.25, -1.40,  0.00, -0.50, 0.0, 0.0, 0.0,
                                          0.25,  1.40,  0.00,  0.50, 0.0, 0.0, 0.0,
                                          0.0,
                                          -0.1, 0.0, 0.0, 0.2, 0.137, 0.125,
                                          -0.1, 0.0, 0.0, 0.2, 0.137, 0.125,
                                        };


  // lift lows up
  for (int i = 0; i < num_time_steps; ++i) {
    // update jpos des
    for (int j = 0; j < init_pos.size(); ++j) {
      current_jpos_des.at(j) +=
          std::clamp(target_pos.at(j) - current_jpos_des.at(j),
                     -max_joint_delta, max_joint_delta);
    }

    // set control joints
    for (int j = 0; j < init_pos.size(); ++j) {
      msg.motor_cmd().at(int(low_joints.at(j))).q(current_jpos_des.at(j));
      msg.motor_cmd().at(int(low_joints.at(j))).dq(dq);
      msg.motor_cmd().at(int(low_joints.at(j))).kp(kps.at(j));
      msg.motor_cmd().at(int(low_joints.at(j))).kd(kds.at(j));
      msg.motor_cmd().at(int(low_joints.at(j))).tau(tau_ff);
    }

    // send dds msg
    low_sdk_publisher->Write(&msg);

    // sleep
    std::this_thread::sleep_for(sleep_time);
  }

  // stop control
  std::cout << "Stoping low ctrl ...";
  float stop_time = 2.0f;
  int stop_time_steps = static_cast<int>(stop_time / control_dt);

  for (int i = 0; i < stop_time_steps; ++i) {
    // increase weight
    weight -= weight_margin;
    weight = std::clamp(weight, 0.f, 1.f);

    // send dds msg
    low_sdk_publisher->Write(&msg);

    // sleep
    std::this_thread::sleep_for(sleep_time);
  }

  std::cout << "Done!" << std::endl;

  return 0;
}
