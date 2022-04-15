
__version__ = '0.4'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from os.path import exists
import json

Builder.load_file("layout.kv")

class MainInfo(BoxLayout):
	pass

class FuncMenu(BoxLayout):
	pass

class RootWidget(BoxLayout):
	buildings = {"castle": 50, "house": 50, "guard": 50, "camp": 50}
	resources = 0
	mines = 0
	soldiers = 0
	residents = 0
	residents_limit = buildings["house"] * 5
	counter = 0
	if residents > residents_limit:
		residents = residents_limit
	labors = residents - soldiers
	def __init__(self, **kwargs):
		super(RootWidget, self).__init__()
		user = kwargs["user"]
		self.data = kwargs["data"][user]
		self.ids["_maininfo"].ids["_resources"].text = \
			str(format(self.data["resources"], ","))
		self.ids["_managepage"].ids["_gather"].bind(on_release=self.gather)

	def gather(self, instance):
		if self.data["buildings"]["castle"] == 0:
			self.data["resources"] += 3
		else:
			self.data["resources"] += self.data["buildings"]["castle"] * 500000
		print(self.data["resources"])

	def update(self):
		self.counter += 1
		if self.counter % 10 == 0:
			self.data["residents"] += self.data["buildings"]["castle"]
			if self.data["buildings"]["castle"] == 0:
				self.data["mines"] += 50
			else:
				self.data["mines"] += self.data["buildings"]["castle"] * 100
		if self.data["residents"] > self.data["buildings"]["house"] * 5:
			self.data["residents"] = self.data["buildings"]["house"] * 5
		#print("residents:", self.data["residents"])
		self.data["resources"] += self.data["residents"] - \
					self.data["soldiers"]
		#print("resources:", self.data["resources"])
		self.ids["_maininfo"].ids["_resources"].text = \
			str(format(self.data["resources"], ","))
		self.ids["_maininfo"].ids["_residents"].text = \
			str(format(self.data["residents"], ","))
		self.labors = self.data["residents"] - self.data["soldiers"]
		self.ids["_maininfo"].ids["_resources_increase"].text = \
			str("{}/s".format(self.labors, ","))
		self.ids["_maininfo"].ids["_residents_increase"].text = \
			str("{}/m".format(self.data["buildings"]["castle"], ","))

		self.ids["_managepage"].ids["_labors"].text = str(format(self.labors, ","))
		self.ids["_managepage"].ids["_mines"].text = str(format(self.data["mines"], ","))

class ManagePage(FloatLayout):
	pass

class GameApp(App):
	user = "admin"
	data_path = "./user_data.json"
	data = {}

	def build(self):
		Window.bind(on_request_close=self.on_quit)
		self.check_user(self.user)
		root = RootWidget(user=self.user, data=self.data)
		Clock.schedule_interval(self._update, 1.0)
		return root

	def _update(self, dt):
		self.root.update()
		self.save_data()

	def create_user(self):
		user_data = {\
		"buildings": {"castle": 50, "house": 50, "guard": 0, "camp": 0},\
		"resources": 0, "residents": 0, "soldiers": 0, "mines": 0}
		self.data[self.user] = user_data

	def check_user(self, user="admin"):
		if not exists(self.data_path):
			self.create_user()
		else:
			with open(self.data_path, "r") as f:
				self.data = json.load(f)
			if not self.user in self.data.keys():
				self.create_user()

	def save_data(self):
		"""
		data = {"admin": {"resources": 0}}
		"""
		self.data[self.user] = self.root.data
		with open(self.data_path, "w") as f:
			json.dump(self.data, f)
		print("saved!")

	def on_quit(self, *args):
		self.save_data()

if __name__ == '__main__':
	GameApp().run()

