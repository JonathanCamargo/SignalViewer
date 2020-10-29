
#include <iostream>

#include <ros/ros.h>

#include <decision_making/SynchCout.h>
#include <decision_making/BT.h>
#include <decision_making/FSM.h>
#include <decision_making/ROSTask.h>
#include <decision_making/DecisionMaking.h>

using namespace std;
using namespace decision_making;

FSM(gait)
{
	FSM_STATES
	{
		WaitState,		
		EarlyStance,
		LateStance,
		SwingFlexion,
		SwingExtension				
	}
	FSM_START(WaitState);
	FSM_BGN
	{

		FSM_STATE(WaitState)
		{
 			FSM_CALL_TASK(WaitState_Entrypoint) //Entrypoint
			FSM_TRANSITIONS
			{
				//FSM_PRINT_EVENT;
				FSM_ON_EVENT("/EarlyStance", FSM_NEXT(EarlyStance));
//FSM_PRINT_EVENT;
				FSM_ON_EVENT("/LateStance", FSM_NEXT(LateStance));
//FSM_PRINT_EVENT;
				FSM_ON_EVENT("/SwingFlexion", FSM_NEXT(SwingFlexion));
//FSM_PRINT_EVENT;
				FSM_ON_EVENT("/SwingExtension", FSM_NEXT(SwingExtension));
			}
		}
		
		
		FSM_STATE(EarlyStance)
		{
 			FSM_CALL_TASK(EarlyStance_Entrypoint) //Entrypoint
			FSM_TRANSITIONS
			{
				//FSM_PRINT_EVENT;
				FSM_ON_EVENT("/T1", FSM_NEXT(LateStance));
			}
		}
		FSM_STATE(LateStance)
		{
 			FSM_CALL_TASK(LateStance_Entrypoint) //Entrypoint
			FSM_TRANSITIONS
			{
				//FSM_PRINT_EVENT;
		  	        FSM_ON_EVENT("/T2", FSM_NEXT(SwingFlexion));
			}
		}
		FSM_STATE(SwingFlexion)
		{
 			FSM_CALL_TASK(SwingFlexion_Entrypoint) //Entrypoint
			FSM_TRANSITIONS
			{
				//FSM_PRINT_EVENT;
		  	        FSM_ON_EVENT("/T3", FSM_NEXT(SwingExtension));
			}
		}
		FSM_STATE(SwingExtension)
		{
 			FSM_CALL_TASK(SwingExtension_Entrypoint) //Entrypoint
			FSM_TRANSITIONS
			{
				//FSM_PRINT_EVENT;
		  	        FSM_ON_EVENT("/T4", FSM_NEXT(EarlyStance));
			}
		}
	}
	FSM_END
}
