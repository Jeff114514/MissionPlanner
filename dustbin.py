'''
Represents nodes in the problem graph or network.
Locatin coordinates can be passed while creating the object or they
will be assigned random values.
'''
from globals import *
import globals
class Dustbin:
	# Good old constructor
	def __init__ (self, x = None, y = None):
		if x == None and y == None:
			self.x = random.randint(0, xMax)
			self.y = random.randint(0, yMax)
			self.id = globals.dustbinInitCnt
			globals.dustbinInitCnt += 1
		else:
			self.x = x
			self.y = y
			if x == -1 and y == -1:
				#temporary id
				self.id = None
			else:
				self.id = -1

	def getX (self):
		return self.x

	def getY (self):
		return self.y

	# Returns distance to the dustbin passed as argument
	def distanceTo (self, db):
		if globals.distanceMatrix is None:
			print("init distance matrix")
			globals.distanceMatrix = globals.initDistanceMatrix()
		if self.id == -1 or db.id == -1:
			xDis = abs(self.getX() - db.getX())
			yDis = abs(self.getY() - db.getY())
			dis = math.sqrt((xDis*xDis) + (yDis*yDis))
		else:
			dis = globals.distanceMatrix[self.id][db.id]
		return dis

	# Gives string representation of the Object with coordinates
	def toString (self):
		s =  '(' + str(self.getX()) + ',' + str(self.getY()) + ')'
		return s

	# Check if cordinates have been assigned or not
	# Dusbins with (-1, -1) as coordinates are created during creation on chromosome objects
	def checkNull(self):
		if self.x == -1:
			return True
		else:
			return False
