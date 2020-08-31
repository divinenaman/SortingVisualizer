import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.clock import Clock
import time


def bubbleSort(arr):
	n = len(arr)
	steps = []
	for i in range(n-1):
		for j in range(0, n-i-1):
			if arr[j] > arr[j+1]:
				arr[j], arr[j+1] = arr[j+1], arr[j]
				steps.append((j, j+1, 1))
			else:
				steps.append((j, j+1, 0))
	return steps

# Driver code to test above


class Bar(Widget):
	position = ListProperty([0,0])
	def __init__(self, p, n, **kwargs):
		super(Bar, self).__init__(**kwargs)
		with self.canvas.before:
			self.c = Color(1, 0, 0, .5, mode='rgba')
			self.rect = Rectangle(
				pos=(100+(p*100), self.center_y+50), size=(50, 25+(n*4)))
		
		self.label = Label(text=str(n),font_size=str(20))
		self.label.pos=[self.rect.pos[0]-(self.rect.size[0]//2),self.rect.size[1]+self.rect.pos[1]-40]
		self.add_widget(self.label)
		self.pos=[self.rect.pos[0]-40,self.rect.pos[1]]
		
	def on_position(self,instance,pos):
		
		self.rect.pos=pos
		self.label.pos=[self.rect.pos[0]-(self.rect.size[0]//2),self.rect.size[1]+self.rect.pos[1]-40]

	def set_default_color(self):
		self.c.rgba=[1,0,0,0.5]
	def set_highlight_color(self):
		self.c.rgba=[1,0,255,0.5]
	def set_finish_color(self):
		self.c.rgba=[53,169,47,1]

class Cursor(Widget):

	position=ListProperty([0,0])
	def __init__(self, c1=[0,0], c2=[0,0], s1=[0,0], s2=[0,0], **kwargs):
		super(Cursor, self).__init__(**kwargs)

		self.x1 = (2*c1[0]+s1[0])//2
		self.y1 = c1[1]

		self.x2 = (2*c2[0]+s2[0])//2
		self.y2 = c2[1]
		with self.canvas:
			Color(1., 1., 0)
			self.line1 = Line(
				points=[self.x1, self.y1-5, self.x1, self.y1-30], width=2)
			self.line2 = Line(
				points=[self.x2, self.y2-5, self.x2, self.y2-30], width=2)
			self.line3 = Line(
				points=[self.x1, self.y1-30, self.x2, self.y2-30], width=2)
		
	def on_position(self,instance,pos):
		self.x1 = (2*pos[0][0]+pos[2][0])//2
		self.y1 = pos[0][1]

		self.x2 = (2*pos[1][0]+pos[3][0])//2
		self.y2 = pos[1][1]
		self.line1.points = [self.x1, self.y1-5, self.x1, self.y1-30]
		self.line2.points=[self.x2, self.y2-5, self.x2, self.y2-30]
		self.line3.points=[self.x1, self.y1-30, self.x2, self.y2-30]



class InputBar(GridLayout):

	def __init__(self, **kwargs):
		super(InputBar, self).__init__(**kwargs)

		with self.canvas.before:
			Color(240,100,50,mode="hsv")

		self.arr = [64, 34, 25, 12, 22, 11, 90]
		self.a = []
		self.cols = len(self.arr)
		self.n = len(self.arr)
		self.i = 0
		self.move = ()
		copy = self.arr[:]
		self.steps = bubbleSort(copy)
		print(self.arr)
		while(self.i < self.n):
			self.a.append(Bar(self.i, self.arr[self.i]))
			self.add_widget(self.a[self.i])
			self.i = self.i+1
		
		self.cur = Cursor()
		self.add_widget(self.cur)

		self.event = Clock.schedule_interval(self.startSort, 0.5)
		# self.event=Clock.schedule_once(self.sortBar,5)
		# Clock.unschedule(self.event)
		self.counter = -1
		print(self.steps)

	def startSort(self, dt):
		self.counter = self.counter+1
		self.a[self.steps[self.counter-1][0]].set_default_color()
		self.a[self.steps[self.counter-1][1]].set_default_color()
		if self.counter==len(self.steps):
			Clock.unschedule(self.event)
			self.remove_widget(self.cur)
			for i in self.a:
				i.set_finish_color()
			return False
		else:
			self.a[self.steps[self.counter][0]].set_highlight_color()
			self.a[self.steps[self.counter][1]].set_highlight_color()
			self.cur.position=[self.a[self.steps[self.counter][0]].rect.pos, self.a[self.steps[self.counter][1]].rect.pos,self.a[self.steps[self.counter][0]].rect.size, self.a[self.steps[self.counter][1]].rect.size]

		if self.steps[self.counter][2] == 1:
			self.move = self.steps[self.counter]
			self.sortBar()
		#else:
			#self.cur.position=[self.a[self.steps[self.counter][0]].rect.pos,self.a[self.steps[self.counter][1]].rect.pos,self.a[self.steps[self.counter][0]].rect.size, self.a[self.steps[self.counter][1]].rect.size]
			#self.remove_widget(self.cur)
			#self.cur = Cursor(self.a[self.steps[self.counter][0]].rect.pos, self.a[self.steps[self.counter][1]].rect.pos,
			#				  self.a[self.steps[self.counter][0]].rect.size, self.a[self.steps[self.counter][1]].rect.size)
			#self.add_widget(self.cur)

		# bar1=Bar(1,2)
		# self.add_widget(bar1)
		# bar2=Bar(2,3)
		# self.add_widget(bar2)

	def sortBar(self):
		self.a[self.move[0]].position,self.a[self.move[1]].position=self.a[self.move[1]].rect.pos,self.a[self.move[0]].rect.pos
		
		#self.a[self.move[0]].rect.pos, self.a[self.move[1]
		#									  ].rect.pos = self.a[self.move[1]].rect.pos, self.a[self.move[0]].rect.pos
		self.a[self.move[0]], self.a[self.move[1]
									 ] = self.a[self.move[1]], self.a[self.move[0]]
		
		#self.remove_widget(self.cur)
		

		#self.cur = Cursor(self.a[self.steps[self.counter+1][0]].rect.pos, self.a[self.steps[self.counter+1][1]].rect.pos,
						  #self.a[self.steps[self.counter+1][0]].rect.size, self.a[self.steps[self.counter+1][1]].rect.size)
		#self.add_widget(self.cur)


class MyApp(App):

	def build(self):
		self.window=InputBar()
		self.size_hint=(0.5,0.5)
		return self.window


if __name__ == '__main__':

	MyApp().run()
