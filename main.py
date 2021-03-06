#
# twobody by don bright ( patreon.com/donbright )
#
# Based on the 'orbits' Java app by John Walker, www.fourmilab.ch
#
# This program attempts to show the orbit of two objects using General 
# Relativity theory of motion. One object is assumed a 'point mass' or 
# 'test mass' of tiny proportion The second object is assumed a 'black 
# hole', non spinning. see www.fourmilab.ch for more details
# 
# This is an update to the olden days of celestial mechanics, wherein 
# philosophers believed the Sun may have formed a circular motion around 
# the Earth, or, later on, that two bodies orbit in a fixed ellipse 
# about each other.
#
# Units are in Kilograms, Meters, Seconds, Radians
# 
# The particle position is stored using Polar coordinates,
# with an Origin point at the center of the Black Hole, 
# and Angle and Radius stored as numbers.
#
# The suffix _q indicates 'quadrance' or squaring of an amount
# which is performed to avoid square roots and floating point problems 

from fractions import Fraction

def render_txt_particle(p):
	s = '['+str(p.angular_momentum)+' '+str(p.angle)+' '+str(p.radius)+' '+str(p.time)+' '+str(p.direction)+']'
	return s

def render_txt_body(b):
	s = '['+str(b.mass)+']'
	return s

class Body:
	def __init__(self):
		self.mass = 1

class Particle:
	inside_blackhole = False
	angular_momentum = 1 # kilograms * meters per second
	angle = 0 # Radians
	radius = 100 # meters
	time = 0 # seconds
	direction = 1 # 1 or -1
	def __init__(self):
		self.created = True #noop
	def __str__(self):
		return render_txt_particle(self)

def effective_potential_energy_q( particle ):
	am = particle.angular_momentum
	m = particle.mass
	r = particle.radius
	return 1-Fraction(2*m,r) * 1+Fraction(am**2,r**2)
	
def update( particle ):
	particle1 = particle
	particle2 = particle
	particle2.radius = current_radius_q
	peq1 = effective_potential_energy_q( particle1 )
	peq2 = effective_potential_energy_q( particle2 )
	dr_dt_q = peq1 - peq2
	current_radius_q += direction * dr_dt_q

	if (current_radius_q < (2*M)**2):
		particle.inside_blackhole = True
	
	delta_angle = Fraction(angular_momentum,current_radius_q)
	angle += delta_angle

	#delta_tee = 1 - Fraction( 2 * particle.mass, current_radius_q )		
		
b = Body()
p = Particle()
print b,p

