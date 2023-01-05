"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PY GAME

https://pygame-learning-environment.readthedocs.io/en/latest/user/games/snake.html

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
from os.path import exists

import tensorflow as tf

import ple
from ple import PLE
from ple.games.snake import Snake as Snake_Game

from pygame.constants import K_a, K_s, K_d, K_w, K_h

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
None
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)
print(physical_devices)
print(config)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Variables
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
actions = { "none_1": K_h, "left_1": K_a, "down_1": K_s, "right1": K_d, "up___1": K_w }

steps = 0
reward = 0
gamescores = 0
nb_frames = 100000000000

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Environment
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
game_console = Snake_Game(width=512, height=512, init_length=3)
p = PLE(game_console, fps=30, display_screen=True, reward_values={})
p.init()

obs = p.getScreenRGB()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Class / Functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class AgentQueue:

	def __init__( self, PLE, momentum = 0.1, learning_rate = 0.0001, batch_size = 100, epochs=1, actions={ "none_1": K_h, "left_1": K_a, "down_1": K_s, "right1": K_d, "up___1": K_w }):
		self.PLE = PLE
		self.previous_snake_head_x = 0
		self.previous_snake_head_y = 0
		self.model = tf.keras.models.Sequential([ ])
		self.momentum = momentum
		self.learning_rate = learning_rate
		self.batch_size = batch_size
		self.epochs = epochs
		self.optimizer = tf.keras.optimizers.SGD( learning_rate=self.learning_rate, momentum=self.momentum, nesterov=False, name='SGD', )
		self.lossfn = tf.keras.losses.MeanSquaredLogarithmicError(reduction=tf.keras.losses.Reduction.AUTO, name='mean_squared_logarithmic_error')
		self.history = []
		
		self.actions = { "none_1": K_h, "left_1": K_a, "down_1": K_s, "right1": K_d, "up___1": K_w }
		self.action = 0
		
		self.lives = 0
		self.reward = 0
		self.steps = 0
		self.gamescores = 0
		
		self.DATA = tf.zeros([1, 1, 1, 16 ], dtype=tf.float32)
		self.LABEL = tf.zeros([1, 1, 1, 1], dtype=tf.float32)
		for i in range(15):
			DATA_row = -9999 * tf.ones([1, 1, 1, 16 ], dtype=tf.float32)		
			self.DATA = tf.experimental.numpy.vstack([self.DATA, DATA_row])
			self.LABEL = tf.experimental.numpy.vstack([self.LABEL, tf.constant(0, shape=(1, 1, 1, 1))])
			
		for i in range(15):
			DATA_row = 9999 * tf.ones([1, 1, 1, 16 ], dtype=tf.float32)			
			self.DATA = tf.experimental.numpy.vstack([self.DATA, DATA_row])
			self.LABEL = tf.experimental.numpy.vstack([self.LABEL, tf.constant(9, shape=(1, 1, 1, 1))])	

		self.LABEL = self.LABEL[-500:,:,:,:]
		self.LABEL = self.LABEL[-500:,:,:,:]
		
		self.dataset = tf.data.Dataset.from_tensor_slices((self.DATA, self.LABEL))
		
		self.checkpoint_path = "F:\\models\\checkpoint\\" + os.path.basename(__file__).split('.')[0] + "\\TF_DataSets_01.h5"
		self.checkpoint_dir = os.path.dirname(self.checkpoint_path)

		if not exists(self.checkpoint_dir) : 
			os.mkdir(self.checkpoint_dir)
			print("Create directory: " + self.checkpoint_dir)
		
		return
		
	def build( self ):
	
		return
	
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
	
		# print( 'stage_position: ' + str( stage_position ) )
	
		# temp_action = [['left'], ['down'], ['right'], ['up']]
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
			
		# print( list_actions )
	
	
		( idx_1, idx_2, idx_3, idx_4 ) = ( 0, 0, 0, 0 )
		# idx_2 = 0
		# idx_3 = 0
		# idx_4 = 0
		if ['left'] in list_actions :
			idx_1 = 1
		if ['down'] in list_actions :
			idx_2 = 1
		if ['right'] in list_actions :
			idx_3 = 1
		if ['up'] in list_actions :
			idx_4 = 1
	
		# x = [ x for a, b, c, d in temp_action ]
		# [['left'], ['right'], ['down']]
	
		# print( x )
		
		self.previous_snake_head_x = snake_head_x
		self.previous_snake_head_y = snake_head_y
	
		possible_actions = [ 0, idx_1, idx_2, idx_3, idx_4 ]
		
		# action = self.random_action( possible_actions )
		# return action
	
		# if ( stage_position[2] >= 485.0 and stage_position[3] >= 45.0  ):
			# print( 'condition 1: { up, down }' )
			
			# possible_actions = ( 0, 0, 1, 0, 1 )
			# action = self.random_action( possible_actions )
			
			# return action
			
		# elif ( stage_position[2] >= 485.0 and stage_position[3] < 45.0  ):
			# print( 'condition 2: { left }' )
			
			# possible_actions = ( 0, 1, 0, 0, 0 )
			# action = self.random_action( possible_actions )
			
			# return action
		
		# elif ( stage_position[2] <= 25.0 and stage_position[3] >= 488.0  ):
			# print( 'condition 3: { right }' )
			
			# possible_actions = ( 0, 0, 0, 1, 0 )
			# action = self.random_action( possible_actions )
			
			# return action
		
		# elif ( stage_position[2] <= 25.0 and stage_position[3] >= 45.0  ):
			# print( 'condition 3: { up, right }' )
			
			# possible_actions = ( 0, 0, 0, 1, 1 )
			# possible_actions = ( 0, 0, 0, 0, 1 )
			# action = self.random_action( possible_actions )
			
			# return action
		
		# elif ( stage_position[2] <= 25.0 and stage_position[3] < 45.0  ):
			# print( 'condition 3: { up }' )
			
			# possible_actions = ( 0, 0, 0, 0, 1 )
			# action = self.random_action( possible_actions )
			
			# return action
			
		# elif ( stage_position[2] >= 470.0 and stage_position[3] > 490.0  ):
			# print( 'condition 4: { down }' )
			
			# possible_actions = ( 0, 0, 1, 0, 0 )
			# action = self.random_action( possible_actions )
			
			# return action
			
		# elif ( stage_position[3] < 45.0  ):
			# print( 'condition 2: { left }' )
			
			# possible_actions = ( 0, 1, 0, 0, 0 )
			# action = self.random_action( possible_actions )
			
			# return action
			
		# elif ( stage_position[2] <= 45.0 ):
			# print( 'condition 2' )
			
		# elif ( stage_position[3] >= 485.0 and stage_position[2] < 485.0 ):
			# print( 'condition 3: { right, down }' )
			
		# elif ( stage_position[3] >= 485.0 ):
			# print( 'condition 4' )
			
		# elif ( stage_position[2] >= 25.0 and stage_position[3] <= 488.0 ):
			# print( 'condition 5: { left, down }' )
			
		# elif ( stage_position[2] < 488.0 and stage_position[3] <= 488.0 ):
			# print( 'condition 2: { left, up }' )

		# if ( stage_position[2] >= 485.0 and stage_position[3] <= 45.0 ):
			# print( 'condition 1' )
			
			# possible_actions = ( 0, 1, 0, 0, 0 )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# action = self.random_action( possible_actions )
			
			# return action
			
		# elif ( stage_position[2] <= 5.0 and stage_position[3] <= 45.0 ):
			# print( 'condition 2' )
			# possible_actions = ( 0, 0, 0, 0, 1 )
			
			# if snake_head_y < self.previous_snake_head_y :
				# possible_actions = ( 0, 0, 0, 1, 1 )
				
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
			
		# elif ( stage_position[3] >= 488.0 and stage_position[2] <= 5.0 ):
			# print( 'condition 3' )
			# possible_actions = ( 0, 0, 0, 1, 0 )
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action	
			
		# elif ( stage_position[3] <= 45.0 and stage_position[2] < 485.0 and stage_position[2] > 15.0 ):
			# print( 'condition 4' )
			# possible_actions = ( 0, 1, 0, 0, 0 )
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
			
		# elif ( stage_position[2] >= 485.0 ):
			# print( 'condition 5' )
			# possible_actions = ( 0, 0, 1, 0, 1 )
			
			# if self.previous_snake_head_y > snake_head_y :
				# possible_actions = ( 0, 1, 1, 0, 1 )
				
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
			
		# elif ( stage_position[3] >= 488.0 ):
			# print( 'condition 6' )
			# possible_actions = ( 0, 1, 0, 1, 0 )
			
			# if snake_head_x > self.previous_snake_head_x  :
				# possible_actions = ( 0, 1, 1, 1, 0 )
				
			# action = self.random_action( possible_actions )

			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
			
		# elif ( stage_position[2] <= 5.0 ):
			# print( 'condition 7' )
			# possible_actions = ( 0, 0, 1, 0, 1 )
			
			# if snake_head_y > self.previous_snake_head_y :
				# possible_actions = ( 0, 0, 1, 1, 1 )
				
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
			
		# elif ( stage_position[3] <= 45.0 ):
			# print( 'condition 8' )
			# possible_actions = ( 0, 1, 0, 1, 0 )
			
			# if self.previous_snake_head_y > snake_head_y :
				# possible_actions = ( 0, 1, 0, 1, 1 )
			
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
			
		# elif ( stage_position[2] > 10.0 and stage_position[2] < 485.0 and stage_position[3] > 45.0 and stage_position[3] < 488.0 ):
			# print( 'free condition' )
			# possible_actions = ( 1, 1, 1, 1, 1 )
			# action = self.random_action( possible_actions )
			
			# self.previous_snake_head_x = snake_head_x
			# self.previous_snake_head_y = snake_head_y
			
			# return action
	
		return possible_actions
		
	def	read_current_state( self, string_gamestate ):
	
		GameState = self.PLE.getGameState()
		
		if string_gamestate in ['snake_head_x']:
			temp = tf.cast( GameState[string_gamestate], dtype=tf.int32 )
			temp = tf.cast( temp, dtype=tf.float32 )
			return temp.numpy()
			
		elif string_gamestate in ['snake_head_y']:
			temp = tf.cast( 512 - GameState[string_gamestate], dtype=tf.int32 )
			temp = tf.cast( temp, dtype=tf.float32 )
			return temp.numpy()
			
		elif string_gamestate in ['food_x']:
			temp = tf.cast( GameState[string_gamestate], dtype=tf.int32 )
			temp = tf.cast( temp, dtype=tf.float32 )
			return temp.numpy()
			
		elif string_gamestate in ['food_y']:
			temp = tf.cast( 512 - GameState[string_gamestate], dtype=tf.int32 )
			temp = tf.cast( temp, dtype=tf.float32 )
			return temp.numpy()
			
		elif string_gamestate in ['snake_body']:
			temp = tf.zeros([n_blocks * 1, ], dtype=tf.float32)
			return temp.numpy()[0]
			
		elif string_gamestate in ['snake_body_pos']:
			temp = tf.zeros([n_blocks * 2, ], dtype=tf.float32)
			return temp.numpy()[0]
			
		return None
		
	def random_action( self, possible_actions ): 

		snake_head_x = self.read_current_state('snake_head_x')
		snake_head_y = self.read_current_state('snake_head_y')
		food_x = self.read_current_state('food_x')
		food_y = self.read_current_state('food_y')

		distance = ( ( abs( snake_head_x - food_x ) + abs( snake_head_y - food_y ) + abs( food_x - snake_head_x ) + abs( food_y - snake_head_y ) ) / 4 )
		
		coeff_01 = distance
		coeff_02 = abs( snake_head_x - food_x )
		coeff_03 = abs( snake_head_y - food_y )
		coeff_04 = abs( food_x - snake_head_x )
		coeff_05 = abs( food_y - snake_head_y )
		
		# coeff_01 = 1
		# coeff_02 = 1
		# coeff_03 = 1
		# coeff_04 = 1
		# coeff_05 = 1
		
		temp = tf.constant( possible_actions, shape=(5, 1), dtype=tf.float32 )
		temp = tf.math.multiply(tf.constant([ coeff_01, coeff_02, coeff_03, coeff_04, coeff_05 ], shape=(5, 1), dtype=tf.float32), temp)
		
		# print( 'possible_actions: ' )
		# print( possible_actions )
		# print( 'temp: ' )
		# print( temp )
		# print( tf.math.argmax(temp, axis=0) )
		
		action = tf.math.argmax(temp, axis=0)
		
		# print( "coeff_01: " + str( coeff_01 ) + " coeff_02: " + str( coeff_02 ) + " coeff_03: " + str( coeff_03 ) + " coeff_04: " + str( coeff_04 ) + " coeff_05: " + str( coeff_05 ) 
	
		# )
		
		self.action = int(action)

		return int(action)

	def create_model( self ):
		input_shape = (1, 16)

		model = tf.keras.models.Sequential([
			tf.keras.layers.InputLayer(input_shape=input_shape),
			
			tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, return_sequences=True, return_state=False)),
			tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, return_sequences=True)),
			
			tf.keras.layers.Dense(256, activation='relu'),
			tf.keras.layers.Dense(256, activation='relu'),
		])
				
		model.add(tf.keras.layers.Flatten())
		model.add(tf.keras.layers.Dense(192))
		model.add(tf.keras.layers.Dense(5))
		model.summary()
		
		model.compile(optimizer=self.optimizer, loss=self.lossfn, metrics=['accuracy'])
		self.model = model

		return model

	def training( self ):
		self.history = model.fit(self.dataset, epochs=self.epochs, callbacks=[custom_callback])
		self.model.save_weights(self.checkpoint_path)
		
		return self.model

	def predict_action( self ):

		predictions = self.model.predict(tf.expand_dims(tf.squeeze(self.DATA), axis=1 ))
		
		self.action = int(tf.math.argmax(predictions[0]))
		
		action_from_list = list(actions.values())[self.action]

		return action_from_list

	def update_DATA( self, reward, gamescores ):
	
		self.steps = self.steps + 1
		self.reward = reward
		self.gamescores = gamescores
		
		list_input = []
	
		snake_head_x = self.read_current_state('snake_head_x')
		snake_head_y = self.read_current_state('snake_head_y')
		food_x = self.read_current_state('food_x')
		food_y = self.read_current_state('food_y')
		
		possible_actions = self.request_possible_action()
		
		distance = ( ( abs( snake_head_x - food_x ) + abs( snake_head_y - food_y ) + abs( food_x - snake_head_x ) + abs( food_y - snake_head_y ) ) / 4 )
		
		contrl = snake_head_x
		contr2 = snake_head_y
		contr3 = food_x
		contr4 = food_y
		contr5 = float(self.DATA[-1:,:,:,0:1])
		contr6 = float(self.DATA[-1:,:,:,1:2])
		contr7 = distance
		contr8 = float(self.DATA[-1:,:,:,7:8])
		contr9 = float(self.DATA[-1:,:,:,9:10])
		contr10 = possible_actions[0]
		contr11 = possible_actions[1]
		contr12 = possible_actions[2]
		contr13 = possible_actions[3]
		contr14 = possible_actions[4]
		contr15 = 1
		contr16 = self.gamescores
		
		list_input.append( contrl )
		list_input.append( contr2 )
		list_input.append( contr3 )
		list_input.append( contr4 )
		list_input.append( contr5 )
		list_input.append( contr6 )
		list_input.append( contr7 )
		list_input.append( contr8 )
		list_input.append( contr9 )
		list_input.append( contr10 )
		list_input.append( contr11 )
		list_input.append( contr12 )
		list_input.append( contr13 )
		list_input.append( contr14 )
		list_input.append( contr15 )
		list_input.append( contr16 )
		
		action_name = list(self.actions.values())[self.action]
		action_name = [ x for ( x, y ) in self.actions.items() if y == action_name]
		
		print( "steps: " + str( self.steps ).zfill(6) + " action: " + str( action_name ) + " contrl: " + str(int(contrl)).zfill(6) + " contr2: " + str(int(contr2)).zfill(6) + " contr3: " +
			str(int(contr3)).zfill(6) + " contr4: " + str(int(contr4)).zfill(6) + " contr5: " + str(int(contr5)).zfill(6) )
	
		print( "steps: " + str( self.steps ).zfill(6) + " gamescores: " + str( self.gamescores ) + " reward: " + str(int( self.reward )).zfill(6)

		)
		
		DATA_row = tf.constant([ list_input ], shape=(1, 1, 1, 16), dtype=tf.float32)	

		self.DATA = tf.experimental.numpy.vstack([self.DATA, DATA_row])
		self.DATA = self.DATA[-500:,:,:,:]
		
		self.LABEL = tf.experimental.numpy.vstack([self.LABEL, tf.constant(self.action, shape=(1, 1, 1, 1))])
		self.LABEL = self.LABEL[-500:,:,:,:]
		
		self.DATA = self.DATA[-500:,:,:,:]
		self.LABEL = self.LABEL[-500:,:,:,:]
	
		return self.DATA, self.LABEL, self.steps

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Callback
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class custom_callback(tf.keras.callbacks.Callback):

	def __init__(self, patience=0):
		self.best_weights = None
		self.best = 999999999999999
		self.patience = patience
	
	def on_train_begin(self, logs={}):
		self.best = 999999999999999
		self.wait = 0
		self.stopped_epoch = 0

	def on_epoch_end(self, epoch, logs={}):
		if(logs['accuracy'] == None) : 
			pass
		
		if logs['loss'] < self.best :
			self.best = logs['loss']
			self.wait = 0
			self.best_weights = self.model.get_weights()
		else :
			self.wait += 1
			if self.wait >= self.patience:
				self.stopped_epoch = epoch
				self.model.stop_training = True
				print("Restoring model weights from the end of the best epoch.")
				self.model.set_weights(self.best_weights)
		
		if self.wait > self.patience :
			self.model.stop_training = True

custom_callback = custom_callback(patience=8)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
: Tasks
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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