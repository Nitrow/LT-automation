#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>

using namespace ur_rtde;


RTDEControlInterface rtde_control("127.0.0.1");
RTDEReceiveInterface rtde_receive("127.0.0.1");

void newTCPOffset (double x, double y, double z)
{   
    
    std::vector<double> target = rtde_receive.getActualTCPPose();

    target[0] += x;
    target[1] += y;
    target[2] += z;

    rtde_control.moveL(target, 0.25, 0.5, false);
}




int main(int argc, char* argv[])
{

while (true)
{
    /* code */



/////////// GOING TO INITIAL STARTING POSITION ////////////////////
std::vector<double> joint_q_1 = {-0.000068, -109.030956, -138.951581, 67.982569, 90.000100, 0.000032};

for (size_t i = 0; i < 6; i++)
{
    joint_q_1[i] = (joint_q_1[i] * (3.1415 / 180));
}

////////////////////////////////////////////////////////////////////


//////// MOVING TCP TO POSTION NEED FOR MOVING BOXES ///////////////

int input;


input = 0;
std::cout << "VÆLG BUR 1 ELLER 2: ";

std::cin >> input;


if (input == 1)
{


//// BUR 1 ////

rtde_control.moveJ(joint_q_1, 0.25, 0.25, false);

newTCPOffset(0, 0.72, 0);

newTCPOffset(0.175, 0, 0);

newTCPOffset(-0.05, 0, 0.05);

newTCPOffset(-0.17, 0, 0);

newTCPOffset(-0.05, 0, -0.05);

std::this_thread::sleep_for(std::chrono::milliseconds(2000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

newTCPOffset(0.05, 0, 0);

newTCPOffset(0.535, 0, 0);

newTCPOffset(-0.05, 0, 0.05);

newTCPOffset(-0.53, 0, 0);

newTCPOffset(-0.05, 0, -0.05);


std::this_thread::sleep_for(std::chrono::milliseconds(2000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

newTCPOffset(0.05, 0, 0);

}

else if (input == 2)
{



////////////////////////////////////////////////////////////////////

//// BUR 2 ////

rtde_control.moveJ(joint_q_1, 0.25, 0.25, false);

newTCPOffset(0.175, 0, 0);

newTCPOffset(-0.05, 0, 0.05);

newTCPOffset(-0.17, 0, 0);

newTCPOffset(-0.05, 0, -0.05);

std::this_thread::sleep_for(std::chrono::milliseconds(2000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

newTCPOffset(0.05, 0, 0);

newTCPOffset(0.535, 0, 0);

newTCPOffset(-0.05, 0, 0.05);

newTCPOffset(-0.53, 0, 0);

newTCPOffset(-0.05, 0, -0.05);


std::this_thread::sleep_for(std::chrono::milliseconds(2000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

newTCPOffset(0.05, 0, 0);
}

}

return 0;
}