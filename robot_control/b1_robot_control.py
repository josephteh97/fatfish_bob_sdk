#!/usr/bin/env python3

from booster_robotics_sdk_python import (
    B1LocoClient, ChannelFactory, RobotMode, B1HandIndex, 
    GripperControlMode, Position, Orientation, Posture, 
    GripperMotionParameter, Quaternion, Frame, Transform, 
    DexterousFingerParameter
)
import sys
import time
import random

class B1RobotController:
    def __init__(self, network_interface):
        """Initialize the robot controller with network interface"""
        self.network_interface = network_interface
        self.client = None
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self.yaw, self.pitch = 0.0, 0.0
        self.hand_action_count = 0
        
    def initialize(self):
        """Initialize the robot client"""
        try:
            ChannelFactory.Instance().Init(0, self.network_interface)
            self.client = B1LocoClient()
            self.client.Init()
            print(f"Robot initialized successfully with interface: {self.network_interface}")
            return True
        except Exception as e:
            print(f"Failed to initialize robot: {e}")
            return False
    
    def hand_rock(self):
        """Make rock hand gesture"""
        finger_params = []
        
        # Configure fingers 0-4 for rock (closed fist)
        for i in range(5):
            finger_param = DexterousFingerParameter()
            finger_param.seq = i if i != 4 else 4  # Fix the seq assignment for finger 4
            finger_param.angle = 0
            finger_param.force = 200
            finger_param.speed = 800
            finger_params.append(finger_param)
        
        res = self.client.ControlDexterousHand(finger_params, B1HandIndex.kRightHand)
        if res != 0:
            print(f"Rock hand failed: error = {res}")
        
        time.sleep(0.2)
        
        # Add thumb
        finger5_param = DexterousFingerParameter()
        finger5_param.seq = 5
        finger5_param.angle = 0
        finger5_param.force = 200
        finger5_param.speed = 800
        finger_params.append(finger5_param)
        
        res = self.client.ControlDexterousHand(finger_params, B1HandIndex.kRightHand)
        if res != 0:
            print(f"Rock hand thumb failed: error = {res}")
    
    def hand_scissor(self):
        """Make scissor hand gesture"""
        finger_params = []
        
        # Configure fingers - index and middle extended, others closed
        angles = [0, 0, 1000, 1000, 0, 0]  # finger 0,1,2,3,4,5
        
        for i in range(6):
            finger_param = DexterousFingerParameter()
            finger_param.seq = i if i != 4 else 4
            finger_param.angle = angles[i]
            finger_param.force = 200
            finger_param.speed = 800
            finger_params.append(finger_param)
        
        res = self.client.ControlDexterousHand(finger_params, B1HandIndex.kRightHand)
        if res != 0:
            print(f"Scissor hand failed: error = {res}")
    
    def hand_paper(self):
        """Make paper hand gesture"""
        finger_params = []
        
        # Configure all fingers extended
        for i in range(6):
            finger_param = DexterousFingerParameter()
            finger_param.seq = i if i != 4 else 4
            finger_param.angle = 1000
            finger_param.force = 200
            finger_param.speed = 800
            finger_params.append(finger_param)
        
        res = self.client.ControlDexterousHand(finger_params, B1HandIndex.kRightHand)
        if res != 0:
            print(f"Paper hand failed: error = {res}")
    
    def hand_grasp(self):
        """Make grasping gesture"""
        finger_params = []
        
        for i in range(6):
            finger_param = DexterousFingerParameter()
            finger_param.seq = i if i != 4 else 4
            finger_param.angle = 350
            finger_param.force = 400
            finger_param.speed = 800
            finger_params.append(finger_param)
        
        res = self.client.ControlDexterousHand(finger_params, B1HandIndex.kRightHand)
        if res != 0:
            print(f"Grasp hand failed: error = {res}")
    
    def hand_ok(self):
        """Make OK hand gesture"""
        finger_params = []
        
        # Configure fingers for OK gesture
        angles = [1000, 1000, 1000, 500, 400, 350]
        forces = [200, 200, 200, 200, 200, 200]
        speeds = [800, 800, 800, 800, 800, 1000]
        
        for i in range(6):
            finger_param = DexterousFingerParameter()
            finger_param.seq = i if i != 4 else 4
            finger_param.angle = angles[i]
            finger_param.force = forces[i]
            finger_param.speed = speeds[i]
            finger_params.append(finger_param)
        
        res = self.client.ControlDexterousHand(finger_params, B1HandIndex.kRightHand)
        if res != 0:
            print(f"OK hand failed: error = {res}")
    
    def execute_command(self, cmd):
        """Execute a robot command"""
        need_print = False
        res = 0
        
        if cmd == "mp":
            res = self.client.ChangeMode(RobotMode.kPrepare)
            print("Mode: Prepare")
        elif cmd == "md":
            res = self.client.ChangeMode(RobotMode.kDamping)
            print("Mode: Damping")
        elif cmd == "mw":
            res = self.client.ChangeMode(RobotMode.kWalking)
            print("Mode: Walking")
        elif cmd == "mc":
            res = self.client.ChangeMode(RobotMode.kCustom)
            print("Mode: Custom")
        elif cmd == "stop":
            self.x, self.y, self.z = 0.0, 0.0, 0.0
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "w":
            self.x, self.y, self.z = 0.8, 0.0, 0.0
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "a":
            self.x, self.y, self.z = 0.0, 0.2, 0.0
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "s":
            self.x, self.y, self.z = -0.2, 0.0, 0.0
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "d":
            self.x, self.y, self.z = 0.0, -0.2, 0.0
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "q":
            self.x, self.y, self.z = 0.0, 0.0, 0.2
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "e":
            self.x, self.y, self.z = 0.0, 0.0, -0.2
            need_print = True
            res = self.client.Move(self.x, self.y, self.z)
        elif cmd == "hd":
            self.yaw, self.pitch = 0.0, 1.0
            need_print = True
            res = self.client.RotateHead(self.pitch, self.yaw)
        elif cmd == "hu":
            self.yaw, self.pitch = 0.0, -0.3
            need_print = True
            res = self.client.RotateHead(self.pitch, self.yaw)
        elif cmd == "hr":
            self.yaw, self.pitch = -0.785, 0.0
            need_print = True
            res = self.client.RotateHead(self.pitch, self.yaw)
        elif cmd == "hl":
            self.yaw, self.pitch = 0.785, 0.0
            need_print = True
            res = self.client.RotateHead(self.pitch, self.yaw)
        elif cmd == "ho":
            self.yaw, self.pitch = 0.0, 0.0
            need_print = True
            res = self.client.RotateHead(self.pitch, self.yaw)
        elif cmd == "mhel":
            tar_posture = Posture()
            tar_posture.position = Position(0.35, 0.25, 0.1)
            tar_posture.orientation = Orientation(-1.57, -1.57, 0.0)
            res = self.client.MoveHandEndEffectorV2(tar_posture, 2000, B1HandIndex.kLeftHand)
        elif cmd == "gopenl":
            motion_param = GripperMotionParameter()
            motion_param.position = 500
            motion_param.force = 100
            motion_param.speed = 100
            res = self.client.ControlGripper(motion_param, GripperControlMode.kPosition, B1HandIndex.kLeftHand)
        elif cmd == "gft":
            src = Frame.kBody
            dst = Frame.kLeftHand
            transform = Transform()
            res = self.client.GetFrameTransform(src, dst, transform)
            if res == 0:
                print(f"Transform: {transform}")
        elif cmd == "hcm-start":
            res = self.client.SwitchHandEndEffectorControlMode(True)
            print("Hand end effector control mode: ON")
        elif cmd == "hcm-stop":
            res = self.client.SwitchHandEndEffectorControlMode(False)
            print("Hand end effector control mode: OFF")
        elif cmd == "hand-down":
            tar_posture = Posture()
            tar_posture.position = Position(0.28, -0.25, 0.05)
            tar_posture.orientation = Orientation(0.0, 0.0, 0.0)
            res = self.client.MoveHandEndEffector(tar_posture, 1000, B1HandIndex.kRightHand)
            time.sleep(0.3)
            self.hand_action_count += 1
            r_num = random.randint(0, 2)
            if r_num == 0:
                self.hand_rock()
            elif r_num == 1:
                self.hand_scissor()
            else:
                self.hand_paper()
        elif cmd == "hand-up":
            tar_posture = Posture()
            tar_posture.position = Position(0.25, -0.3, 0.25)
            tar_posture.orientation = Orientation(0.0, -1.0, 0.0)
            res = self.client.MoveHandEndEffector(tar_posture, 1000, B1HandIndex.kRightHand)
            time.sleep(0.3)
            self.hand_paper()
        elif cmd == "grasp":
            self.hand_grasp()
        elif cmd == "ok":
            self.hand_ok()
        elif cmd == "paper":
            self.hand_paper()
        elif cmd == "scissor":
            self.hand_scissor()
        elif cmd == "rock":
            self.hand_rock()
        elif cmd == "help":
            self.print_help()
        elif cmd == "quit" or cmd == "exit":
            return False
        else:
            print(f"Unknown command: {cmd}")
            self.print_help()
        
        if need_print:
            print(f"Movement params: x={self.x}, y={self.y}, z={self.z}")
            print(f"Head params: pitch={self.pitch}, yaw={self.yaw}")
        
        if res != 0:
            print(f"Command failed: error = {res}")
        
        return True
    
    def print_help(self):
        """Print available commands"""
        print("\n=== B1 Robot Control Commands ===")
        print("Mode Commands:")
        print("  mp    - Prepare mode")
        print("  md    - Damping mode") 
        print("  mw    - Walking mode")
        print("  mc    - Custom mode")
        print("\nMovement Commands:")
        print("  w     - Move forward")
        print("  s     - Move backward")
        print("  a     - Move left")
        print("  d     - Move right")
        print("  q     - Move up")
        print("  e     - Move down")
        print("  stop  - Stop movement")
        print("\nHead Commands:")
        print("  hd    - Head down")
        print("  hu    - Head up")
        print("  hr    - Head right")
        print("  hl    - Head left")
        print("  ho    - Head origin")
        print("\nHand Commands:")
        print("  rock      - Rock hand gesture")
        print("  paper     - Paper hand gesture")
        print("  scissor   - Scissor hand gesture")
        print("  grasp     - Grasp gesture")
        print("  ok        - OK gesture")
        print("  hand-up   - Move hand up")
        print("  hand-down - Move hand down with random gesture")
        print("\nControl Commands:")
        print("  hcm-start - Start hand end effector control mode")
        print("  hcm-stop  - Stop hand end effector control mode")
        print("  mhel      - Move hand end effector left")
        print("  gopenl    - Open left gripper")
        print("  gft       - Get frame transform")
        print("\nOther Commands:")
        print("  help  - Show this help")
        print("  quit  - Exit program")
        print("=====================================\n")
    
    def run(self):
        """Main control loop"""
        if not self.initialize():
            return
        
        print(f"B1 Robot Controller started with interface: {self.network_interface}")
        print("Type 'help' for available commands, 'quit' to exit")
        
        try:
            while True:
                try:
                    cmd = input("B1> ").strip().lower()
                    if not cmd:
                        continue
                    
                    if not self.execute_command(cmd):
                        break
                        
                except KeyboardInterrupt:
                    print("\nReceived Ctrl+C, stopping robot...")
                    self.execute_command("stop")
                    break
                except EOFError:
                    print("\nEOF received, exiting...")
                    break
                except Exception as e:
                    print(f"Error executing command: {e}")
        
        finally:
            print("Robot controller shutting down...")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <network_interface>")
        print(f"Example: {sys.argv[0]} 192.168.10.102")
        sys.exit(1)
    
    network_interface = sys.argv[1]
    controller = B1RobotController(network_interface)
    controller.run()

if __name__ == "__main__":
    main()
