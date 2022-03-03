from gettext import find
from tools import  *
from objects import *
from routines import *

#This file is for strategy

class ExampleBot(GoslingAgent):
    def run(agent):
        
        my_goal_to_ball,my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        goal_to_me = agent.me.location - agent.friend_goal.location
        my_distance = my_goal_to_ball.dot(goal_to_me)

        foe_goal_to_ball,foe_ball_distance = (agent.ball.location - agent.foe_goal.location).normalize(True)
        foe_goal_to_foe = agent.foes[0].location - agent.foe_goal.location
        foe_distance = foe_goal_to_ball.dot(foe_goal_to_foe)

        me_onside = my_distance - 200 < my_ball_distance
        foe_onside = foe_distance - 200 < foe_ball_distance
        close = (agent.me.location - agent.ball.location).magnitude() < 2000
        have_boost = agent.me.boost > 20

        if agent.team == 0:
            agent.debug_stack()
            agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])
            my_point = agent.friend_goal.location + (my_goal_to_ball * my_distance)
            agent.line(my_point - Vector3(0, 0, 100), my_point + Vector3(0, 0, 100), [0,255,0])


        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
            elif (close and me_onside) or (not foe_onside and me_onside):
                left_field = Vector3(4200*-side(agent.team),agent.ball.location.y + (1000*-side(agent.team)),0)
                right_field = Vector3(4200*side(agent.team),agent.ball.location.y + (1000*side(agent.team)),0)
                targets = {"goal" : (agent.foe_goal.left_post,agent.foe_goal.right_post), "upfield" : (left_field,right_field)}
                shots = find_hits(agent,targets)
                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                elif len(shots["upfield"]) > 0:
                    agent.push(shots["upfield"][0])
                else: 
                    relative_target = agent.friend_goal.location - agent.me.location
                    angles = defaultPD(agent, agent.me.local(relative_target))
                    defaultThrottle(agent, 2300)
                    if abs(angles[1]) > 0.5 or agent.me.airborne:
                        agent.controller.boost = False
                    if abs(angles[1]) > 2.8 or agent.me.airborne:
                        agent.controller.handbrake = True





