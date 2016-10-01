import numpy
import random
import time
import logging
from ai import AI
from operator import itemgetter
from pykeyboard import PyKeyboard 


class Population:

	def __init__(self, resume=False, genNumber=1, generation=[]):

		# Create new random generation
		if not resume:
			self.chromosomes = []
			self.generation = 1
			#Initialize a population of 16 with 4 values each
			for x in range(16):
				chromosome = []
				for num in range(4):
					chromosome.append(numpy.random.normal())

				self.chromosomes.append(chromosome)
			# Save the constants
			self.recordGeneration()

		# Continue algorithm with existing generation
		else:
			if generation == []:
				raise Exception('No generation was provided')

			self.chromosomes = generation
			self.generation = genNumber

	def start(self):
	
		while True:
			generationResults = []
			count = 1
			for x in self.chromosomes:
				
				print('Starting ' + str(self.generation) + '.' + str(count) + '\n')
				
				# It'd be faster to just pass chromosomes in to the __init__ function but this method
				# makes more long term sense once values have been settled on
				ai = AI(x[0], x[1], x[2], x[3])
				ai.runAI()

				time.sleep(5)
				pykey = PyKeyboard()
				pykey.tap_key('n')
				result = {'chromosome': x, 'clearedLines': ai.tetris.g.clearedLines, 'score': ai.tetris.g.score}
				generationResults.append(result)
				count += 1

			self.doNaturalSelection(generationResults)


	def doNaturalSelection(self, genResults):
		"""This function removes the worst 25% performing AI as well breeds
		the top 50% performing randomly together"""
		self.generation = self.generation + 1	

		populationSize = len(genResults)
		popQuarter = populationSize / 4
		popHalf = populationSize / 2

		sortedResults = sorted(genResults, key=itemgetter('clearedLines', 'score'))
		
		bottomQuartile = sortedResults[0: int(popQuarter)]
		secondQuartile = sortedResults[int(popQuarter): int(popHalf)]
		topHalf = sortedResults[int(popHalf): int(populationSize)]				
		
		# Write the chromosomes of the best performing ai to constants.py
		bestChromosome = topHalf[-1]['chromosome']
		self.updateConstants(bestChromosome[0], bestChromosome[1], bestChromosome[2], bestChromosome[3])
	
		# Eliminate the lower 25% from self.chromosomes
		for badChrome in bottomQuartile:
			self.chromosomes.remove(badChrome['chromosome'])
		
		# Randomly pair up top half winners
		offspring = []
		while len(topHalf) > 0:
			org1 = random.choice(topHalf)
			topHalf.remove(org1)
			
			org2 = random.choice(topHalf)
			topHalf.remove(org2)

			offspring.append(self.breed([org1, org2]))
		
	
		#Update self.chromosomes with new offspring
		for newOrg in offspring:
			self.chromosomes.append(newOrg)

		self.recordGeneration()
		
	def breed(self, pair):
		"""This function creates new offspring for the next generation by first obtaining 4 chromosomes from 
		the parents. Both parents have a 50% chance of passing on any given chromosome. There then is a 5%
		chance for each chromosome to be mutated +/- 20%"""

		childChromosome = []		
		for i in range(4):

			if random.randint(0,100) < 50:
				newChrome = pair[0]['chromosome'][i]
			else:
				newChrome = pair[1]['chromosome'][i]
		
			if random.randint(0, 100) < 5:
				delta = random.randint(1, 20)
				posORneg = 1 if random.randint(0, 100) > 50 else -1
			
				trueDelta = posORneg * (delta * 0.01 + 1)
				newChrome += trueDelta
			childChromosome.append(newChrome)

		return childChromosome
		

	def updateConstants(self, linesX, agHeightX, holesX, bumpyX):
		
		
		constFile = open('scoreConstants.py', 'w')
		
		constants = str('LINES_CLEARED_MULTIPLIER = ' + str(linesX) + '\n' + 'AGGREGATE_HEIGHT_MULTIPLIER = ' + str(agHeightX) + '\n' + 'HOLES_MULTIPLIER = ' + str(holesX) + '\n' + 'BUMPINESS_MULTIPLIER = ' + str(bumpyX) + '\n')
		constFile.write(constants)
		constFile.close()

	def recordGeneration(self):

		genFile = open('generationHistory.txt', 'a')
		header = '--------GENERATION ' + str(self.generation) + ' --------\n\n'
		footer = '-----------------------------------\n\n'
		genFile.write(header)

		for org in self.chromosomes:
			constants = str('LINES_CLEARED_MULTIPLIER = ' + str(org[0]) + '\n' + 'AGGREGATE_HEIGHT_MULTIPLIER = ' + str(org[1]) + '\n' + 'HOLES_MULTIPLIER = ' + str(org[2]) + '\n' + 'BUMPINESS_MULTIPLIER = ' + str(org[3]) + '\n\n')
		
			genFile.write(constants)
		genFile.write(footer)
		genFile.close()

