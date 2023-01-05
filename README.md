# agent_queue_action_response.

For Study Agent Queue responses, factorials or stateless conditions is almost similar when you had both stage conditions and game play conditions, and each time request at critical conditions response may change according to the stage conditions but it does not effect AI game play conditions. Sample request for none rims possible actions return ```{ NONE | LEFT | RIGHT | UP | DOWN }``` when you are almost the right corners return ```{ NONE | UP | DOWN }``` and ```{ NONE | LEFT | UP | DOWN }```.

## Staless conditions ##

```
def request_possible_action( self ):
	
		( width, height ) = self.PLE.getScreenDims()
		
		snake_head_x = self.read_current_state( 'snake_head_x' )
		snake_head_y = self.read_current_state( 'snake_head_y' )
		
		stage_position = ( width, height, snake_head_x, snake_head_y )
		possible_actions = ( 1, 1, 1, 1, 1 )
		action = 0
		
		"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
		# ( width, height, snake_head_x, snake_head_y )
		# {'none_1': 104, 'left_1': 97, 'down_1': 115, 'right1': 100, 'up___1': 119}
		
		# ( none, left, down, right, up )
		# ( 0, 0, 0, 0, 0 )
		"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
		list_actions = [['left'], ['down'], ['right'], ['up']]
		
		if stage_position[2] <= 25.0 : 
			list_actions.remove( ['left'] )
		if stage_position[2] >= 488.0 : 
			list_actions.remove( ['right'] )
		
		###
		if stage_position[2] >= 488.0 and snake_head_y == self.previous_snake_head_y: 
			list_actions.remove( ['left'] )
		if stage_position[2] <= 25.0 and snake_head_y == self.previous_snake_head_y: 
			list_actions.remove( ['right'] )
		###

		if stage_position[3] <= 25.0 : 
			list_actions.remove( ['down'] )
		if stage_position[3] >= 488.0 : 
			list_actions.remove( ['down'] )
			
		###
		if stage_position[3] >= 488.0 and snake_head_x == self.previous_snake_head_x: 
			list_actions.remove( ['down'] )
		if stage_position[3] <= 25.0 and snake_head_x == self.previous_snake_head_x: 
			list_actions.remove( ['up'] )
		###

		( idx_1, idx_2, idx_3, idx_4 ) = ( 0, 0, 0, 0 )

		if ['left'] in list_actions :
			idx_1 = 1
		if ['down'] in list_actions :
			idx_2 = 1
		if ['right'] in list_actions :
			idx_3 = 1
		if ['up'] in list_actions :
			idx_4 = 1
		
		self.previous_snake_head_x = snake_head_x
		self.previous_snake_head_y = snake_head_y
	
		possible_actions = [ 0, idx_1, idx_2, idx_3, idx_4 ]
	
		return possible_actions
```


## Files and Directory ##

| File Name | Description |
--- | --- |
| sample.py | sample codes |
| Snake_stage_rims_start_learn_01.gif |data12|
| Snank_AI_vs_Random_10_minutes.gif |data12|
| README.md | readme file |

## Results ##

#### Stage conditions ####

![Stage conditions](https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Snake_stage_rims_start_learn_01.gif "Stage conditions")

#### Randoms play ####

![Play](https://github.com/jkaewprateep/agent_queue_action_response./blob/main/Snank_AI_vs_Random_10_minutes.gif "Play")


