# agent_queue_action_response ( Single Simultaneous ).

For Study Agent Queue responses, factorials or stateless conditions is almost similar when you had both stage conditions and game play conditions, and each time request at critical conditions response may change according to the stage conditions but it does not effect AI game play conditions. Sample request for none rims possible actions return ```{ NONE | LEFT | RIGHT | UP | DOWN }``` when you are almost the right corners return ```{ NONE | UP | DOWN }``` and ```{ NONE | LEFT | UP | DOWN }```.

Stateless requests are your updated messages with conditions within this example the position of food and the snakes compared to rulers, you can have all possible actions return at any point it is possible to do the actions without considering writing equations for game rules ( Gym games and Retro Gym games had actions space that determined ). We are running on PyGame we can read the possible action set but we need to create rules for the game stage within AgentQueue or equations. The AgentQueue is nothing more than removed negative actions as stage rules. In some competitions we see robots keep rotating themselves or running in and out of the corner that is because of the stage rules ( consult referees for match rules ) or you can train robots for rules but they create the ruler's lines on the fields.
> 👧💬 Referee lines and cameras is the same as width x height that is area explore.

## Stateless conditions ##

For solving the problems you need to list down the question challenges 
1. You cannot hit the wall on any side cause of the new gameplay. 
2. You cannot hit yourself on any side cause of the new gameplay.
3. You cannot move backward in the ongoing direction.
4. You can consume the food for adding scores or new gameplay for minus scores.

🧸💬 You see the wall rules, AI request for possible actions from possible actions ```{ NONE | LEFT | RIGHT | UP | DOWN }```
```
🔍 No wall free for all { ⬆️, ➡️, ⬅️, ⬇️ }
🔍 Left wall { ⬆️, ➡️, ⬇️ }, { ⬆️, ⬇️ }, { ⬇️ }, { ⬆️ }
🔍 Right wall { ⬆️, ⬅️, ⬇️ }, { ⬆️, ⬇️ }, { ⬇️ }, { ⬆️ }
🔍 Top wall { ➡️, ⬅️, ⬇️ }, { ➡️, ⬅️ }, { ⬅️ }, { ➡️ }
🔍 Buttom wall { ⬆️, ➡️, ⬅️ }, { ➡️, ⬅️ }, { ⬅️ }, { ➡️ }
```

## Sample Codes ##

AgentQueue benefits from codes and calculation by removing fewer scores active from a possible list than adding it in that you need multiple lines of list append or assignments.

```
def request_possible_action( self ):
	
    ( width, height ) = self.PLE.getScreenDims()
		
    snake_head_x = self.read_current_state( 'snake_head_x' )
    snake_head_y = self.read_current_state( 'snake_head_y' )
    self.possible_actions = ( 1, 1, 1, 1, 1 )
		
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    # ( width, height, snake_head_x, snake_head_y )
    # {'none_1': 104, 'left_1': 97, 'down_1': 115, 'right1': 100, 'up___1': 119}
		
    # ( none, left, down, right, up )
    # ( 0, 0, 0, 0, 0 )
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""

    stage_position = ( 0, snake_head_x, snake_head_y, 512 - snake_head_x, 512 - snake_head_y )
    stage_position = tf.where([tf.math.greater_equal(stage_position, 35 * tf.ones([5, ]))], [1], [0]).numpy()[0]

    # list_actions = [['left'], ['down'], ['right'], ['up']]
    # stage_position = ( 0, 5, 5, 512 - 5, 512 - 5 )                # ==> right and up			( 0, 0, 0, 1, 1 )	
    # stage_position = ( 0, 5, 512, 512 - 5, 512 - 512 )            # ==> right and down		( 0, 0, 1, 1, 0 )	
    # stage_position = ( 0, 512, 512, 512 - 512, 512 - 512 )        # ==> left and down			( 0, 1, 1, 0, 0 )	
    # stage_position = ( 0, 512, 5, 512 - 512, 512 - 5 )            # ==> left and up			( 0, 1, 0, 0, 1 )
		
    if snake_head_x == self.previous_snake_head_x and snake_head_y > self.previous_snake_head_y : 
        print( "condition 1: moving up" )
        stage_position[2] = 0
    if snake_head_x == self.previous_snake_head_x and snake_head_y < self.previous_snake_head_y : 
        print( "condition 2: moving down" )
        stage_position[4] = 0
			
    if snake_head_y == self.previous_snake_head_y and snake_head_x > self.previous_snake_head_x : 
        print( "condition 3: moving right" )
        stage_position[1] = 0
    if snake_head_y == self.previous_snake_head_y and snake_head_x < self.previous_snake_head_x : 
        print( "condition 4: moving left" )
        stage_position[3] = 0
		
    self.previous_snake_head_x = snake_head_x
    self.previous_snake_head_y = snake_head_y
	
    return stage_position
```
## Sample Outputs ##

It is possible to send the stage rules to AI but it is AI decisions where you applied scores based, time scales, or algorithms and it is no guarantee that AI will follow your rules the AI will select from their learing not fixed conditions that is valid in the competitions.

```
possible_actions: [0 0 1 1 1] to actions: [['down'], ['right'], ['up']]
Seleted: ('right1', 100)
condition 3: moving right
possible_actions: [0 0 1 1 1] to actions: [['down'], ['right'], ['up']]
Seleted: ('right1', 100)
condition 3: moving right
possible_actions: [0 0 1 1 1] to actions: [['down'], ['right'], ['up']]
Seleted: ('right1', 100)
condition 3: moving right
possible_actions: [0 0 1 0 1] to actions: [['down'], ['up']]
conditions robots doing prohibited action
Seleted: ('right1', 100)
```

## Controls ##

Simply controls AI selected move actions, continuous number is primary when using internal sequence summary ``` self.steps + gamescores ``` and input possible actions with conditions ```snake_head_x - food_x``` and ```snake_head_y - food_y``` .

```
contrl = possible_actions[0] * 5
contr2 = possible_actions[1] * 5
contr3 = possible_actions[2] * 5
contr4 = possible_actions[3] * 5
contr5 = possible_actions[4] * 5
contr6 = 1
contr7 = 1
contr8 = 1
contr9 = 1
contr10 = 1
contr11 = 1
contr12 = 1
contr13 = 1
contr14 = snake_head_x - food_x
contr15 = snake_head_y - food_y
contr16 = self.steps + gamescores
```

## Tasks Running ##

Simply as an AgentQueue class method you can implement as templates for many games or actions.

```
AgentQueue = AgentQueue( p )
model = AgentQueue.create_model()

for i in range(nb_frames):
	
    reward = 0
    steps = steps + 1
	
    if p.game_over():
        p.init()
        p.reset_game()
        steps = 0
        lives = 0
        reward = 0
        gamescores = 0
		
    if ( steps == 0 ):
        print('start ... ')

    reward = p.act( AgentQueue.predict_action() )
    gamescores = gamescores + 5 * reward
	
    AgentQueue.update_DATA( reward, gamescores )
	
    if ( reward > 0 ):
        model = AgentQueue.training()
		
    if ( steps % 500 == 0 ):
        model = AgentQueue.training()
		
input('...')
```

## Files and Directory ##

| File Name | Description |
|--- | --- |
| sample.py | sample codes |
| Snake_1_minute_learning.gif | result from staeless actions learning |
| Snake_stage_rims_start_learn_01.gif | result from previous method v.s. random |
| Snank_AI_vs_Random_10_minutes.gif | result from previous method v.s. random |
| Street Fighters as sample.gif | AI Learning, single simultaneous |
| Marios Bros.gif | AI Learning, single simultaneous |
| README.md | readme file |

## Results ##

#### Stage conditions ####

![Stage conditions](https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Snake_stage_rims_start_learn_01.gif "Stage conditions")

#### Stateless conditions ####

The AI fast learning away from invalids actions within 1 minute ( learning time randoms )

![Stateless conditions](https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Snake_1_minute_learning.gif "Stateless conditions")

#### Randoms play ####

![Play](https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Snank_AI_vs_Random_10_minutes.gif "Play")

#### Street Fighters ####

Gym Retro games had actions space or sample but you can create agentQueue for the same purpose. ( The games introduced background layers problems will discuss them later )

![Street Fighters Play](
https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Street%20Fighters%20as%20sample.gif "Street Fighters Play")

#### Mario Bros ####

Mario Bros is a more simple problem for solving but it is equipped by equation expression with stage time elapsed problems.

![Mario Bros](https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Marios%20Bros.gif "Mario Bros")
