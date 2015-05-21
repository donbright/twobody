import math, sys

class Graphics:
 def __init__(self):
  self.name='graphics1'
 def drawImage(self,*args):
  print 'Graphics.drawImage'

class Image:
 def __init__(self):
  self.name='image1'
 def __init__(self,w,h):
  self.name='image1'
  self.w=w
  self.h=h

class orbitViewer:
 def __init__(self):
  self.name='ov1'
 def remake(self):
  print 'ov.remake'
 def setParticlePosition(self,rad,phi,tee):
  print 'ov.setparticlepos',rad,phi,tee

class Dimension:
 def __init__(self,w,h):
  self.name='dimension1'
  self.width=w
  self.height=h

class energyPlot:
 build = ""
 initialised = False
 chart = None
 ov = orbitViewer()
 sv = orbitViewer()
 reentry = 0
 ANG = 3.57         # Angular momentum
 M = 1.0            # Mass
 FROM = 0.1         # Minimum radius to plot
 TO = 12.0          # Maximum radius to plot
 LOW = 0.92 
 HIGH = 1.05 # Range of chart
 currentR = 4.86
 eParticle = 0
 phi = 0.0
 phiscale = 1
 tee = 0.0
 teescale = 0.1

 eminv = HIGH
 eminR = 0
 direction = -1
    
 # Constructors

 def __init__(self,width, height, graphicsobj):
  print 'init'
  print 'super(width, height):'
  self.initialised = True
  self.graphics = graphicsobj
  self.size = Dimension(width,height)

  #  SETORBITVIEWER  --  Set peer orbit viewer

 def setOrbitViewer(self,newov):
  self.ov = newov

    #  SETSCHWARZSCHILD  --  Set peer Schwarzschild metric viewer

 def setSchwarzschild(self,news):
  self.sv = news

    #  UPDATEPEERS  --  Update peer displays, if any

 def updatePeers(self, rn, phin, teen):
  if (self.ov != None):
   self.ov.currentR = rn
   self.ov.setParticlePosition(rn, phin, teen)
  if (self.sv != None):
   self.sv.currentR = rn
   self.sv.setParticlePosition(rn, phin, teen)

#    /*  SETPARTICLEPOSITION  --  This is called by peers to
#                                 reset our state when a mouse click
#                                 occurs in a peer component.  */

 def setParticlePosition(self, srad, sphi, stee):
  self.currentR = srad
  self.eParticle = self.gEnergy(self.currentR)
  if self.currentR > self.eminR:
   self.direction = 1
  else:
   self.direction = -1
  self.phi = sphi
  self.tee = stee
  refreshDisplay()
  initialised = True

    #  RESTART  --  Reset when global parameter changed

 def restart(self):
  print 'restart'
  if (self.ANG * self.ANG < 12 * (self.M * self.M)):
   self.eminR = sys.float_info.max # Double.MAX_VALUE
   self.eminv = 0.9
  else:
   self.eminR = self.ANG * (self.ANG + math.sqrt(self.ANG * self.ANG - 12 * (self.M * self.M))) / (2 * self.M)
   self.eminv = self.gEnergy(self.eminR)
   self.TO = self.eminR * (7 / 4.0)
  if (self.sv != None and self.ov != None):
   self.sv.TO = self.ov.TO = self.TO
   self.ov.remake()
  self.validate()
  self.repaint()

 def repaint(self):
  self.paintWindow(self.graphics)
    #  MOUSEDOWN  --  Reset radius by mouse click in window

 def mouseDown(self, evt, x, y):
  self.currentR = self.FROM + (x * (self.TO - self.FROM)) / (self.size.width - 1)
  print 'self.currentR:',self.currentR
  self.phi = 0
  self.tee = 0
  self.eParticle = self.gEnergy(self.currentR)
  if self.currentR > self.eminR:
   self.direction = 1
  else:
   self.direction = -1
  #self.direction = self.currentR > self.eminR ? 1 : -1
  updatePeers(self.currentR, self.phi, self.tee)
  if (self.ov != None):
   self.ov.validate()
  repaint()
  return True

    #  GENERGY  --  Calculate effective potential for a given radius

 def gEnergy(self,r):
  return math.sqrt((1.0 - ((2.0 * self.M) / r)) * (1.0 + (self.ANG * self.ANG) / (r * r)))

    #  FILLCIRCLE  --  Draw a filled circle with a given centre and radius

 def fillCircle(self,g, x, y, radius):
  print 'circle ', x,y,radius

    #  PAINTWINDOW  --  Paint the component window
    
 def paintWindow(self,g):
  print 'paintWindow',g
  if (self.initialised):
   print 'already initted'
   s, x, y, px = 0, 0, 0, 0
   py = 0.0
   dr = 0.0
   dr_dt = 0.0
   if (self.chart == None):
     gfx = Graphics()
     plot = 0.0
     scaling = False
     title = "Effective Potential" + '1.0'
     #FontMetrics fm

     #  Create chart image

     self.chart = Image(self.size.width, self.size.height)
     #gfx = self.chart.getGraphics()
     #gfx.setColor(Color.lightGray)
     #gfx.fillRect(0, 0, self.size.width, self.size.height)

     #gfx.setColor(Color.yellow)

     scaling = True
     self.LOW = sys.float_info.max # Double.MAX_VALUE
     self.HIGH = sys.float_info.min # Double.MIN_VALUE
     self.eminv = sys.float_info.max # Double.MAX_VALUE
     if (self.ANG * self.ANG < 12 * (self.M * self.M)):
      self.eminR = sys.float_info.max # Double.MAX_VALUE
      self.eminv = 0.9
     else:
      self.eminR = self.ANG * (self.ANG + math.sqrt(self.ANG * self.ANG - 12 * (self.M * self.M))) / (2 * self.M)
      self.eminv = self.gEnergy(self.eminR)
      self.TO = self.sv.TO = self.ov.TO = self.eminR * (7 / 4.0)
      self.ov.remake()
     while (True):
#            /* Plot the effective potential curve.  We have to
#              explicitly exclude points within the event horizon
#              because the test for infinite values doesn't work
#              on some browser implementations of Java. */

      for x in range(0,self.size.width):
       sx = 0.0
       plot = self.FROM + (x * (self.TO - self.FROM)) / (self.size.width - 1)
       if (plot > (2.0 * self.M)):
        plot = self.gEnergy(plot)
        if (scaling and not math.isinf(plot) and not math.isnan(plot)):
         self.LOW = min(self.LOW, plot)
         self.HIGH = max(self.HIGH, plot)
        else:
         if (plot > self.HIGH):
          plot = self.HIGH
         if (plot >= self.LOW):
          y = (int) ((self.size.height - 1) - (self.size.height - 1) * (plot - self.LOW) / (self.HIGH - self.LOW))
          #gfx.drawLine(x, self.size.height - 1, x, y)
      if (scaling):
       scaling = False
       self.LOW = self.eminv - (self.HIGH - self.eminv) / 10
       self.HIGH += (self.HIGH - self.LOW) / 10
      else:
       break

          #  Plot minimum energy point on chart

     if (self.eminR < sys.float_info.max): #Double.MAX_VALUE):
      ex = (int) (((self.eminR - self.FROM) * self.size.width) / (self.TO - self.FROM))
      #gfx.setColor(Color.green)
      #gfx.drawLine(ex, 0, ex, self.size.height - 1)

          #  Paint title at top of window

      #gfx.setColor(Color.black)
      #gfx.setFont(new Font("Helvetica", Font.BOLD, self.size.height / 12))
      #fm = gfx.getFontMetrics()
      #gfx.drawString(title,(self.size.width - fm.stringWidth(title)) / 2,fm.getAscent())
      self.eParticle = self.gEnergy(self.currentR)

      #  Paint the underlying chart image.

   g.drawImage(self.chart, 0, 0, self)

      #  Plot particle at current radius on effective potential curve

   s = (int) (((self.currentR - self.FROM) * self.size.width) / (self.TO - self.FROM))
   #g.setColor(Color.red)
   y = (int) ((self.size.height - 1) - (self.size.height - 1) * (self.gEnergy(self.currentR) - self.LOW) / (self.HIGH - self.LOW))
   self.fillCircle(g, s, y, 5)

      #  Update current R, self.phi, and tee

   if (self.currentR > 0):
    self.updatePeers(self.currentR, self.phi, self.tee)
    dr_dt = math.sqrt(self.eParticle * self.eParticle - self.gEnergy(self.currentR) * self.gEnergy(self.currentR))
    self.currentR += self.direction * dr_dt

#          /* If the particle fell into the black hole, play the
#           sound accompanying that event. */

    if (self.currentR <= (2 * self.M)):
     self.currentR = -1    # Mark particle as having fallen in
     if (sound != None):
      sound.play()
     updatePeers(self.currentR, self.phi, self.tee)   # Tell peers to hide particle

#          /* When particle's energy increases compared to the last
#          time and we were in the self.direction of increased radius,
#          inform the orbit viewer that we've just passed aphelion,
#          which should be marked on the plot to show precession. */

    elif (self.gEnergy(self.currentR) >= self.eParticle):
     if (self.direction > 0):
      if (self.ov != None):
       self.ov.markApAstron()
     self.direction *= -1
     s = (int) (((self.currentR - self.FROM) * self.size.width) / (self.TO - self.FROM))
     while (self.gEnergy(self.FROM + ((self.TO - self.FROM) * s) / self.size.width) >= self.eParticle):
      s += self.direction
     self.currentR = self.FROM + ((self.TO - self.FROM) * s) / self.size.width
    dPhi = self.ANG / (self.currentR * self.currentR)
    self.phi += dPhi

    if (self.currentR > 2 * self.M):
     dTee = (1 - (2 * self.M) / self.currentR)
     self.tee += dTee

#    /*  VALIDATE  --  We need to know when the layout manager
#                      changes our self.size so we can regenerate the
#                      face bitmap on the next paint request.  */

 def validate(self):
  print 'super.validate()'
  print 'self.size = new Dimension(self.size())'
  chart = None


g = Graphics()
e = energyPlot(100,100,g)
e.restart()
for i in range(0,10):
	e.paintWindow(g)

