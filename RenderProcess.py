import multiprocessing, math, random, numpy
from Vector import Vector
from Ray import Ray
from ObjectList import ObjectList


class RenderProcess(multiprocessing.Process):
	def __init__(self,outputQ,order,width,height,startLine,bucketHeight,objects,cam):
		multiprocessing.Process.__init__(self)
		self.outputQ = outputQ
		self.order = order
		self.width = width
		self.height = height
		self.startLine = startLine
		self.bucketHeight = bucketHeight
		self.objects = objects #includes geometries and lights
		self.cam = cam
		#QImage pickling is not supported at the moment. PIL doesn't support 32 bit RGB.
		
	def run(self):
		#bucket rendered color data is stored in an array
		bucketArray = numpy.ndarray(shape=(self.bucketHeight,self.width,3),dtype = numpy.uint8)

		#----shoot rays-------
		for j in range(self.startLine,self.startLine + self.bucketHeight):
			for i in range(0,self.width):
				#shoot 4 rays each pixel for anti-aliasing
				col = Vector(0,0,0)
				AAsample = 1
				for k in range(0,AAsample):
					rayDir = Vector(i + random.random() - self.width/2, -j - random.random() + self.height/2, 
									-0.5*self.width/math.tan(math.radians(self.cam.angle/2))) #Warning!!!!! Convert to radian!!!!!!!
					ray = Ray(self.cam.pos,rayDir)

					#----check intersections with spheres----
					#hitResult is a list storing calculated data [hit_t, hit_pos,hit_normal]
					hitResult = [] 
					hitBool = self.objects.getClosestIntersection(ray,hitResult)

					col = col + self.getColor(hitBool,hitResult)

				averageCol = col / AAsample
				bucketArray[j%self.bucketHeight,i] = [int(averageCol.x),int(averageCol.y),int(averageCol.z)]

		self.outputQ.put((self.order,bucketArray))
		print("Bucket Finished - " + multiprocessing.current_process().name)

	def getColor(self,hit,hitResult):
		#hit is bool,
		if hit == True:
			#shadow ray---------temp implementation-----
			lightPos = self.objects.lights[0].pos
			shadowRayDir = lightPos - hitResult[1]
			offsetOrigin = hitResult[1] + shadowRayDir.normalized() * 0.0001 #slightly offset the ray start point because the origin itself is a root
			shadowRay = Ray(offsetOrigin,shadowRayDir)
			temp_t = shadowRayDir.length()
			shadowRayResult = [temp_t]
			shadowBool = self.objects.getClosestIntersection(shadowRay,shadowRayResult)
			if shadowBool:
				return Vector(0,0,0)
			else:
				return Vector(255,255,255) * numpy.interp(1/math.pow(temp_t,2),[0,0.001],[0,1])
			#------------------------------------------

			# remapHitNormal = (hitResult[2]+Vector(1,1,1))*0.5
			# return Vector(255*remapHitNormal.x,255*remapHitNormal.y,255*remapHitNormal.z)
		else:
			return Vector(0,0,0)