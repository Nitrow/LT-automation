#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>
#include <thread>
#include <chrono>

using namespace ur_rtde;
using namespace std::chrono;

int main(int argc, char* argv[])
{

RTDEControlInterface rtde_control("127.0.0.1");
RTDEReceiveInterface rtde_receive("127.0.0.1");

std::vector<double> joint_q = {-0.000000, -112.312305, -145.949854, 78.262160, 90.000000, -0.000000};

rtde_control.moveJ(joint_q, 0.25, 0.25, false);

//std::vector<double> speed = {0, 0, -0.100, 0, 0, 0};  //Maybe use if possible to simply program
//rtde_control.moveUntilContact(speed);

std::vector<double> target = rtde_receive.getActualTCPPose();
target[2] += 0.60;


rtde_control.moveL(target, 0.25, 0.5, false);


//target[1] += 0.5;            //if we need to lift the boxes first
//rtde_control.moveL(target, 0.25, 0.5, false);

rtde_control.moveJ(joint_q, 0.25, 0.5, false);


return 0;
}