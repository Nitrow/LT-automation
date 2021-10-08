#include <ur_rtde/rtde_control_interface.h>
#include <ur_rtde/rtde_receive_interface.h>
#include <chrono>

using namespace ur_rtde;
using namespace std::chrono;


RTDEControlInterface rtde_control("127.0.0.1");
RTDEReceiveInterface rtde_receive("127.0.0.1");

void newTCPOffset (double x, double y, double z)
{   
    
    std::vector<double> target = rtde_receive.getActualTCPPose();

    target[0] += x;
    target[1] += y;
    target[2] += z;

    rtde_control.moveL(target, 0.15, 0.5, false);
}



void forceModeUp ()
{
  std::vector<double> task_frame = {0, 0, 0, 0, 0, 0};
  std::vector<int> selection_vector = {1, 0, 1, 0, 0, 0};
  std::vector<double> ur_up = {-10, 0, 10, 0, 0, 0};
  std::vector<double> limits = {2, 2, 1.5, 1, 1, 1};
  int force_type = 2;
  double dt = 1.0/500; // 2ms

  for (unsigned int i=0; i<3000; i++)
  {
    auto t_start = high_resolution_clock::now();
    if (i > 1000)
      rtde_control.forceMode(task_frame, selection_vector, ur_up, force_type, limits);
    auto t_stop = high_resolution_clock::now();
    auto t_duration = std::chrono::duration<double>(t_stop - t_start);

    if (t_duration.count() < dt)
    {
      std::this_thread::sleep_for(std::chrono::duration<double>(dt - t_duration.count()));
    }
  }
  rtde_control.forceModeStop();

}


int main(int argc, char* argv[])
{




while (true)
{

/////////// GOING TO INITIAL STARTING POSITION ////////////////////
std::vector<double> joint_q_1 = {-0.000068, -109.030956, -138.951581, 67.982569, 90.000100, 0.000032};

for (size_t i = 0; i < 6; i++)
{
    joint_q_1[i] = (joint_q_1[i] * (3.1415 / 180));
}


int input = 0;



std::cout << "VÆLG BUR 1 ELLER 2: ";

std::cin >> input;


if (input == 1)
{


//// BUR 1 ////

rtde_control.moveJ(joint_q_1, 0.25, 0.25, false);

newTCPOffset(0, 0.36, 0);

std::vector<double> home1 = rtde_receive.getActualTCPPose();

newTCPOffset(0.32, 0, 0);

forceModeUp ();

//newTCPOffset(-0.05, 0, 0.05);



newTCPOffset(-0.32, 0, 0);

newTCPOffset(0, 0, -0.03);

newTCPOffset(-0.08, 0, 0);

std::this_thread::sleep_for(std::chrono::milliseconds(4000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

rtde_control.moveL(home1, 0.15, 0.5, false);

newTCPOffset(0.64, 0, 0);

//newTCPOffset(-0.05, 0, 0.05);

forceModeUp ();

newTCPOffset(-0.64, 0, 0);

newTCPOffset(0, 0, -0.03);

newTCPOffset(-0.08, 0, 0);


std::this_thread::sleep_for(std::chrono::milliseconds(4000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT


}

else if (input == 2)
{



////////////////////////////////////////////////////////////////////

//// BUR 2 ////

rtde_control.moveJ(joint_q_1, 0.25, 0.25, false);

newTCPOffset(0, -0.36, 0);

std::vector<double> home2 = rtde_receive.getActualTCPPose();

newTCPOffset(0.32, 0, 0);

//newTCPOffset(-0.05, 0, 0.05);
forceModeUp ();


newTCPOffset(-0.32, 0, 0);



newTCPOffset(0, 0, -0.03);

newTCPOffset(-0.08, 0, 0);

std::this_thread::sleep_for(std::chrono::milliseconds(4000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

rtde_control.moveL(home2, 0.15, 0.5, false);

newTCPOffset(0.64, 0, 0);

forceModeUp ();

//newTCPOffset(-0.05, 0, 0.05);

newTCPOffset(-0.64, 0, 0);

newTCPOffset(0, 0, -0.03);

newTCPOffset(-0.08, 0, 0);

std::this_thread::sleep_for(std::chrono::milliseconds(4000)); ////SLEEP TO GIVE BOX TIME TO MOVE ON CONVAYOR BELT

newTCPOffset(0.05, 0, 0);
}

else
{
  std::cout << "ERROR: Wrong input! \n";
  input = 0;
}


}


return 0;
}