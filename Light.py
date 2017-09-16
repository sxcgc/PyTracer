from Geo.Vector import Vector
import random, math

class Light:
	#This is a base class for all types of lights, holds the common light attributes
	def __init__(self,pos,intensity,color):
		self.pos = pos
		self.intensity = intensity
		self.color = color


class PointLight(Light):
	def __init__(self,pos,intensity = 8000,color = Vector(1,1,1)):
		super().__init__(pos,intensity,color)
		self.type = 'Point'
		self.samples = 1


class DiskLight(Light):
	def __init__(self,pos,radius,intensity = 5000, color = Vector(1,1,1)):
		super().__init__(pos,intensity,color)
		self.type = 'Area'
		self.radius = radius
		self.samples = 16

	def getRandomSample(self):
		#generate a sample point on the disk
		theta = random.random() * math.pi #range [0,2pi)
		randPointOnDisk =self.pos +  Vector(math.cos(theta) * self.radius,0,math.sin(theta) * self.radius)
		return randPointOnDisk
