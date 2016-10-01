from ai import AI
from scoreConstants import *

def run():
	
	ai = AI(LINES_CLEARED_MULTIPLIER, AGGREGATE_HEIGHT_MULTIPLIER, HOLES_MULTIPLIER, BUMPINESS_MULTIPLIER)
	ai.runAI()

run()
