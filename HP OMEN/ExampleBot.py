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
        large_boosts = [boost for boost in agent.boosts if boost.large and boost.active]
        foe_goal_to_ball,foe_ball_distance = (agent.ball.location - agent.foe_goal.location).normalize(True)
        foe_goal_to_foe = agent.foes[0].location - agent.foe_goal.location
        foe_distance = foe_goal_to_ball.dot(foe_goal_to_foe)

        left_field = Vector3(4200*-side(agent.team),agent.ball.location.y + (1000*-side(agent.team)),0)
        right_field = Vector3(4200*side(agent.team),agent.ball.location.y + (1000*side(agent.team)),0)
        targets = {"goal" : (agent.foe_goal.left_post,agent.foe_goal.right_post), "upfield" : (left_field,right_field), "not_my_net" : (agent.friend_goal.right_post, agent.friend_goal.left_post)}
        shots = find_hits(agent,targets)

        me_onside = my_distance - 200 < my_ball_distance
        foe_onside = foe_distance - 200 < foe_ball_distance
        close = (agent.me.location - agent.ball.location).magnitude() < 2000
        have_boost = agent.me.boost > 20
        x = 1
        if agent.team == 0:
            agent.debug_stack()
            agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])
            my_point = agent.friend_goal.location + (my_goal_to_ball * my_distance)
            agent.line(my_point - Vector3(0, 0, 100), my_point + Vector3(0, 0, 100), [0,255,0])


        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
                if agent.me.velocity == 200:
                    agent.push(flip(agent.me.local(agent.foe_goal.location - agent.me.location)))

            elif (close and me_onside) or (not foe_onside and me_onside):


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


            elif (agent.ball.location - agent.friend_goal.location).magnitude() > 8000 and agent.me.boost < 20:
                closest_boost = large_boosts[0]
                for item in large_boosts:
                    if (closest_boost.location - agent.me.location).magnitude() > (
                            item.location - agent.me.location).magnitude():
                        closest_boost = item
                agent.stack = []
                agent.push(goto_boost(closest_boost))

            elif len(shots["not_my_net"]) > 0:
                    agent.push(shots["not_my_net"][0])

            else:
                agent.push(short_shot(agent.foe_goal.location))
