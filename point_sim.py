"""
One-dimensional point movement simulation.
Author: Garrek Stemo

"""
import csv
import numpy as np


# xRange = 100
# yRange = 100


class Point:
	"""Set parameters for a point-like object"""
	def __init__(self, mass=1.0, velocity=1.0, position=1.0):
		self.name = "bob"
		#self.length = length
		self.mass = mass
		self.velocity = velocity
    	# area = length ** 2
		self.position = position

	def PrintMass(self):
		print(self.mass)


def unit_vector(body_1, body_2):
	"""Define a unit vector for the force acting on body_1 called r_hat"""
	d = body_2.position - body_1.position
	r_hat = d/ np.sqrt(d ** 2)

	return r_hat


def potential_func(body_1, body_2):
	"""Define the potential function of body_2 that acts on body_1"""
	K = 10.0 ** -11 # force constant, in this case resembling gravitational constant
	m1 = body_1.mass
	m2 = body_2.mass
	d = body_2.position - body_1.position

	if d == 0.0:
		potential = 0.0
	else:
		potential = (m2 / (d ** 2) * K)  # potential at m1 due to m2

	return potential


def velocity_func(body_1, body_2, potential, r_hat, delT):
	"""Define the velocity function that sets the velocity for body_1 using
	the potential at body_1 from body_2 at a given timestep, delT.
	r_hat is the unit vector pointing from body_1 to body_2."""

	body_1.velocity = body_1.velocity + potential * delT * r_hat

	return body_1.velocity


def position_func(body_1, body_2, potential, r_hat, delT):
	"""Define the position function that sets a new position for body_1 given
	a potential, timestep, and unit vector from body_1 to body_2."""

	new_pos = body_1.position + body_1.velocity * delT * r_hat + 0.5 * potential * (delT ** 2) * r_hat
	#print("displacement(", body_1.name, ") = ", body_1.position, "+", body_1.velocity, "*", delT, "*", r_hat, "+ 1/2 * ", potential, "*", delT**2, "*", r_hat)

	return new_pos


def move(body_1, body_2, delT):
	"""Move body_1 and body_2 at a given timestep, delT.
	Return a list of new positions."""

	positions = []

	#print(body_1.name, " OLD position: ", body_1.position)
	#print(body_2.name, " OLD position: ", body_2.position, "\n")

	# Compute potential of body_1 and body_2 and unit vectors
	potential_1 = potential_func(body_1, body_2)
	potential_2 = potential_func(body_2, body_1)
	print("potential A:", potential_1, " potential B:", potential_2)
	r12 = unit_vector(body_1, body_2)
	r21 = unit_vector(body_2, body_1)
	#print("Potential =", potential, " r12 =", r12, " r21 =", r21)

	# Use force to compute new positions for body_1 and body_2. Append to positions list.
	body_1.position = position_func(body_1, body_2, potential_2, r12, delT)
	body_2.position = position_func(body_2, body_1, potential_1, r21, delT)
	positions.append(body_1.position)
	positions.append(body_2.position)

	# Update velocities in objects body_1 and body_2
	body_1.velocity = velocity_func(body_1, body_2, potential_2, r12, delT)
	body_2.velocity = velocity_func(body_2, body_1, potential_1, r21, delT)

	#print(body_1.name, " NEW position: ", positions[0])
	#print(body_2.name, " NEW position: ", positions[1], "\n")

	return positions


def main():

	particle_A = Point()
	particle_A.name = "A"
	particle_A.mass = 100000
	particle_A.position = 0.0
	particle_A.velocity = 0.0

	particle_B = Point()
	particle_B.name = "B"
	particle_B.mass = 100000
	particle_B.position = 100
	particle_B.velocity = 0.0

	fpos = open('pos_data.csv', 'wt')
	pwriter = csv.writer(fpos)
	pwriter.writerow(("Particle A Position", "Particle B Position"))

	# fforce = open('force_data.csv', 'wt')
	# fwriter = csv.writer(fforce)
	# fwriter.writerow(("Force"))

	delT = 0.0
	while delT < 10000:
		#print("\n", "TIME STEP", delT)
		#print("-" * 60)
		moved = move(particle_A, particle_B, delT)
		pwriter.writerow(moved)

		delT += 1
		#print("Final output particle positions: ", moved)

	fpos.close()
	# fforce.close()


if __name__ == "__main__":
    main()
