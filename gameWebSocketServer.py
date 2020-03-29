from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from colorama import init as Init, Fore, Back, Style
from copy import deepcopy as Deepcopy
from datetime import date as Date, datetime as Datetime
from math import pi as PI, cos as Cos, sin as Sin, atan2 as Atan2, sqrt as Sqrt, radians as Radians, ceil as Ceil
from os import system as System
from os.path import exists as Exists
from random import random as Random, shuffle as Shuffle
from re import compile as Compile, sub as Sub
from threading import Thread
from time import strftime as Strftime, gmtime as Gmtime, sleep as Sleep, time as Time



global USED_NAMES,PLAYERS,CHAT,DECODE_CONSOLE_CHAT,END,BANS


NOISE_OFFSET=[Random()*10,Random()*10,Random()*10]



PRINT_QUEUE=[]
SOCKETS=[]
PACKETS={
	"already_address_connected": "ac%s",
	"start_game": "sp",
	"texture_pack": "tp%s",
	"setup_name": "sn%i:%s",
	"setup_board": "sb%s",
	"setup_data": "sd%i:%s:%i:%i:%i:%s",
	"join": "jn%i",
	"wait_status": "ws%s",
	"drop_plane": "dp%i:%i:%i:%i:%i:%i",
	"no_drop_plane": "np",
	"name_change_true": "nt%s",
	"name_change_false": "nf%s:%i",
	"name_change": "nc%i:%s",
	"mainhand": "mh%i:%s",
	"inventory": "iv%s",
	"move": "mv%i:%i:%i:%i",
	"bullet_data": "bl%s",
	"hp": "hp%i",
	"item": "it%i:%i:%i:%i:%i:%s",
	"coins": "cd%i",
	"rm_item": "ri%i",
	"del_loot_chest": "rc%i",
	"remove_player": "rp%i",
	"leave": "lv%i",
	"kick": "kk%i",
	"private_kick": "pk%s",
	"banned": "bn%i:%s",
	"server_close": "sc%s"
}
USED_NAMES=[]
NEW_PLAYER_TEMPLATE="Player #%i"
IDS={}
PLAYERS={}
PREVENT_PLAYER_ESCAPED_NAMES=False
NEXT_ID=0
MIN_NAME_LENGTH=3
MAX_NAME_LENGTH=20
CHAT=True
DECODE_CONSOLE_CHAT=True
LOG_FILE_PATH="./log/"
LOG_MOVE_PACKETS=False
LOG_INV_DATA=False
END=False
BANS={}
WEB_CONSOLE=True
CONSOLE_SERVER=None
COMMAND_SPLIT_TOKEN="||"
CONSOLE_CLIENTS=[]
HELP={
	"ADMIN": "&&MAGENTA,NORMAL&&ADMIN &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&ADMIN&&YELLOW,BRIGHT&&:&&CYAN,BRIGHT&&{&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Player ID&&GREEN,BRIGHT&&]&&YELLOW,BRIGHT&&:&&CYAN,BRIGHT&&{&&WHITE,BRIGHT&&yes&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&no&&CYAN,BRIGHT&&}&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&list&&CYAN,BRIGHT&&}\n&&BLACK,BRIGHT&&Gives/Removes admin from a player or lists all admins\n&&MAGENTA,BRIGHT&&Parameters:\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Player ID: &&CYAN,NORMAL&&ID of the player that will gain/lose admin (Can be easily aquired with the &&BLUE,BRIGHT&&LIST&&CYAN,NORMAL&& command)\n&&YELLOW,NORMAL&&-> &&MAGENTA,BRIGHT&&Parameters:\n&&YELLOW,NORMAL&&  -> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&yes&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&:&&CYAN,NORMAL&& Indicates,that the player will gain admin\n&&YELLOW,NORMAL&&  -> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&no&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Indicates,that the player will lose admin\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&list&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Indicates,that all admins will be listed",

	"BAN": "&&MAGENTA,NORMAL&&BAN &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&BAN&&YELLOW,BRIGHT&&:&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Player ID&&GREEN,BRIGHT&&]&&YELLOW,BRIGHT&&:&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Time&&GREEN,BRIGHT&&]&&YELLOW,BRIGHT&&:&&MAGENTA,BRIGHT&&(&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Reason&&GREEN,BRIGHT&&]&&MAGENTA,BRIGHT&&)\n&&BLACK,BRIGHT&&Bans a player from the server for a specific amount of time\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Player ID:&&CYAN,NORMAL&& ID of the player that will be banned (Can be easily aquired with the &&BLUE,BRIGHT&&LIST&&CYAN,NORMAL&& command)\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Time: &&CYAN,NORMAL&&Time that the player will be banned for (ex. BAN:0:1y 2m 3d 4h 5mn -> Player with ID 0 will be banned for 1 year 2 months 3 days 4 hours and 5 minutes)\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Reason &&MAGENTA,BRIGHT&&(optional)&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Reason of the ban. If not specified,the default reason is &&GREEN,BRIGHT&&'&&CYAN,BRIGHT&&Manual ban&&GREEN,BRIGHT&&'",

	"CHAT": "&&MAGENTA,NORMAL&&CHAT &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&CHAT&&YELLOW,BRIGHT&&:&&CYAN,BRIGHT&&{&&WHITE,BRIGHT&&on&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&off&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&decode&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&no-decode&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&log-move&&CYAN,BRIGHT&&/&&WHITE,BRIGHT&&no-log-move&&CYAN,BRIGHT&&}\n&&BLACK,BRIGHT&&Turns on/off chat decoding or the whole chat\n&&MAGENTA,BRIGHT&&Parameters:\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&on&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns on the whole chat\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&off&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns off the whole chat\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&decode&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns on chat decoding\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&no-decode&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns off chat decoding\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&log-move&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns on move packet logging\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&no-log-move&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns off move packet logging\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&log-inv&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns on inventory data packet logging\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&no-log-inv&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Turns off move inventory data logging",

	"CLEAR": "&&MAGENTA,NORMAL&&CLEAR &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&CLEAR\n&&BLACK,BRIGHT&&Clears the console",

	"HELP": "&&MAGENTA,NORMAL&&HELP &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&HELP&&YELLOW,BRIGHT&&:&&CYAN,BRIGHT&&{&&WHITE,BRIGHT&&all&&CYAN,BRIGHT&&/&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Command name&&GREEN,BRIGHT&&]&&CYAN,BRIGHT&&}\n&&BLACK,BRIGHT&&Displays help documentation for a specific command or for all of them\n&&MAGENTA,BRIGHT&&Parameters:\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&all&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Indicates,that help for all commands should be displayed\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& Command name:&&CYAN,NORMAL&& String indictaing what command help documentation should be displayed",

	"KICK": "&&MAGENTA,NORMAL&&KICK &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&KICK&&YELLOW,BRIGHT&&:&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Player ID&&GREEN,BRIGHT&&]&&YELLOW,BRIGHT&&:&&MAGENTA,BRIGHT&&(&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Reason&&GREEN,BRIGHT&&]&&MAGENTA,BRIGHT&&)\n&&BLACK,BRIGHT&&Kicks a player from the server\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Player ID:&&CYAN,NORMAL&& ID of the player that will be kicked (Can be easily aquired with the &&BLUE,BRIGHT&&LIST&&CYAN,NORMAL&& command)\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Reason &&MAGENTA,BRIGHT&&(optional)&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Reason of the kick. If not specified,the default reason is &&GREEN,BRIGHT&&'&&CYAN,BRIGHT&&Manual kick&&GREEN,BRIGHT&&'",

	"LIST": "&&MAGENTA,NORMAL&&LIST &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&LIST&&YELLOW,BRIGHT&&:&&CYAN,BRIGHT&&{&&WHITE,BRIGHT&&all&&CYAN,BRIGHT&&/&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Player ID&&GREEN,BRIGHT&&]&&CYAN,BRIGHT&&}\n&&BLACK,BRIGHT&&Lists player data of all players or one specific player\n&&MAGENTA,BRIGHT&&Parameters:\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&all&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Indicates,that data of all players should be displayed\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& Player ID:&&CYAN,NORMAL&& ID indictaing what player's data should be displayed",

	"STOP": "&&MAGENTA,NORMAL&&STOP &&YELLOW,NORMAL&&=> &&BLUE,BRIGHT&&STOP&&YELLOW,BRIGHT&&:&&MAGENTA,BRIGHT&&(&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Reason&&GREEN,BRIGHT&&]&&MAGENTA,BRIGHT&&)\n&&BLACK,BRIGHT&&Stops the server\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&Reason &&MAGENTA,BRIGHT&&(optional)&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Reason of the shutdown. If not specified,the default reason is &&GREEN,BRIGHT&&'&&CYAN,BRIGHT&&Manual shutdown&&GREEN,BRIGHT&&'",

	"UNBAN": "&&MAGENTA,NORMAL&&UNBAN&&YELLOW,NORMAL&& => &&BLUE,BRIGHT&&UNBAN&&YELLOW,BRIGHT&&:&&CYAN,BRIGHT&&{&&WHITE,BRIGHT&&all&&CYAN,BRIGHT&&/&&GREEN,BRIGHT&&[&&WHITE,BRIGHT&&Player ID&&GREEN,BRIGHT&&]&&CYAN,BRIGHT&&}\n&&BLACK,BRIGHT&&Unbans a plyers from the server\n&&MAGENTA,BRIGHT&&Parameters:\n&&YELLOW,NORMAL&&-> &&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&all&&GREEN,BRIGHT&&'&&WHITE,BRIGHT&&: &&CYAN,NORMAL&&Indicates,that all players will be unbanned\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& Player ID: &&CYAN,NORMAL&&ID of the player that will be unbanned (Can be easily aquired with the &&BLUE,BRIGHT&&LIST&&CYAN,NORMAL&& command)"
}



MAX_GAME_START_WAIT_TIME=2
MIN_GAME_PLAYERS=1
MAX_GAME_PLAYERS=20
PLAYER_MAX_MOVE_SPEED=20
PLAYER_NOMOVE_CIRCLE_RADIUS=50
PLAYER_WATER_SPEED_PROC=0.3
GAME_BOARD_WIDTH=30000
GAME_BOARD_HEIGHT=30000
START_X=GAME_BOARD_WIDTH/2
START_Y=GAME_BOARD_HEIGHT/2
GAMES=[]



DEFAULT_TEXTURE_PACK={
	"world": {
		"grass": "#009800",
		"grass_border": "#008400",
		"water": "#007ac0",
		"sand": "#fae6b9",
		"sand_border": "#e6d2a5",
		"bridge": "#6e3700",
		"path": "#a56e36",
		"min_tree": "#026d10",
		"max_tree": "#07b21d"
	},
	"object": {
		"coin": "#f0dc0a",
		"coin_border": "#dcc800",
		"loot_chest": "#966e3c",
		"loot_chest_border": "#78501e",
		"bullet": "#afafaf",
		"bullet_border": "#9b9b9b",
		"drop_plane": "#f0f0f0",
		"drop_plane_border": "#c8c8c8",
	},
	"player": {
		"body": "#ffd296",
		"body_border": "#0a0a0a",
		"nametag": "#050505"
	},
	"map": {
		"loot_chest": "#dc0a0a",
		"drop_plane_A": "#008cdc",
		"drop_plane_B": "#003cdc",
		"other_player": "#4628dc",
		"current_player": "#e61e3c"
	},
	"gui": {
		"border": "#fafafa",
		"main_hand_border": "#c83232",
		"other_slot_border": "#fafafa",
		"slot": "#00000014",
		"slot_overlay": "#ffffff80",
		"small_slot_text": "#0f0f0f",
		"big_slot_text": "#0f0f0f",
		"heart": "#fa0a14",
		"heart_border": "#000000",
		"coin_text": "#0a0a0a",
		"spectating_text": "#323232",
		"spectating_name_text": "#f01414",
		"wait_status_text": "#323232"
	},
	"menu": {
		"pause": "#00000080",
		"main": "#ffffff",
		"button": "#00ff80",
		"button_border": "#00dc64",
		"button_text": "#0f0f0f",
		"play_button": "#28b41e",
		"play_button_border": "#0a9600",
		"play_button_text": "#005a00"
	},
	"settings": {
		"cover_bg": "#000000",
		"icon": "#303030",
		"bg": "#646464",
		"border": "#7b7b7b",
		"name_text": "#e0e0e0",
		"name": "#eb3a11"
	},
	"other": {
		"grid": "#323232",
		"mouse": "#00000028"
	}
}
START_COINS=10
DROP_PLANE_SPEED=1000
DROP_PLANE_END_DIST=800
MAX_INTERACT_DIST=1200
MIN_ITEM_PICKUP_DELAY=2.5
MIN_PICKUP_DIST=100
MIN_LOOT_CHEST_ITEMS=5
MAX_LOOT_CHEST_ITEMS=20
LOOT_CHEST_SIZE=100
GUN_DATA={
	"basic": {
		"id": 0,
		"name": "Basic",
		"proc": 50,
		"types": [
			{
				"name": "Basic Pistol",
				"total_ammo": 6,
				"reload_time": 1.1,
				"cooldown": 0.1,
				"proc": 50,
				"bullets": {
					"damage": 11.5,
					"range": 1000,
					"speed": 10000
				}
			},
			{
				"name": "Basic Pistol #2",
				"total_ammo": 15,
				"reload_time": 0.7,
				"cooldown": 0.2,
				"proc": 50,
				"bullets": {
					"damage": 4,
					"range": 1000,
					"speed": 100
				}
			}
		]
	}
	# rare
	# legendary
	# mythic
}



def print_queue(*a):
	s=""
	for i in range(0,len(a)):
		s+=str(a[i])+" "
	s=s[:len(s)-1]
	def _print():
		s=PRINT_QUEUE[0]
		print(s)
		PRINT_QUEUE.remove(s)
		if (len(PRINT_QUEUE)>0):
			thr=Thread(target=_print,args=(),kwargs={})
			thr.deamon=True
			thr.start()
	PRINT_QUEUE.append(s)
	if (len(PRINT_QUEUE)==1):
		thr=Thread(target=_print,args=(),kwargs={})
		thr.deamon=True
		thr.start()



def format(s):
	fn={"BLACK":Fore.BLACK,"RED":Fore.RED,"GREEN":Fore.GREEN,"YELLOW":Fore.YELLOW,"BLUE":Fore.BLUE,"MAGENTA":Fore.MAGENTA,"CYAN":Fore.CYAN,"WHITE":Fore.WHITE,"RESET":Fore.RESET}
	bk={"bBLACK":Back.BLACK,"bRED":Back.RED,"bGREEN":Back.GREEN,"bYELLOW":Back.YELLOW,"bBLUE":Back.BLUE,"bMAGENTA":Back.MAGENTA,"bCYAN":Back.CYAN,"bWHITE":Back.WHITE,"bRESET":Back.RESET}
	st={"NORMAL":Style.NORMAL,"BRIGHT":Style.BRIGHT,"RESET_ALL":Style.RESET_ALL}
	def rpl(o):
		o=o.group(1)
		l=""
		for k in o.split(","):
			if (k in fn.keys()):l+=fn[k]
			if (k in bk.keys()):l+=bk[k]
			if (k in st.keys()):l+=st[k]
		return l
	return Sub("&&([^&]+)&&",rpl,s)+Style.RESET_ALL
def blank_format(s):
	return Sub("&&([^&]+)&&","",s)



def log(m):
	date=Date.today()
	fp=LOG_FILE_PATH+Strftime("%d_%m_%y",Gmtime())+".log"
	with open(fp,"a") as f:
		f.write(blank_format(m)+"\n")
	if (CHAT==True):
		print_queue(format(m))
		for c in CONSOLE_CLIENTS:
			c.sendConsoleMessage("tx"+m)



class World:
	def __init__(self,GAME):
		self.GAME=GAME
		self.BOARD_WIDTH=GAME_BOARD_WIDTH
		self.BOARD_HEIGHT=GAME_BOARD_HEIGHT
		self.CLASS_NAME="WORLD"
		self.DONE=False
		self.board={}
		self.GROUND_POINTS_PER_SIDE=300
		self.GROUND_START_RECT_OFFSET=700
		self.ISLAND_TYPE=2# self.r_weight([[0,2],[1,70],[2,28]])
		self.ISLAND_MIN={"x":0,"y":0};
		self.ISLAND_MAX={"x":0,"y":0};
		self.ISLAND_POINTS=1000
		self.ISLAND_SIDE_POINTS=100
		self.DELETED_PATH_POINTS=self.r(1,3)
		if (self.r(0,25)==0):self.DELETED_PATH_POINTS=0
		self.BRIDGES={"up":-1,"down":-1,"left":-1,"right":-1}
		self.BRIDGE_OFFSET=self.r(18,22)
		self.PATH_WIDTH=600
		self.PATH_POINT_W=100
		self.PATH_POINTS_R=15
		self.FOREST_TYPE=["0" for i in range(0,16)]
		self.FOREST_NUM_MIN=4
		self.FOREST_NUM_MAX=8
		for i in range(0,self.r(self.FOREST_NUM_MIN,self.FOREST_NUM_MAX)):self.FOREST_TYPE[i]="1"
		Shuffle(self.FOREST_TYPE)
		self.FOREST_TYPE="".join(self.FOREST_TYPE)
		self.MIN_TREES_PER_SQUARE=50
		self.MAX_TREES_PER_SQUARE=80
		self.MIN_SMALL_TREES_PER_SQUARE=10
		self.MAX_SMALL_TREES_PER_SQUARE=15
		self.MIN_FOREST_RADIUS=self.BOARD_WIDTH/8
		self.MAX_FOREST_RADIUS=self.BOARD_WIDTH/5
		self.MIN_RANDOM_TREES=20
		self.MAX_RANDOM_TREES=60
		self.TREE_POINTS=35
		self.MIN_LOOT_CHESTS=5
		self.MAX_LOOT_CHESTS=12
		self.LOOT_CHEST_TREE_CLEAR_RADIUS=200
	def map(self,v,aa,ab,ba,bb):
		return (v-aa)/(ab-aa)*(bb-ba)+ba
	def lerp(self,a,b,c,d=False):
		return a*(1-c)+b*c if d==False else int(a*(1-c)+b*c)
	def noise(self,x,y,z=0):
		p=[151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,74,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]
		for i in range(0,256):
			p.append(p[i])
		def fade(t):
			return t*t*t*(t*(t*6-15)+10)
		def lerp(t,a,b):
			return a+t*(b-a)
		def grad(hash,x,y,z):
			h=hash&15
			u=x if h<8 else y
			v=y if h<4 else (x if h==12 or h==14 else z)
			return (u if (h&1)==0 else -u)+(v if (h&2)==0 else -v)
		x+=NOISE_OFFSET[0]
		y+=NOISE_OFFSET[1]
		z+=NOISE_OFFSET[2]
		floorX=int(x)
		floorY=int(y)
		floorZ=int(z)
		X=floorX&255
		Y=floorY&255
		Z=floorZ&255
		x-=floorX
		y-=floorY
		z-=floorZ
		xMinus1=x-1
		yMinus1=y-1
		zMinus1=z-1
		u=fade(x)
		v=fade(y)
		w=fade(z)
		A=p[X]+Y
		AA=p[A]+Z
		AB=p[A+1]+Z
		B=p[X+1]+Y
		BA=p[B]+Z
		BB=p[B+1]+Z
		return -lerp(w,lerp(v,lerp(u,grad(p[AA],x,y,z),grad(p[BA],xMinus1,y,z)),lerp(u,grad(p[AB],x,yMinus1,z),grad(p[BB],xMinus1,yMinus1,z))),lerp(v,lerp(u,grad(p[AA+1],x,y,zMinus1),grad(p[BA+1],xMinus1,y,z-1)),lerp(u,grad(p[AB+1],x,yMinus1,zMinus1),grad(p[BB+1],xMinus1,yMinus1,zMinus1))))
	def r(self,a,b,c=False):
		return int(Random()*(b-a)+a) if c==False else Random()*(b-a)+a
	def r_weight(self,dt):
		a=[]
		for d in dt:
			for i in range(0,d[1]):
				a.append(d[0])
		return a[self.r(0,len(a)-1)]
	def dark(self,c):
		c=[int(c[1:3],16),int(c[3:5],16),int(c[5:7],16)]
		return "#%0.2X%0.2X%0.2X"%(max(0,c[0]-20),max(0,c[1]-20),max(0,c[2]-20))
	def gen(self):
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating board...")
		self.board["w"]=self.BOARD_WIDTH
		self.board["h"]=self.BOARD_HEIGHT
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating island...")
		self.board["island"]=self.gen_island()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating ground...")
		self.board["ground_path"]=self.gen_ground_path()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating bridges...")
		self.board["bridges"]=self.gen_bridges()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating paths...")
		self.board["paths"]=self.gen_paths()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating trees...")
		self.board["trees"]=self.gen_trees()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating loot chests...")
		self.board["loot_chests"]=self.gen_loot_chests()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&YELLOW,BRIGHT&&Generating vector graphics...")
		self.board["graphics"]=self.gen_vector_graphics()
		self.GAME.log(f"&&BLUE,BRIGHT&&{self.CLASS_NAME}:\t&&RED,NORMAL&&World generated!")
		self.DONE=True
	def gen_ground_path(self):
		def map(v,aa,ab,ba,bb):
			return (v-aa)/(ab-aa)*(bb-ba)+ba
		def d(x,y):
			return Sqrt((x-self.BOARD_WIDTH/2)**2+(y-self.BOARD_HEIGHT/2)**2)
		gp=[]
		if (self.ISLAND_TYPE==1):
			return [{"x":0,"y":0},{"x":self.BOARD_WIDTH,"y":0},{"x":self.BOARD_WIDTH,"y":self.BOARD_HEIGHT},{"x":0,"y":self.BOARD_HEIGHT}]
		sq=[]
		OFFSET=self.GROUND_START_RECT_OFFSET
		i=OFFSET
		while (i<self.BOARD_WIDTH-OFFSET):
			sq.append(d(i,OFFSET))
			i+=(self.BOARD_WIDTH-OFFSET*2)/self.GROUND_POINTS_PER_SIDE
		ca=PI*1.25
		csa=PI*2/(self.GROUND_POINTS_PER_SIDE*4)
		cr=10
		i=0
		while (i<self.GROUND_POINTS_PER_SIDE*4):
			nx=20+cr*Cos(ca)
			ny=20+cr*Sin(ca)
			n=map(self.noise(nx,ny),-1,1,-OFFSET*0.8,OFFSET*0.8)+sq[i%self.GROUND_POINTS_PER_SIDE]-OFFSET
			gp.append({"x":self.BOARD_WIDTH/2+n*Cos(ca),"y":self.BOARD_HEIGHT/2+n*Sin(ca)})
			ca+=csa
			i+=1
		return gp
	def gen_island_paths(self,W,H):
		path=[]
		w_path=[]
		a=0
		STEP=1
		sa=False
		sb=False
		while (a<PI*2):
			rx=self.noise(Cos(a)*STEP+10,Sin(a)*STEP+10)*1750+W/2
			ry=self.noise(Cos(a)*STEP+20,Sin(a)*STEP+20)*1750+H/2
			path.append({"x":round(rx*Cos(a)+W/2+self.ISLAND_MIN["x"]),"y":round(ry*Sin(a)+H/2+self.ISLAND_MIN["y"])})
			if (self.ISLAND_TYPE==1):
				if (sa==False and len(w_path)>1 and w_path[len(w_path)-1]["x"]-10<=0):
					sa=True
					w_path.append({"x":0,"y":w_path[len(w_path)-1]["y"]})
					w_path.append({"x":0,"y":0})
				elif (sa==True and sb==False and a>=PI*1.5 and round(ry*Sin(a)+H/2+self.ISLAND_MIN["y"])-10>0):
					sb=True
					rx+=1300
					ry+=1300
					w_path.append({"x":round(rx*Cos(a+PI*2/self.ISLAND_POINTS)+W/2+self.ISLAND_MIN["x"]),"y":0})
				elif (sa==False or (sa==True and sb==True)):
					rx+=1300
					ry+=1300
					w_path.append({"x":round(rx*Cos(a)+W/2+self.ISLAND_MIN["x"]),"y":round(ry*Sin(a)+H/2+self.ISLAND_MIN["y"])})
			if (self.ISLAND_TYPE==2):
				rx+=1300
				ry+=1300
				w_path.append({"x":round(rx*Cos(a)+W/2+self.ISLAND_MIN["x"]),"y":round(ry*Sin(a)+H/2+self.ISLAND_MIN["y"])})
			a+=PI*2/self.ISLAND_POINTS
		return path,w_path
	def gen_island(self):
		if (self.ISLAND_TYPE==0):
			return -1;
		W=self.r(self.BOARD_WIDTH*0.3,self.BOARD_WIDTH*0.4)
		H=self.r(self.BOARD_HEIGHT*0.3,self.BOARD_HEIGHT*0.4)
		if (self.ISLAND_TYPE==1):
			self.ISLAND_MIN["x"]=self.r(0,self.BOARD_WIDTH*0.01)+self.BOARD_WIDTH*0.02
			self.ISLAND_MIN["y"]=self.r(0,self.BOARD_HEIGHT*0.01)+self.BOARD_HEIGHT*0.02
			self.ISLAND_MAX["x"]=self.ISLAND_MIN["x"]+W
			self.ISLAND_MAX["y"]=self.ISLAND_MIN["y"]+H
		if (self.ISLAND_TYPE==2):
			self.ISLAND_MIN["x"]=self.BOARD_WIDTH*0.5-W/2
			self.ISLAND_MIN["y"]=self.BOARD_HEIGHT*0.5-H/2
			self.ISLAND_MAX["x"]=self.BOARD_WIDTH*0.5+W/2
			self.ISLAND_MAX["y"]=self.BOARD_HEIGHT*0.5+H/2
		self.ISLAND_MIN["x"]=round(self.ISLAND_MIN["x"])
		self.ISLAND_MIN["y"]=round(self.ISLAND_MIN["y"])
		self.ISLAND_MAX["x"]=round(self.ISLAND_MAX["x"])
		self.ISLAND_MAX["y"]=round(self.ISLAND_MAX["y"])
		paths=self.gen_island_paths(W,H)
		return {
			"type": self.ISLAND_TYPE,
			"start": self.ISLAND_MIN,
			"end": self.ISLAND_MAX,
			"w_path": paths[1],
			"path": paths[0]
		}
	def gen_bridges(self):
		if (self.ISLAND_TYPE==0):
			return -1
		br=[]
		si=0
		ni=si+self.BRIDGE_OFFSET
		a={"x":self.board["island"]["path"][si]["x"]-200,"y":self.board["island"]["path"][si]["y"]}
		b={"x":self.board["island"]["path"][si]["x"]+1600,"y":self.board["island"]["path"][si]["y"]}
		c={"x":self.board["island"]["path"][ni]["x"]+1600,"y":self.board["island"]["path"][ni]["y"]}
		d={"x":self.board["island"]["path"][ni]["x"]-200,"y":self.board["island"]["path"][ni]["y"]}
		l=[]
		l.append({"x":self.lerp(a["x"],d["x"],0.15,True),"y":a["y"]})
		l.append({"x":self.lerp(b["x"],c["x"],0.15,True),"y":b["y"]})
		l.append({"x":self.lerp(c["x"],b["x"],0.15,True),"y":c["y"]})
		l.append({"x":self.lerp(d["x"],a["x"],0.15,True),"y":d["y"]})
		br.append(l)
		self.BRIDGES["right"]=l
		si=int(self.ISLAND_POINTS/4)
		ni=si+self.BRIDGE_OFFSET
		a={"x":self.board["island"]["path"][si]["x"],"y":self.board["island"]["path"][si]["y"]-200}
		b={"x":self.board["island"]["path"][si]["x"],"y":self.board["island"]["path"][si]["y"]+1600}
		c={"x":self.board["island"]["path"][ni]["x"],"y":self.board["island"]["path"][ni]["y"]+1600}
		d={"x":self.board["island"]["path"][ni]["x"],"y":self.board["island"]["path"][ni]["y"]-200}
		l=[]
		l.append({"x":a["x"],"y":self.lerp(a["y"],d["y"],0.15,True)})
		l.append({"x":b["x"],"y":self.lerp(b["y"],c["y"],0.15,True)})
		l.append({"x":c["x"],"y":self.lerp(c["y"],b["y"],0.15,True)})
		l.append({"x":d["x"],"y":self.lerp(d["y"],a["y"],0.15,True)})
		br.append(l)
		self.BRIDGES["down"]=l
		if (self.ISLAND_TYPE==2):
			si=int(self.ISLAND_POINTS/2)
			ni=si+self.BRIDGE_OFFSET
			a={"x":self.board["island"]["path"][si]["x"]+200,"y":self.board["island"]["path"][si]["y"]}
			b={"x":self.board["island"]["path"][si]["x"]-1600,"y":self.board["island"]["path"][si]["y"]}
			c={"x":self.board["island"]["path"][ni]["x"]-1600,"y":self.board["island"]["path"][ni]["y"]}
			d={"x":self.board["island"]["path"][ni]["x"]+200,"y":self.board["island"]["path"][ni]["y"]}
			l=[]
			l.append({"x":self.lerp(a["x"],d["x"],0.15,True),"y":a["y"]})
			l.append({"x":self.lerp(b["x"],c["x"],0.15,True),"y":b["y"]})
			l.append({"x":self.lerp(c["x"],b["x"],0.15,True),"y":c["y"]})
			l.append({"x":self.lerp(d["x"],a["x"],0.15,True),"y":d["y"]})
			br.append(l)
			self.BRIDGES["left"]=l
			si=int(self.ISLAND_POINTS*3/4)
			ni=si+self.BRIDGE_OFFSET
			a={"x":self.board["island"]["path"][si]["x"],"y":self.board["island"]["path"][si]["y"]+200}
			b={"x":self.board["island"]["path"][si]["x"],"y":self.board["island"]["path"][si]["y"]-1600}
			c={"x":self.board["island"]["path"][ni]["x"],"y":self.board["island"]["path"][ni]["y"]-1600}
			d={"x":self.board["island"]["path"][ni]["x"],"y":self.board["island"]["path"][ni]["y"]+200}
			l=[]
			l.append({"x":a["x"],"y":self.lerp(a["y"],d["y"],0.15,True)})
			l.append({"x":b["x"],"y":self.lerp(b["y"],c["y"],0.15,True)})
			l.append({"x":c["x"],"y":self.lerp(c["y"],b["y"],0.15,True)})
			l.append({"x":d["x"],"y":self.lerp(d["y"],a["y"],0.15,True)})
			br.append(l)
			self.BRIDGES["up"]=l
		return br
	def sc(self,i,j):
		dct={0:[1/12,3/12],1:[5/12,7/12],2:[9/12,11/12]}
		def p(v,mn,mx):
			return self.r(v*mn,v*mx)
		return {"x":p(self.BOARD_WIDTH,*dct[i]),"y":p(self.BOARD_HEIGHT,*dct[j])}
	def rand_ln(self,ps,rls):
		p=[]
		l=len(ps)-1
		for i in range(0,len(ps)):
			d=Sqrt((ps[i]["x"]-ps[l]["x"])**2+(ps[i]["y"]-ps[l]["y"])**2)
			pts=int(d/self.PATH_POINT_W)
			p.append({"x":ps[l]["x"],"y":ps[l]["y"]})
			if (i in rls):
				for j in range(1,pts):
					pt={"x":self.lerp(ps[l]["x"],ps[i]["x"],j/(pts+1),True),"y":self.lerp(ps[l]["y"],ps[i]["y"],j/(pts+1),True)}
					pt["x"]+=self.r(self.PATH_POINTS_R,-self.PATH_POINTS_R)
					pt["y"]+=self.r(self.PATH_POINTS_R,-self.PATH_POINTS_R)
					p.append(pt)
			l=(l+1)%len(ps)
		return p
	def ang(self,x1,y1,x2,y2):
		return -Atan2(x2-x1,y2-y1)
	def rot_point(self,px,py,x,y,a):
		return {"x":int((px-x)*Cos(a)-(py-y)*Sin(a)+x),"y":int((px-x)*Sin(a)+(py-y)*Cos(a)+y)}
	def connect(self,a,b):
		p=[]
		p.append(self.rot_point(a["x"]+int(self.PATH_WIDTH/2),a["y"],a["x"],a["y"],self.ang(a["x"],a["y"],b["x"],b["y"])))
		p.append(self.rot_point(a["x"]-int(self.PATH_WIDTH/2),a["y"],a["x"],a["y"],self.ang(a["x"],a["y"],b["x"],b["y"])))
		p.append(self.rot_point(b["x"]-int(self.PATH_WIDTH/2),b["y"],b["x"],b["y"],self.ang(a["x"],a["y"],b["x"],b["y"])))
		p.append(self.rot_point(b["x"]+int(self.PATH_WIDTH/2),b["y"],b["x"],b["y"],self.ang(a["x"],a["y"],b["x"],b["y"])))
		return self.rand_ln(p,[0,2]),[p[0],p[1]],[p[2],p[3]]
	def gen_paths(self):
		ps=[]
		pts=[]
		for i in range(0,3):
			for j in range(0,3):
				pts.append([self.sc(i,j),{"up":-1,"down":-1,"left":-1,"right":-1},True,False])
		if (self.ISLAND_TYPE==1):
			pts[0][0]["x"]=self.r(self.BOARD_WIDTH*1/8,self.BOARD_WIDTH*5/24)
			pts[0][0]["y"]=self.r(self.BOARD_HEIGHT*1/8,self.BOARD_HEIGHT*5/24)
			pts[0][3]=True
			br=self.BRIDGES["right"]
			px=(br[0]["x"]+br[3]["x"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			p=[]
			p.append({"x":br[3]["x"],"y":br[3]["y"]})
			p.append(self.rot_point(pts[0][0]["x"]-int(self.PATH_WIDTH/2),pts[0][0]["y"],pts[0][0]["x"],pts[0][0]["y"],self.ang(pts[0][0]["x"],pts[0][0]["y"],px,ay)))
			p.append(self.rot_point(pts[0][0]["x"]+int(self.PATH_WIDTH/2),pts[0][0]["y"],pts[0][0]["x"],pts[0][0]["y"],self.ang(pts[0][0]["x"],pts[0][0]["y"],px,ay)))
			p.append({"x":br[0]["x"],"y":br[0]["y"]})
			pts[0][1]["right"]=[p[1],p[2]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["down"]
			py=(br[0]["y"]+br[3]["y"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			p=[]
			p.append({"x":br[3]["x"],"y":br[3]["y"]})
			p.append(self.rot_point(pts[0][0]["x"]-int(self.PATH_WIDTH/2),pts[0][0]["y"],pts[0][0]["x"],pts[0][0]["y"],self.ang(pts[0][0]["x"],pts[0][0]["y"],ax,py)))
			p.append(self.rot_point(pts[0][0]["x"]+int(self.PATH_WIDTH/2),pts[0][0]["y"],pts[0][0]["x"],pts[0][0]["y"],self.ang(pts[0][0]["x"],pts[0][0]["y"],ax,py)))
			p.append({"x":br[0]["x"],"y":br[0]["y"]})
			pts[0][1]["down"]=[p[1],p[2]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["right"]
			px=(br[1]["x"]+br[2]["x"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			pts[3][0]["x"]=int(ax+self.BOARD_WIDTH*1/12+self.r(-500,500))
			pts[3][0]["y"]=int(ay+self.r(-500,500))
			pts[3][2]=False
			p=[]
			p.append({"x":br[1]["x"],"y":br[1]["y"]})
			p.append(self.rot_point(pts[3][0]["x"]-int(self.PATH_WIDTH/2),pts[3][0]["y"],pts[3][0]["x"],pts[3][0]["y"],self.ang(pts[3][0]["x"],pts[3][0]["y"],px,ay)))
			p.append(self.rot_point(pts[3][0]["x"]+int(self.PATH_WIDTH/2),pts[3][0]["y"],pts[3][0]["x"],pts[3][0]["y"],self.ang(pts[3][0]["x"],pts[3][0]["y"],px,ay)))
			p.append({"x":br[2]["x"],"y":br[2]["y"]})
			pts[3][1]["left"]=[p[2],p[1]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["down"]
			py=(br[1]["y"]+br[2]["y"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			pts[1][0]["x"]=int(ax+self.r(-500,500))
			pts[1][0]["y"]=int(ay+self.BOARD_HEIGHT*1/12+self.r(-500,500))
			pts[1][2]=False
			p=[]
			p.append({"x":br[1]["x"],"y":br[1]["y"]})
			p.append(self.rot_point(pts[1][0]["x"]-int(self.PATH_WIDTH/2),pts[1][0]["y"],pts[1][0]["x"],pts[1][0]["y"],self.ang(pts[1][0]["x"],pts[1][0]["y"],ax,py)))
			p.append(self.rot_point(pts[1][0]["x"]+int(self.PATH_WIDTH/2),pts[1][0]["y"],pts[1][0]["x"],pts[1][0]["y"],self.ang(pts[1][0]["x"],pts[1][0]["y"],ax,py)))
			p.append({"x":br[2]["x"],"y":br[2]["y"]})
			pts[1][1]["up"]=[p[2],p[1]]
			ps.append(self.rand_ln(p,[1,3]))
		if (self.ISLAND_TYPE==2):
			pts[4][0]["x"]=self.r(self.BOARD_WIDTH*11/24,self.BOARD_WIDTH*13/24)
			pts[4][0]["y"]=self.r(self.BOARD_HEIGHT*11/24,self.BOARD_HEIGHT*13/24)
			pts[4][3]=True
			br=self.BRIDGES["right"]
			px=(br[0]["x"]+br[3]["x"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			p=[]
			p.append({"x":br[3]["x"],"y":br[3]["y"]})
			p.append(self.rot_point(pts[4][0]["x"]-int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],px,ay)))
			p.append(self.rot_point(pts[4][0]["x"]+int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],px,ay)))
			p.append({"x":br[0]["x"],"y":br[0]["y"]})
			pts[4][1]["right"]=[p[1],p[2]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["down"]
			py=(br[0]["y"]+br[3]["y"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			p=[]
			p.append({"x":br[3]["x"],"y":br[3]["y"]})
			p.append(self.rot_point(pts[4][0]["x"]-int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],ax,py)))
			p.append(self.rot_point(pts[4][0]["x"]+int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],ax,py)))
			p.append({"x":br[0]["x"],"y":br[0]["y"]})
			pts[4][1]["down"]=[p[1],p[2]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["left"]
			px=(br[0]["x"]+br[3]["x"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			p=[]
			p.append({"x":br[3]["x"],"y":br[3]["y"]})
			p.append(self.rot_point(pts[4][0]["x"]-int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],px,ay)))
			p.append(self.rot_point(pts[4][0]["x"]+int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],px,ay)))
			p.append({"x":br[0]["x"],"y":br[0]["y"]})
			pts[4][1]["left"]=[p[1],p[2]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["up"]
			py=(br[0]["y"]+br[3]["y"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			p=[]
			p.append({"x":br[3]["x"],"y":br[3]["y"]})
			p.append(self.rot_point(pts[4][0]["x"]-int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],ax,py)))
			p.append(self.rot_point(pts[4][0]["x"]+int(self.PATH_WIDTH/2),pts[4][0]["y"],pts[4][0]["x"],pts[4][0]["y"],self.ang(pts[4][0]["x"],pts[4][0]["y"],ax,py)))
			p.append({"x":br[0]["x"],"y":br[0]["y"]})
			pts[4][1]["up"]=[p[1],p[2]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["right"]
			px=(br[1]["x"]+br[2]["x"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			pts[7][0]["x"]=int(ax+self.BOARD_WIDTH*1/12+self.r(-500,500))
			pts[7][0]["y"]=int(ay+self.r(-500,500))
			pts[7][2]=False
			p=[]
			p.append({"x":br[1]["x"],"y":br[1]["y"]})
			p.append(self.rot_point(pts[7][0]["x"]-int(self.PATH_WIDTH/2),pts[7][0]["y"],pts[7][0]["x"],pts[7][0]["y"],self.ang(pts[7][0]["x"],pts[7][0]["y"],px,ay)))
			p.append(self.rot_point(pts[7][0]["x"]+int(self.PATH_WIDTH/2),pts[7][0]["y"],pts[7][0]["x"],pts[7][0]["y"],self.ang(pts[7][0]["x"],pts[7][0]["y"],px,ay)))
			p.append({"x":br[2]["x"],"y":br[2]["y"]})
			pts[7][1]["left"]=[p[2],p[1]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["down"]
			py=(br[1]["y"]+br[2]["y"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			pts[5][0]["x"]=int(ax+self.r(-500,500))
			pts[5][0]["y"]=int(ay+self.BOARD_HEIGHT*1/12+self.r(-500,500))
			pts[5][2]=False
			p=[]
			p.append({"x":br[1]["x"],"y":br[1]["y"]})
			p.append(self.rot_point(pts[5][0]["x"]-int(self.PATH_WIDTH/2),pts[5][0]["y"],pts[5][0]["x"],pts[5][0]["y"],self.ang(pts[5][0]["x"],pts[5][0]["y"],ax,py)))
			p.append(self.rot_point(pts[5][0]["x"]+int(self.PATH_WIDTH/2),pts[5][0]["y"],pts[5][0]["x"],pts[5][0]["y"],self.ang(pts[5][0]["x"],pts[5][0]["y"],ax,py)))
			p.append({"x":br[2]["x"],"y":br[2]["y"]})
			pts[5][1]["up"]=[p[2],p[1]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["left"]
			px=(br[1]["x"]+br[2]["x"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			pts[1][0]["x"]=int(ax-self.BOARD_WIDTH*1/12+self.r(-500,500))
			pts[1][0]["y"]=int(ay+self.r(-500,500))
			pts[1][2]=False
			p=[]
			p.append({"x":br[1]["x"],"y":br[1]["y"]})
			p.append(self.rot_point(pts[1][0]["x"]-int(self.PATH_WIDTH/2),pts[1][0]["y"],pts[1][0]["x"],pts[1][0]["y"],self.ang(pts[1][0]["x"],pts[1][0]["y"],px,ay)))
			p.append(self.rot_point(pts[1][0]["x"]+int(self.PATH_WIDTH/2),pts[1][0]["y"],pts[1][0]["x"],pts[1][0]["y"],self.ang(pts[1][0]["x"],pts[1][0]["y"],px,ay)))
			p.append({"x":br[2]["x"],"y":br[2]["y"]})
			pts[1][1]["right"]=[p[2],p[1]]
			ps.append(self.rand_ln(p,[1,3]))
			br=self.BRIDGES["up"]
			py=(br[1]["y"]+br[2]["y"])/2
			ax=(br[0]["x"]+br[1]["x"]+br[2]["x"]+br[3]["x"])/4
			ay=(br[0]["y"]+br[1]["y"]+br[2]["y"]+br[3]["y"])/4
			pts[3][0]["x"]=int(ax+self.r(-500,500))
			pts[3][0]["y"]=int(ay-self.BOARD_HEIGHT*1/12+self.r(-500,500))
			pts[3][2]=False
			p=[]
			p.append({"x":br[1]["x"],"y":br[1]["y"]})
			p.append(self.rot_point(pts[3][0]["x"]-int(self.PATH_WIDTH/2),pts[3][0]["y"],pts[3][0]["x"],pts[3][0]["y"],self.ang(pts[3][0]["x"],pts[3][0]["y"],ax,py)))
			p.append(self.rot_point(pts[3][0]["x"]+int(self.PATH_WIDTH/2),pts[3][0]["y"],pts[3][0]["x"],pts[3][0]["y"],self.ang(pts[3][0]["x"],pts[3][0]["y"],ax,py)))
			p.append({"x":br[2]["x"],"y":br[2]["y"]})
			pts[3][1]["down"]=[p[2],p[1]]
			ps.append(self.rand_ln(p,[1,3]))
		if (self.DELETED_PATH_POINTS>0):
			for k in range(0,self.DELETED_PATH_POINTS-(1 if self.ISLAND_TYPE>0 else 0)):
				while (True):
					idx=self.r(0,8)
					if (pts[idx]!=-1 and pts[idx][2]==True and pts[idx][3]==False):
						pts[idx]=-1
						break
		for i in range(0,3):
			for j in range(0,3):
				if (pts[i+j*3]==-1 or pts[i+j*3][3]==True):continue
				if (i<2 and pts[i+1+j*3]!=-1 and pts[i+1+j*3][3]==False):
					cp,tdA,tdB=self.connect(pts[i+j*3][0],pts[i+1+j*3][0])
					pts[i+j*3][1]["right"]=tdA
					pts[i+1+j*3][1]["left"]=tdB
					ps.append(cp)
				if (j<2 and pts[i+j*3+3]!=-1 and pts[i+j*3+3][3]==False):
					cp,tdA,tdB=self.connect(pts[i+j*3][0],pts[i+j*3+3][0])
					pts[i+j*3][1]["down"]=tdA
					pts[i+j*3+3][1]["up"]=tdB
					ps.append(cp)
		for i in range(0,3):
			for j in range(0,3):
				if (pts[i+j*3]==-1):continue
				st=-1
				last=-1
				done=[]
				for d in "up right down left up right down left".split(" "):
					if (last!=-1 and pts[i+j*3][1][d]!=-1):
						l=pts[i+j*3][1][last]
						c=pts[i+j*3][1][d]
						p=[]
						p.append(l[0])
						p.append(c[1])
						p.append({"x":pts[i+j*3][0]["x"],"y":pts[i+j*3][0]["y"]})
						ps.append(self.rand_ln(p,[1]))
					if (pts[i+j*3][1][d]!=-1):
						if (d in done):
							break
						done.append(d)
						last=d
		return ps
	def pointPoly(self,px,py,p):
		c=False
		for i in range(0,len(p)):
			if (((p[i][1]>py and p[(i+1)%len(p)][1]<py) or (p[i][1]<py and p[(i+1)%len(p)][1]>py)) and (px<(p[(i+1)%len(p)][0]-p[i][0])*(py-p[i][1])/(p[(i+1)%len(p)][1]-p[i][1])+p[i][0])):
				c=not c
		return c
	def pointCircle(self,px,py,cx,cy,cr):
		return (Sqrt((px-cx)*(px-cx)+(py-cy)*(py-cy))<=cr)
	def path_to_arr(self,p):
		return [[v["x"],v["y"]] for v in p]
	def trees(self,px,py,f,rd=False):
		ts=[]
		tn=self.r(self.MIN_TREES_PER_SQUARE,self.MAX_TREES_PER_SQUARE)
		if (rd==False):
			fr=self.r(self.MIN_FOREST_RADIUS,self.MAX_FOREST_RADIUS)
			if (f==True):
				tn=self.r(self.MIN_SMALL_TREES_PER_SQUARE,self.MAX_SMALL_TREES_PER_SQUARE)
		else:
			tn=self.r(self.MIN_RANDOM_TREES,self.MAX_RANDOM_TREES)
		ctn=0
		while (ctn<tn):
			cx=self.r(0,self.BOARD_WIDTH)
			cy=self.r(0,self.BOARD_HEIGHT)
			if ((rd==False and self.pointCircle(cx,cy,px+self.BOARD_WIDTH/8,py+self.BOARD_HEIGHT/8,fr)==True) or rd==True):
				if (self.pointPoly(cx,cy,self.path_to_arr(self.board["ground_path"]))==True and ((self.board["island"]!=-1 and self.pointPoly(cx,cy,self.path_to_arr(self.board["island"]["w_path"]))==False and self.pointPoly(cx,cy,self.path_to_arr(self.board["island"]["path"]))==False) or self.board["island"]==-1)):
					s=True
					for ps in self.board["paths"]:
						if (self.pointPoly(cx,cy,self.path_to_arr(ps))==True):
							s=False
							break
					if (s==True):
						if (self.board["bridges"]!=-1):
							for br in self.board["bridges"]:
								if (self.pointPoly(cx,cy,self.path_to_arr(br))==True):
									s=False
									break
						if (s==True):
							r=self.r(150,300)
							p=[]
							a=0
							while True:
								if (a>=PI*2):break
								p.append({"x":int(cx+r*Cos(a)),"y":int(cy+r*Sin(a))})
								a+=PI*2/self.TREE_POINTS
							c=self.r(0,100)
							ct=[cx,cy,r,c,p]
							ts.append(ct)
							ctn+=1
		return ts
	def gen_trees(self):
		ts=[]
		bs=[]
		ns=[]
		if (self.ISLAND_TYPE==1):
			ns=[0]
			bs=[1,4,5]
		if (self.ISLAND_TYPE==2):
			bs=[5,6,9,10]
		for i in range(0,4):
			for j in range(0,4):
				if (i+j*4 in ns or self.FOREST_TYPE[i+j*4]=="0"):continue
				ts.extend(self.trees(i*self.BOARD_WIDTH/4,j*self.BOARD_HEIGHT/4,i+j*4 in bs))
		ts.extend(self.trees(0,0,False,True))
		return ts
	def check_empty(self,x,y,r):
		if (self.pointPoly(x,y,self.path_to_arr(self.board["ground_path"]))==False):
			return False
		if (self.board["island"]!=-1 and self.pointPoly(x,y,self.path_to_arr(self.board["island"]["w_path"]))==True and self.pointPoly(x,y,self.path_to_arr(self.board["island"]["path"]))==False):
			return False
		for p in self.board["paths"]:
			if (self.pointPoly(x,y,self.path_to_arr(p))==True):
				return False
		for b in self.board["bridges"]:
			if (self.pointPoly(x,y,self.path_to_arr(b))==True):
				return False
		for t in self.board["trees"]:
			if (Sqrt((t[0]-x)**2+(t[1]-y)**2)<t[2]+r):
				return False
		return True
	def gen_loot_chests(self):
		lc=[]
		lcn=self.r(self.MIN_LOOT_CHESTS,self.MAX_LOOT_CHESTS)
		cn=0
		while (cn<lcn):
			x=self.r(0,self.BOARD_WIDTH)
			y=self.r(0,self.BOARD_HEIGHT)
			if (self.check_empty(x,y,self.LOOT_CHEST_TREE_CLEAR_RADIUS)==True):
				lc.append({"x":x,"y":y})
				LootChest(self.GAME,x,y,cn)
				cn+=1
		return lc
	def gen_vector_graphics(self):
		gs=[]
		def heart(f=False):
			l=[]
			S=0.9
			s=0
			t=30
			a=0
			while (a<PI*2):
				if (f==True and s==int(t/2)):
					a=0
				x=-S*16*pow(Sin(a),3)
				y=S*-13*Cos(a)+S*5*Cos(2*a)+S*2*Cos(3*a)+S*Cos(4*a)
				l.append({"x":x,"y":y})
				if (f==True and s==int(t/2)):
					return l
				s+=1
				a+=PI*2/t
			return l
		gs.append(heart())
		gs.append(heart(True))
		gs.append(heart())
		W=10
		H=5
		P=10
		p=[]
		p.append({"x":-W,"y":-H})
		p.append({"x":W,"y":-H})
		a=0
		while (a<PI):
			p.append({"x":W+H*Cos(a-PI/2),"y":H*Sin(a-PI/2)})
			a+=PI/P
		p.append({"x":W,"y":H})
		p.append({"x":-W,"y":H})
		gs.append(p)
		S=8
		cp=[]
		cp.append({"x":-S/4,"y":-S})
		cp.append({"x":S/4,"y":-S})
		cp.append({"x":S/4,"y":-S/4})
		cp.append({"x":S,"y":-S/4})
		cp.append({"x":S,"y":S/4})
		cp.append({"x":S/4,"y":S/4})
		cp.append({"x":S/4,"y":S})
		cp.append({"x":-S/4,"y":S})
		cp.append({"x":-S/4,"y":S/4})
		cp.append({"x":-S,"y":S/4})
		cp.append({"x":-S,"y":-S/4})
		cp.append({"x":-S/4,"y":-S/4})
		gs.append(cp)
		p=[]
		S=85
		a=0
		while (a<PI/2.2):
			b=PI/2.2-a
			p.append({"x":-S*Cos(b),"y":-S*4-S*1.6*Sin(b)})
			a+=PI/2.2/10
		p.append({"x":-S,"y":-S*1.5})
		p.append({"x":-S*4.6,"y":S*0.3})
		p.append({"x":-S*4.6,"y":S*1.3})
		p.append({"x":-S,"y":S*0.7})
		p.append({"x":-S*0.8,"y":S*3.4})
		p.append({"x":-S*2.6,"y":S*4.5})
		p.append({"x":-S*2.6,"y":S*5})
		p.append({"x":0,"y":S*4.4})
		pc=[]
		for v in p:
			pc.append({"x":v["x"],"y":v["y"]})
		for pi in range(len(p)-1,-1,-1):
			pc.append({"x":-p[pi]["x"],"y":p[pi]["y"]})
		gs.append(pc)
		PTS=20
		S=14
		p=[]
		a=0
		while (a<PI*2):
			p.append({"x":S*Cos(a),"y":S*Sin(a)})
			a+=PI*2/PTS
		gs.append(p)
		return gs
	def encode(self):
		def encode_ground_path(gp):
			s=""
			for p in gp:
				s+=str(p["x"])+","+str(p["y"])+":"
			return s[:len(s)-1]
		def encode_island(i):
			if (i==-1):
				return str(i)
			s=""
			s+=str(i["type"])+":"
			s+=str(i["start"]["x"])+","+str(i["start"]["y"])+":"
			s+=str(i["end"]["x"])+","+str(i["end"]["y"])+":"
			for p in i["w_path"]:
				s+=str(p["x"])+"."+str(p["y"])+","
			s=s[:len(s)-1]+":"
			for p in i["path"]:
				s+=str(p["x"])+"."+str(p["y"])+","
			return s[:len(s)-1]
		def encode_bridges(br):
			if (br==-1):
				return str(br)
			s=""
			for b in br:
				for p in b:
					s+=str(p["x"])+"."+str(p["y"])+","
				s=s[:len(s)-1]+":"
			return s[:len(s)-1]
		def encode_paths(ps):
			s=""
			for p in ps:
				for v in p:
					s+=str(v["x"])+"."+str(v["y"])+","
				s=s[:len(s)-1]+":"
			return s[:len(s)-1]
		def encode_trees(ts):
			s=""
			for t in ts:
				s+=str(t[0])+","
				s+=str(t[1])+","
				s+=str(t[2])+","
				s+=str(t[3])+","
				for p in t[4]:
					s+=str(p["x"])+"/"+str(p["y"])+"."
				s=s[:len(s)-1]+":"
			return s[:len(s)-1]
		def encode_loot_cheses(lc):
			s=""
			for c in lc:
				s+=str(c["x"])+","+str(c["y"])+":"
			return s[:len(s)-1]
		def encode_vector_graphics(vg):
			s=""
			for g in vg:
				for p in g:
					s+=str(p["x"])+"/"+str(p["y"])+","
				s=s[:len(s)-1]+":"
			return s[:len(s)-1]
		s=""
		s+=str(self.board["w"])+":"+str(self.board["h"])+";"
		s+=encode_ground_path(self.board["ground_path"])+";"
		s+=encode_island(self.board["island"])+";"
		s+=encode_bridges(self.board["bridges"])+";"
		s+=encode_paths(self.board["paths"])+";"
		s+=encode_trees(self.board["trees"])+";"
		s+=encode_loot_cheses(self.board["loot_chests"])+";"
		s+=encode_vector_graphics(self.board["graphics"])
		return s
class SmallWorld(World):
	def __init__(self,GAME):
		World.__init__(self,GAME)
		self.BOARD_WIDTH=1000
		self.BOARD_HEIGHT=1000
		self.CLASS_NAME="SMALL-WORLD"
		self.ISLAND_TYPE=0
		self.GROUND_START_RECT_OFFSET=30
	def gen_island(self):
		return -1
	def gen_bridges(self):
		return -1
	def gen_paths(self):
		return []
	def gen_trees(self):
		return []
	def gen_loot_chests(self):
		return []



def load_bans():
	l={}
	with open("./server_data/bans.lst","r") as f:
		for ln in f:
			if (len(ln)<2 or int(ln.split(";")[1])<Time()):continue
			l[ln.split(";")[0]]=[int(ln.split(";")[1]),ln.split(";")[2].replace("\n","")]
	return l
def save_bans(l):
	s=""
	for k in l.keys():
		if (l[k][0]<Time()):continue
		s+=f"{k};{l[k][0]};{l[k][1]}\n"
	with open("./server_data/bans.lst","w") as f:
		f.write(s)
def load_players():
	l={}
	with open("./server_data/players.lst","r") as f:
		for ln in f:
			if (len(ln)<2):continue
			l[int(ln.split(";")[0])]={"id":int(ln.split(";")[0]),"name":ln.split(";")[1],"addr":ln.split(";")[2],"on":False,"admin":bool(int(ln.split(";")[4]))}
	return l
def save_players(l):
	s=""
	for i in l.keys():
		k=l[i]
		s+=f"{k['id']};{k['name']};{k['addr']};{'1' if k['on']==True else '0'};{'1' if k['admin']==True else '0'}\n"
	with open("./server_data/players.lst","w") as f:
		f.write(s)
def load_used_names():
	l=[]
	with open("./server_data/used_names.lst","r") as f:
		for ln in f:
			if (len(ln)<2):continue
			l.append(ln.replace("\n",""))
	return l
def save_used_names(l):
	s=""
	for n in l:
		s+=f"{n}\n"
	with open("./server_data/used_names.lst","w") as f:
		f.write(s)
def load_next_id():
	with open("./server_data/id.const","r") as f:
		return int(f.read().replace("\n",""))
def save_next_id(l):
	with open("./server_data/id.const","w") as f:
		f.write(str(l))



def get_address(a):
	# return str(a)[:len(str(a))-len(str(a).split(".")[len(str(a).split("."))-1])-1]
	return a



class GunItem:
	def __init__(self,GAME,x,y,type_="basic",g_type=0,ammo=1,wt=-1):
		self.GAME=GAME
		self.i_id=self.gen_i_id()
		self.x=x
		self.y=y
		self.dir=int(Random()*360)
		self.type=type_
		self.g_type=g_type
		self.ammo=ammo
		self.wait_time=wt if wt!=-1 else MIN_ITEM_PICKUP_DELAY
		self.s_time=Time()+self.wait_time
		self.GAME.ITEMS.append(self)
		if (len(self.GAME.PLAYERS)>0):self.GAME.PLAYERS[0].sendall(PACKETS["item"]%(self.i_id,self.x,self.y,self.dir,0,str(GUN_DATA[self.type]["id"])+","+str(self.g_type)))
		thr=Thread(target=self.can_pick,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def create_gun(self,i):
		return Gun(self.GAME,i,self.type,self.g_type,self.ammo)
	def can_pick(self):
		Sleep(self.wait_time)
		for p in self.GAME.PLAYERS:
			if (p.DEAD==True):continue
			if (self.pick_up(p)==True):
				return
	def pick_up(self,p):
		if (self.s_time<=Time() and p.INVENTORY.is_full()==False and Sqrt((p.POS_X-self.x)**2+(p.POS_Y-self.y)**2)<=MIN_PICKUP_DIST):
			p.INVENTORY.add(self.create_gun(p.INVENTORY))
			if (self in self.GAME.ITEMS):
				self.GAME.ITEMS.remove(self)
			p.sendall(PACKETS["rm_item"]%(self.i_id))
			return True
		return False
	def gen_i_id(self):
		mi=0
		while True:
			s=True
			for i in self.GAME.ITEMS:
				if (i.i_id==mi):
					mi+=1
					s=False
			if (s==True):
				return mi
class CoinItem:
	def __init__(self,GAME,x,y):
		self.GAME=GAME
		self.i_id=self.gen_i_id()
		self.x=x
		self.y=y
		self.GAME.ITEMS.append(self)
		if (len(self.GAME.PLAYERS)>0):self.GAME.PLAYERS[0].sendall(PACKETS["item"]%(self.i_id,self.x,self.y,0,1,""))
		self.can_pick()
	def can_pick(self):
		for p in self.GAME.PLAYERS:
			if (p.DEAD==True):continue
			if (self.pick_up(p)==True):
				return
	def pick_up(self,p):
		if (Sqrt((p.POS_X-self.x)**2+(p.POS_Y-self.y)**2)<=MIN_PICKUP_DIST):
			p.COINS+=1
			self.GAME.ITEMS.remove(self)
			p.sendall(PACKETS["rm_item"]%(self.i_id))
			p.send_(PACKETS["coins"]%(p.COINS))
			return True
	def gen_i_id(self):
		mi=0
		while True:
			s=True
			for i in self.GAME.ITEMS:
				if (i.i_id==mi):
					mi+=1
					s=False
			if (s==True):
				return mi



class CollisionBox:
	def __init__(self,GAME,x,y,w,h):
		self.GAME=GAME
		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.GAME.COLLISION_BOXES.append(self)
	def remove(self):
		self.GAME.COLLISION_BOXES.remove(self)



class LootChest:
	def __init__(self,GAME,x,y,id_):
		self.GAME=GAME
		self.x=x
		self.y=y
		self.id=id_
		self.loot=self.gen_loot()
		self.c_box=CollisionBox(self.GAME,self.x,self.y,LOOT_CHEST_SIZE,LOOT_CHEST_SIZE)
		self.GAME.LOOT_CHESTS.append(self)
		self.GAME.INTERACTIVE_ITEMS.append(self)
	def remove(self):
		if (len(self.GAME.PLAYERS)>0):self.GAME.PLAYERS[0].sendall(PACKETS["del_loot_chest"]%(self.id))
		self.c_box.remove()
		self.GAME.LOOT_CHESTS.remove(self)
		self.GAME.INTERACTIVE_ITEMS.remove(self)
		for i in range(0,len(self.GAME.GAME_BOARD.board["loot_chests"])):
			c=self.GAME.GAME_BOARD.board["loot_chests"][i]
			if (c["x"]==self.x and c["y"]==self.y):
				self.GAME.GAME_BOARD.board["loot_chests"].remove(c)
				return
	def gen_loot(self):
		def r_weight(*dt):
			a=[]
			for d in dt:
				for i in range(0,d[1]):
					a.append(d[0])
			return a[int(Random()*len(a))]
		l=[]
		ni=int(Random()*(MAX_LOOT_CHEST_ITEMS-MIN_LOOT_CHEST_ITEMS)+MIN_LOOT_CHEST_ITEMS)
		for i in range(0,ni):
			dt=[]
			for o in GUN_DATA.keys():
				dt.append([o,GUN_DATA[o]["proc"]])
			type_=r_weight(*dt)
			dt=[]
			for j in range(0,len(GUN_DATA[type_]["types"])):
				dt.append([j,GUN_DATA[type_]["types"][j]["proc"]])
			g_type=r_weight(*dt)
			ammo=int(Random()*(GUN_DATA[type_]["types"][g_type]["total_ammo"]-Ceil(GUN_DATA[type_]["types"][g_type]["total_ammo"]/2))+Ceil(GUN_DATA[type_]["types"][g_type]["total_ammo"]/2))
			l.append([type_,g_type,ammo])
		return l
	def open(self):
		for l in self.loot:
			x=self.x+LOOT_CHEST_SIZE/2+int(Random()*MIN_PICKUP_DIST-MIN_PICKUP_DIST/2)
			y=self.y+LOOT_CHEST_SIZE/2+int(Random()*MIN_PICKUP_DIST-MIN_PICKUP_DIST/2)
			i=GunItem(self.GAME,x,y,l[0],l[1],l[2],0)
	def mouse_over(self,mx,my,tx,ty):
		x=self.x-tx
		y=self.y-ty
		return (mx>=x and mx<=x+LOOT_CHEST_SIZE and my>=y and my<=y+LOOT_CHEST_SIZE)
	def interact(self):
		self.open()
		self.remove()
	def get_box(self):
		return [self.x,self.y,self.x+LOOT_CHEST_SIZE,self.y+LOOT_CHEST_SIZE]



def send_bullets(GAME):
	if (len(GAME.PLAYERS)==0):return
	s=""
	for b in GAME.BULLETS:
		s+=b.encode()+":"
	s=s[:len(s)-1]
	GAME.PLAYERS[0].sendall(PACKETS["bullet_data"]%(s))
def _u_bullets(GAME):
	u=False
	for i in range(len(GAME.BULLETS)-1,-1,-1):
		b=GAME.BULLETS[i]
		b.started=True
		b.update()
		if (b.updated==True):
			u=True
		else:
			GAME.BULLETS.remove(b)
		send_bullets(GAME)
	Sleep(1/30)
	if (u==True and END==False):
		thr=Thread(target=_u_bullets,args=(GAME,),kwargs={})
		thr.deamon=True
		thr.start()
class Bullet:
	def __init__(self,GAME,x,y,vx,vy,damage,range_,id_,target):
		self.GAME=GAME
		self.sx=x+0
		self.sy=y+0
		self.lx=x+0
		self.ly=y+0
		self.x=x
		self.y=y
		self.vx=vx
		self.vy=vy
		self.damage=damage
		self.range=range_
		self.target=target
		self.updated=False
		self.no_kill=id_
		self.started=False
		self.GAME.BULLETS.append(self)
		if (len(self.GAME.BULLETS)==1):
			thr=Thread(target=_u_bullets,args=(self.GAME,),kwargs={})
			thr.deamon=True
			thr.start()
		thr=Thread(target=self._s,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def _s(self):
		Sleep(3/30)
		if (self.started==False):
			_u_bullets(self.GAME)
	def ray_check(self):
		def dist(ax,ay,bx,by):
			return Sqrt((ax-bx)**2+(ay-by)**2)
		def pointCircle(px,py,cx,cy,cr):
			return (dist(px,py,cx,cy)<=cr)
		def pointLine(px,py,sx,sy,ex,ey):
			b=0.1
			return (dist(px,py,sx,sy)+dist(px,py,ex,ey)>=dist(sx,sy,ex,ey)-b and dist(px,py,sx,sy)+dist(px,py,ex,ey)<=dist(sx,sy,ex,ey)+b)
		def lineCircle(sx,sy,ex,ey,cx,cy,cr):
			if (pointCircle(sx,sy,cx,cy,cr) or pointCircle(ex,ey,cx,cy,cr)):
				return True
			if (not pointLine(sx+(((((cx-sx)*(ex-sx))+((cy-sy)*(ey-sy)))/((sx-ex)*(sx-ex)+(sy-ey)*(sy-ey)))*(ex-sx)),sy+(((((cx-sx)*(ex-sx))+((cy-sy)*(ey-sy)))/((sx-ex)*(sx-ex)+(sy-ey)*(sy-ey)))*(ey-sy)),sx,sy,ex,ey)):
				return False
			return (Sqrt((sx+(((((cx-sx)*(ex-sx))+((cy-sy)*(ey-sy)))/((sx-ex)*(sx-ex)+(sy-ey)*(sy-ey)))*(ex-sx))-cx)*(sx+(((((cx-sx)*(ex-sx))+((cy-sy)*(ey-sy)))/((sx-ex)*(sx-ex)+(sy-ey)*(sy-ey)))*(ex-sx))-cx)+(sy+(((((cx-sx)*(ex-sx))+((cy-sy)*(ey-sy)))/((sx-ex)*(sx-ex)+(sy-ey)*(sy-ey)))*(ey-sy))-cy)*(sy+(((((cx-sx)*(ex-sx))+((cy-sy)*(ey-sy)))/((sx-ex)*(sx-ex)+(sy-ey)*(sy-ey)))*(ey-sy))-cy))<=cr)
		lo=[]
		l=[self.x,self.y,self.lx,self.ly]
		for p in self.GAME.PLAYERS:
			if (p.DEAD==True or p.JUMPPED_OFF==False):continue
			if (p.ID!=self.no_kill and lineCircle(*l,p.POS_X,p.POS_Y,PLAYER_NOMOVE_CIRCLE_RADIUS)):
				lo.append(p)
		if (len(lo)>0):
			sd=dist(*l)
			co=None
			for o in lo:
				d=dist(self.lx,self.ly,o.POS_X,o.POS_Y)
				if (d<sd):
					sd=d
					co=o
			if (o!=None):
				o.damage(self.damage,self.target)
				return True
		return False
	def update(self):
		self.updated=False
		self.lx=self.x+0
		self.ly=self.y+0
		self.x+=self.vx
		self.y+=self.vy
		if (Sqrt((self.x-self.sx)**2+(self.y-self.sy)**2)>=self.range):
			return
		if (self.ray_check()==True):
			return
		self.updated=True
	def encode(self):
		s=""
		s+=str(int(self.x))+","
		s+=str(int(self.y))+","
		s+=str(int(Atan2(self.vy,self.vx)/(PI/180)))
		return s



class Gun:
	def __init__(self,GAME,target,type_="basic",g_type=-1,ammo=-1):
		self.GAME=GAME
		self.target=target
		self.type=type_
		self.g_type=int(Random()*len(GUN_DATA[self.type]["types"])) if g_type==-1 else g_type
		self.m_ammo=GUN_DATA[self.type]["types"][self.g_type]["total_ammo"]
		self.ammo=GUN_DATA[self.type]["types"][self.g_type]["total_ammo"] if ammo==-1 else ammo
		self.m_reloading=GUN_DATA[self.type]["types"][self.g_type]["reload_time"]
		self.name=GUN_DATA[self.type]["types"][self.g_type]["name"]
		self.reloading=-1
		self.m_cooldown=GUN_DATA[self.type]["types"][self.g_type]["cooldown"]
		self.cooldown=-1
		self.bullet_data=GUN_DATA[self.type]["types"][self.g_type]["bullets"]
		self.updated=False
	def shoot(self):
		if (self.reloading==-1 and self.ammo>0 and self.cooldown<=Time()):
			self.create_bullet()
			self.ammo-=1
			self.target.shoot_gun()
			self.cooldown=self.m_cooldown+Time()
			if (self.ammo==0):
				self.cooldown=-1
				self.reload()
	def create_bullet(self):
		pp=self.target.player_pos()
		a=self.target.player_rot()*(PI/180)
		p={}
		p["x"]=pp["x"]+(PLAYER_NOMOVE_CIRCLE_RADIUS-10)*Cos(a+PI/4)
		p["y"]=pp["y"]+(PLAYER_NOMOVE_CIRCLE_RADIUS)*Sin(a+PI/4)
		vx=self.bullet_data["speed"]/30*Cos(a)
		vy=self.bullet_data["speed"]/30*Sin(a)
		Bullet(self.GAME,p["x"],p["y"],vx,vy,self.bullet_data["damage"],self.bullet_data["range"],self.target.player_id(),self.target.player())
	def reload(self):
		if (self.reloading==-1):
			self.reloading=self.m_reloading+0
			self.target.reload_gun()
	def drop(self,s=False):
		x=self.target.player_pos()["x"]+int(Random()*MIN_PICKUP_DIST-MIN_PICKUP_DIST/2)
		y=self.target.player_pos()["y"]+int(Random()*MIN_PICKUP_DIST-MIN_PICKUP_DIST/2)
		i=GunItem(self.GAME,x,y,self.type,self.g_type,self.ammo)
		if (s!=True):
			i.s_time=0
	def update(self):
		self.updated=False
		if (self.reloading>-1):
			self.reloading-=1/30
			self.updated=True
			if (self.reloading<=0):
				self.updated=False
				self.reloading=-1
				self.ammo=self.m_ammo
	def encode(self,f=False):
		s=""
		if (f==False):
			s+=str(GUN_DATA[self.type]["id"])+"."
			s+=str(self.g_type)+"."
			s+=GUN_DATA[self.type]["types"][self.g_type]["name"]+"."
			s+=str(self.m_ammo)+"."
			s+=str(self.ammo)+"."
			s+=str(int((self.reloading+1/30)/self.m_reloading*100)) if self.reloading>-1 else "-1"
		if (f==True):
			s+=str(GUN_DATA[self.type]["id"])+","
			s+=str(self.g_type)
		return s



class Inventory:
	def __init__(self,GAME,target):
		self.GAME=GAME
		self.target=target
		self.inv=[-1 for i in range(0,5)]
		self.main=0
		self.updated=False
	def update(self):
		self.updated=False
		for i in range(0,5):
			if (self.inv[i]!=-1):
				self.inv[i].update()
				if (self.inv[i].updated==True):
					self.updated=True
	def shoot_gun(self):
		self.target.send_inv()
	def reload_gun(self):
		if (self.updated==False):
			self.target.start_update_inv()
	def scroll_max(self):
		self.main=(self.main+1)%5
	def scroll_min(self):
		self.main=(self.main-1+5)%5
	def move_item(self,sl):
		self.inv[self.main],self.inv[sl]=self.inv[sl],self.inv[self.main]
	def can_shoot(self):
		return (self.inv[self.main]!=-1 and self.inv[self.main].ammo>0)
	def shoot(self):
		self.inv[self.main].shoot()
	def player_pos(self):
		return {"x":self.target.POS_X,"y":self.target.POS_Y}
	def player_rot(self):
		return self.target.FACING_ROT
	def player_id(self):
		return self.target.ID
	def player(self):
		return self.target
	def drop(self):
		for i in self.inv:
			if (i==-1):continue
			i.drop()
	def drop_item(self):
		if (self.inv[self.main]!=-1):
			self.inv[self.main].drop(True)
			self.inv[self.main]=-1
			self.target.send_inv()
			self.target.send_mainhand()
	def is_full(self):
		for i in self.inv:
			if (i==-1):
				return False
		return True
	def add(self,i):
		for s in range(0,len(self.inv)):
			if (self.inv[s]==-1):
				self.inv[s]=i
				self.target.send_inv()
				self.target.send_mainhand()
				return
	def encode(self,f=False):
		s=""
		if (f==False):
			s+=str(self.main)+","
			for g in self.inv:
				if (g==-1):
					s+="-1,"
					continue
				s+=g.encode()+","
			s=s[:len(s)-1]
		if (f==True):
			if (self.inv[self.main]!=-1):
				s+=self.inv[self.main].encode(True)
			else:
				s+="-1"
		return s



class ConsoleClient(WebSocket):
	def handleMessage(self):
		self.sendMessage("null")
		thr=Thread(target=self.process_message,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def handleConnected(self):
		self.sendMessage("null")
		if (END==True):
			self.close()
			return
		thr=Thread(target=self.setup,args=(),kwargs={})
		thr.deamon=True
		thr.start()
		pass
	def handleClose(self):
		global CONSOLE_CLIENTS
		CONSOLE_CLIENTS.remove(self)
		del IDS[self.ID]
	def setup(self):
		if (self.check_admin()==False):
			return
		global CONSOLE_CLIENTS
		CONSOLE_CLIENTS.append(self)
		self.sendMessage("tx&&RED,BRIGHT&&Connected to console!")
	def process_message(self):
		msg=self.data
		if (msg[:2]=="cm"):
			msg=msg[2:]
			for j in msg.split(COMMAND_SPLIT_TOKEN):
				if (parse_console_command(j)==True):
					END=True
					end()
					break
			return
		if (msg[:2]=="dc"):
			self.close()
	def sendConsoleMessage(self,msg):
		self.sendMessage(msg.replace("\n","<br>").replace("\t","&nbsp;"*4).replace(" ","&nbsp;"))
	def check_admin(self):
		for p in PLAYERS.keys():
			pl=PLAYERS[p]
			if (get_address(self.address[0])==pl["addr"]):
				if (pl["admin"]==False):
					self.sendMessage("na"+get_address(self.address[0]))
					return False
				return True
		self.sendMessage("nr"+get_address(self.address[0]))
		return False
def start_console():
	if (WEB_CONSOLE==True):
		thr=Thread(target=console,args=[],kwargs={})
		thr.deamon=True
		thr.start()
		global CONSOLE_SERVER;
		CONSOLE_SERVER=SimpleWebSocketServer("192.168.178.65",8070,ConsoleClient)
		print_queue(format("&&RED,BRIGHT&&WebSocket has started on port 8070!"))
		CONSOLE_SERVER.serveforever()
	else:
		console()
def parse_console_command(i):
	global CHAT,DECODE_CONSOLE_CHAT,LOG_MOVE_PACKETS,BANS,END,PLAYERS
	if (i[:5].upper()=="STOP:"):
		for s in SOCKETS:
			s.sendMessage(PACKETS["server_close"]%(i[5:]))
		log_console("&&RED&&"+"Server stopped".center(60,"=").replace("Server stopped","&&RED,BRIGHT&&Server stopped&&NORMAL&&"))
		END=True
		return True
	elif (i[:5].upper()=="KICK:"):
		r=""
		if (len(i[5:].split(":"))==2):
			r=i[5:].split(":")[1]
		IDS[int(i[5:].split(":")[0])].kick(r)
		log_console(f"&&YELLOW&&Kicking &&GREEN&&{IDS[int(i[5:].split(':')[0])].NAME} &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&{int(i[5:].split(':')[0])}&&WHITE,BRIGHT&&) &&YELLOW,NORMAL&&from the server")
		return
	elif (i[:5].upper()=="LIST:"):
		i=i[5:]
		if (i=="all"):
			s="&&YELLOW&&"+"PLAYER LIST".center(60,"=").replace("PLAYER LIST","&&YELLOW,BRIGHT&&PLAYER LIST&&NORMAL&&")+"&&RESET_ALL&&\n"
			for pk in PLAYERS.keys():
				p=PLAYERS[pk]
				dt=""
				if (p["addr"] in BANS.keys() and BANS[p["addr"]][0]>=Time()):dt=Strftime("%d/MONTH/%Y %I:%M%p",Datetime.fromtimestamp(BANS[p["addr"]][0]).timetuple()).replace("MONTH",str(Datetime.fromtimestamp(BANS[p["addr"]][0]).month))
				s+=f"&&MAGENTA,NORMAL&&ID {p['id']}:\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&NAME: &&CYAN,NORMAL&&{p['name']}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ONLINE: &&CYAN,NORMAL&&{'Yes' if p['on']==True else 'No'}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ADDRESS: &&CYAN,NORMAL&&{p['addr']}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ADMIN: &&CYAN,NORMAL&&{'Yes' if p['admin']==True else 'No'}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& BANNED: &&CYAN,NORMAL&&{'Yes &&BLUE,BRIGHT&&(Until '+dt+')' if (p['addr'] in BANS.keys() and BANS[p['addr']][0]>=Time()) else 'No'}\n\n"
			if (len(PLAYERS)==0):s+=" "
		else:
			s="&&YELLOW&&"+"PLAYER DATA".center(60,"=").replace("PLAYER DATA","&&YELLOW,BRIGHT&&PLAYER DATA&&NORMAL&&")+"&&RESET_ALL&&\n"
			p=PLAYERS[int(i)]
			dt=""
			if (p["addr"] in BANS.keys() and BANS[p["addr"]][0]>=Time()):dt=Strftime("%d/MONTH/%Y %I:%M%p",Datetime.fromtimestamp(BANS[p["addr"]][0]).timetuple()).replace("MONTH",str(Datetime.fromtimestamp(BANS[p["addr"]][0]).month))
			s+=f"&&MAGENTA,NORMAL&&ID {p['id']}:\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&NAME: &&CYAN,NORMAL&&{p['name']}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ONLINE: &&CYAN,NORMAL&&{'Yes' if p['on']==True else 'No'}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ADDRESS: &&CYAN,NORMAL&&{p['addr']}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ADMIN: &&CYAN,NORMAL&&{'Yes' if p['admin']==True else 'No'}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& BANNED: &&CYAN,NORMAL&&{'Yes &&BLUE,BRIGHT&&(Until '+dt+')' if (p['addr'] in BANS.keys() and BANS[p['addr']][0]>=Time()) else 'No'}\n\n"
		s=s[:len(s)-1]+"&&YELLOW,NORMAL&&"+"="*60
		log_console(s)
		return
	elif (i[:5].upper()=="CLEAR"):
		System("CLS")
		for c in CONSOLE_CLIENTS:
			c.sendConsoleMessage("cl")
		log_console("&&BLACK,BRIGHT&&Console cleared")
	elif (i[:5].upper()=="CHAT:"):
		i=i[5:]
		if (i=="off"):
			CHAT=False
			log_console("&&YELLOW&&Chat has been turned &&BRIGHT&&off")
		elif (i=="on"):
			CHAT=True
			log_console("&&YELLOW&&Chat has been turned &&BRIGHT&&on")
		elif (i=="decode"):
			DECODE_CONSOLE_CHAT=True
			log_console("&&YELLOW&&Chat decode has been turned &&BRIGHT&&on")
		elif (i=="no-decode"):
			DECODE_CONSOLE_CHAT=False
			log_console("&&YELLOW&&Chat decode has been turned &&BRIGHT&&off")
		elif (i=="log-move"):
			LOG_MOVE_PACKETS=True
			log_console("&&YELLOW&&Logging move packets has been turned &&BRIGHT&&on")
		elif (i=="no-log-move"):
			LOG_MOVE_PACKETS=False
			log_console("&&YELLOW&&Logging move packets has been turned &&BRIGHT&&off")
		elif (i=="log-inv"):
			LOG_INV_DATA=True
			log_console("&&YELLOW&&Logging inventory data packets has been turned &&BRIGHT&&on")
		elif (i=="no-log-inv"):
			LOG_INV_DATA=False
			log_console("&&YELLOW&&Logging inventory data packets has been turned &&BRIGHT&&off")
		return
	elif (i[:4].upper()=="BAN:"):
		i=i[4:].split(":")
		if (len(i)==2):i.append("Default ban")
		t=0
		for tm in i[1].split(" "):
			if (tm.endswith("y")):t+=60*60*24*365*int(tm[:len(tm)-1])
			elif (tm.endswith("m")):t+=60*60*24*30*int(tm[:len(tm)-1])
			elif (tm.endswith("d")):t+=60*60*24*int(tm[:len(tm)-1])
			elif (tm.endswith("h")):t+=60*60*int(tm[:len(tm)-1])
			elif (tm.endswith("mn")):t+=60*int(tm[:len(tm)-2])
		t=max(t,0)+Time()
		BANS[PLAYERS[int(i[0])]["addr"]]=[round(t),i[2]]
		save_bans(BANS)
		log_console(f"&&GREEN&&{PLAYERS[int(i[0])]['name']} &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&{i[0]}&&WHITE,BRIGHT&&) &&YELLOW,NORMAL&&has been banned from the server for &&BLUE,BRIGHT&&{tm}")
		for s in SOCKETS:
			sa=get_address(s.address[0])
			if (PLAYERS[int(i[0])]["addr"]==sa):
				s.sendMessage(PACKETS["banned"]%(BANS[PLAYERS[int(i[0])]["addr"]][0],BANS[PLAYERS[int(i[0])]["addr"]][1]))
				log(f"&&YELLOW,BRIGHT&&PRIVATE: &&RESET_ALL&&({s.ID})\t{s.decode_packet(PACKETS['banned']%(BANS[PLAYERS[int(i[0])]['addr']][0],BANS[PLAYERS[int(i[0])]['addr']][1]))}")
		return
	elif (i[:6].upper()=="UNBAN:"):
		i=i[6:]
		if (i=="all"):
			for k in BANS.keys():
				BANS[k]=[0,""]
			log_console("&&GREEN&&All&&YELLOW&& players have been unbanned from the server")
		else:
			if (PLAYERS[int(i)]["addr"] in BANS.keys()):
				BANS[PLAYERS[int(i)]["addr"]]=[0,""]
			log_console(f"&&GREEN&&{PLAYERS[int(i)]['name']} &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&{i}&&WHITE,BRIGHT&&) &&YELLOW,NORMAL&&has been unbanned from the server")
		save_bans(BANS)
		return
	elif (i[:4].upper()=="CHN:"):
		i=i[4:].split(":")
		log_console(f"&&YELLOW&&Changing player name &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&{i[0]}&&WHITE,BRIGHT&&) &&YELLOW,NORMAL&&from &&BLUE,BRIGHT&&{PLAYERS[int(i[0])]['name']} &&YELLOW,NORMAL&&to &&BLUE,BRIGHT&&{i[1]}")
		if (PLAYERS[int(i[0])]["name"] in USED_NAMES):
			USED_NAMES.remove(PLAYERS[int(i[0])]["name"])
		USED_NAMES.append(i[1])
		PLAYERS[int(i[0])]["name"]=i[1]
		save_players(PLAYERS)
		save_used_names(USED_NAMES)
		if (int(i[0]) in IDS.keys()):
			IDS[int(i[0])].NAME=i[1]
			IDS[int(i[0])].sendMessage(PACKETS["name_change_true"]%(i[1]))
			IDS[int(i[0])].sendall(PACKETS["name_change"]%(int(i[0]),i[1]))
	elif (i[:6].upper()=="ADMIN:"):
		i=i[6:].split(":")
		if (i[0]=="list"):
			s="&&YELLOW&&"+"ADMINS".center(60,"=").replace("ADMINS","&&BRIGHT&&ADMINS&&NORMAL&&")+"&&RESET_ALL&&\n"
			for pk in PLAYERS.keys():
				p=PLAYERS[pk]
				if (p["admin"]==True):
					dt=""
					if (p["addr"] in BANS.keys() and BANS[p["addr"]][0]>=Time()):dt=Strftime("%d/MONTH/%Y %I:%M%p",Datetime.fromtimestamp(BANS[p["addr"]][0]).timetuple()).replace("MONTH",str(Datetime.fromtimestamp(BANS[p["addr"]][0]).month))
					s+=f"&&MAGENTA,NORMAL&&ID {p['id']}:\n&&YELLOW,NORMAL&&-> &&WHITE,BRIGHT&&NAME: &&CYAN,NORMAL&&{p['name']}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ONLINE: &&CYAN,NORMAL&&{'Yes' if p['on']==True else 'No'}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ADDRESS: &&CYAN,NORMAL&&{p['addr']}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& ADMIN: &&CYAN,NORMAL&&{'Yes' if p['admin']==True else 'No'}\n&&YELLOW,NORMAL&&->&&WHITE,BRIGHT&& BANNED: &&CYAN,NORMAL&&{'Yes &&BLUE,BRIGHT&&(Until '+dt+')' if (p['addr'] in BANS.keys() and BANS[p['addr']][0]>=Time()) else 'No'}\n\n"
			if (not s.endswith("\n\n")):s+=" "
			s=s[:len(s)-1]+"&&YELLOW,NORMAL&&"+"="*60
			log_console(s)
		else:
			if (i[1].lower()=="yes"):
				PLAYERS[int(i[0])]['admin']=True
				log_console(f"&&GREEN&&{PLAYERS[int(i[0])]['name']} &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&{i[0]}&&WHITE,BRIGHT&&) &&YELLOW,NORMAL&&is now an &&BLUE,BRIGHT&&admin")
			else:
				PLAYERS[int(i[0])]['admin']=False
				log_console(f"&&GREEN&&{PLAYERS[int(i[0])]['name']} &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&{i[0]}&&WHITE,BRIGHT&&) &&YELLOW,NORMAL&&is now a &&BLUE,BRIGHT&&normal player")
				for c in CONSOLE_CLIENTS:
					c.check_admin()
			save_players(PLAYERS)
	elif (i[:5].upper()=="HELP:"):
		i=i[5:]
		s="&&YELLOW&&"+"HELP".center(60,"=").replace("HELP","&&BRIGHT&&HELP&&NORMAL&&")+"&&RESET_ALL&&\n"
		if (i.lower()=="all"):
			for c in HELP.keys():
				s+=HELP[c]+"\n\n"
		else:
			s+=HELP[i.upper()]+"\n\n"
		s=s[:len(s)-1]+f"\n&&MAGENTA,BRIGHT&&TIP: &&CYAN,NORMAL&&To execute multiple commands at once,you can simple separate the with &&GREEN,BRIGHT&&'&&CYAN,BRIGHT&&{COMMAND_SPLIT_TOKEN}&&GREEN,BRIGHT&&'&&CYAN,NORMAL&&!\n&&CYAN,BRIGHT&&Example: &&BLUE,BRIGHT&&CLEAR&&YELLOW,BRIGHT&&{COMMAND_SPLIT_TOKEN}&&BLUE,BRIGHT&&LIST&&YELLOW,BRIGHT&&:&&WHITE,BRIGHT&&all\n&&YELLOW,NORMAL&&"+"="*60
		log_console(s)
	else:
		log_console(f"&&RED&&Unknown command: "+i)
def log_console(msg):
	print_queue(format(str(msg)))
	for c in CONSOLE_CLIENTS:
		c.sendConsoleMessage("tx"+str(msg))
def console():
	global END
	while True:
		i=input()
		for j in i.split(COMMAND_SPLIT_TOKEN):
			if (parse_console_command(j)==True):
				END=True
				break
		if (END==True):break
	end();
def end():
	Sleep(1.5)
	server.close()
	if (WEB_CONSOLE==True):
		CONSOLE_SERVER.close()
	quit()



class TexturePack:
	def __init__(self,target,data):
		self.target=target
		self.data=self.from_data(data)
		self.target.sendMessage(PACKETS["texture_pack"]%(self.encode()))
	def from_data(self,data):
		if (data=="default"):
			return Deepcopy(DEFAULT_TEXTURE_PACK)
		return Deepcopy(data)
	def ch_key(self,a="-1",b="-1",v="-1"):
		if (a=="-1" and b=="-1"):
			self.data=Deepcopy(DEFAULT_TEXTURE_PACK)
		if (a!="-1" and b=="-1"):
			self.data[a]=Deepcopy(DEFAULT_TEXTURE_PACK)[a]
		if (a!="-1" and b!="-1" and v=="-1"):
			self.data[a][b]=Deepcopy(DEFAULT_TEXTURE_PACK)[a][b]
		if (a!="-91" and b!="-1" and v!="-1"):
			self.data[a][b]=v
		self.target.sendMessage(PACKETS["texture_pack"]%(self.encode()))
	def encode(self):
		s=""
		for gk in self.data.keys():
			s+=gk+":"
			for sgk in self.data[gk].keys():
				s+=sgk+"/"+self.data[gk][sgk]+","
			s=s[:len(s)-1]+";"
		return s[:len(s)-1]



class DropPlane:
	def __init__(self,GAME):
		self.GAME=GAME
		self.gen_data()
	def gen_data(self):
		if (Random()<0.5):
			self.sx=0
			self.sy=int(Random()*GAME_BOARD_HEIGHT)
			self.ex=GAME_BOARD_WIDTH
			self.ey=int(Random()*GAME_BOARD_HEIGHT)
		else:
			self.sx=int(Random()*GAME_BOARD_WIDTH)
			self.sy=0
			self.ex=int(Random()*GAME_BOARD_WIDTH)
			self.ey=GAME_BOARD_HEIGHT
		self.x=self.sx+0
		self.y=self.sy+0
		self.d=Atan2(self.ey-self.sy,self.ex-self.sx)
	def start(self):
		thr=Thread(target=self.update,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def send_pos(self):
		if (len(self.GAME.PLAYERS)>0):
			self.GAME.PLAYERS[0].sendall(PACKETS["drop_plane"]%(self.x,self.y,self.sx,self.sy,self.ex,self.ey))
		for p in self.GAME.PLAYERS:
			if (not hasattr(p,"JUMPPED_OFF") or p.JUMPPED_OFF==True):continue
			p.POS_X=self.x+0
			p.POS_Y=self.y+0
	def remove(self):
		if (len(self.GAME.PLAYERS)>0):
			self.GAME.PLAYERS[0].sendall(PACKETS["no_drop_plane"])
	def update(self):
		self.x+=DROP_PLANE_SPEED/30*Cos(self.d)
		self.y+=DROP_PLANE_SPEED/30*Sin(self.d)
		self.send_pos()
		if (Sqrt((self.x-self.ex)**2+(self.y-self.ey)**2)<DROP_PLANE_END_DIST):
			for p in self.GAME.PLAYERS:
				if (p.JUMPPED_OFF==False):
					p.jump_off()
			self.remove()
			return
		Sleep(1/30)
		thr=Thread(target=self.update,args=(),kwargs={})
		thr.deamon=True
		thr.start()



def enter_game(p):
	for g in GAMES:
		if (not hasattr(g,"TOTAL_PLAYERS")):
			g.TOTAL_PLAYERS=0
		if (g.GAME_STATE==0 and g.TOTAL_PLAYERS<MAX_GAME_PLAYERS):
			g.add_player(p)
			return g
	g=Game()
	g.add_player(p)
	return g
class Game:
	def __init__(self):
		GAMES.append(self)
		self.GAME_ID=len(GAMES)-1
		self.GAME_STATE=0
		self.WAIT_BOARD=SmallWorld(self)
		self.WAIT_BOARD.gen()
		thr=Thread(target=self._st,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def _st(self):
		if (not hasattr(self,"PLAYERS")):
			self.PLAYERS=[]
		self.GAME_BOARD=World(self)
		self.LOOT_CHESTS=[]
		self.BULLETS=[]
		self.COLLISION_BOXES=[]
		self.INTERACTIVE_ITEMS=[]
		self.ITEMS=[]
		if (not hasattr(self,"TOTAL_PLAYERS")):
			self.TOTAL_PLAYERS=0
		if (not hasattr(self,"WS")):
			self.WS="Waiting for players..."
		if (not hasattr(self,"delay_start_num")):
			self.delay_start_num=0
		self.DROP_PLANE=DropPlane(self)
		self.GAME_BOARD.gen()
		self.delay_start()
	def add_player(self,p):
		if (not hasattr(self,"TOTAL_PLAYERS")):
			self.TOTAL_PLAYERS=0
		if (not hasattr(self,"PLAYERS")):
			self.PLAYERS=[]
		self.PLAYERS.append(p)
		self.TOTAL_PLAYERS+=1
		if (self.TOTAL_PLAYERS>=MIN_GAME_PLAYERS):
			self.delay_start()
		if (not hasattr(self,"WS")):
			self.WS="Waiting for players..."
		p.send_(PACKETS["start_game"])
		p.send_(PACKETS["wait_status"]%(self.WS))
		if (not hasattr(self,"delay_start_num")):
			self.delay_start_num=0
		self.check_start()
	def _c(self,n):
		Sleep(MAX_GAME_START_WAIT_TIME)
		if (self.GAME_BOARD.DONE==True and n==self.delay_start_num and self.GAME_STATE==0):
			self.start_game()
	def delay_start(self):
		if (not hasattr(self,"delay_start_num")):
			self.delay_start_num=0
		thr=Thread(target=self._c,args=(self.delay_start_num+0,),kwargs={})
		thr.deamon=True
		thr.start()
	def remove_player(self,p):
		self.PLAYERS.remove(p)
		for pl in self.PLAYERS:
			pl.send_(PACKETS["remove_player"]%(p.ID))
		self.TOTAL_PLAYERS-=1
		self.delay_start_num+=1
		if (self.TOTAL_PLAYERS==0):
			self.remove()
	def remove(self):
		GAMES.remove(self)
	def next_sp(self,p,d):
		id_=p.ID+0
		ids=[]
		pls=[]
		for pl in self.PLAYERS:
			if (hasattr(pl,"DEAD") and pl.DEAD==True):continue
			ids.append(pl.ID)
			pls.append(pl)
		while (True):
			id_+=d
			if (id_>max(ids)):id_=min(ids)
			if (id_<min(ids)):id_=max(ids)
			if (id_ in ids):
				return pls[ids.index(id_)]
	def check_start(self):
		if (self.GAME_STATE==0 and self.TOTAL_PLAYERS==MAX_GAME_PLAYERS and self.GAME_BOARD.DONE==True):
			self.start_game()
	def send_ws(self,m):
		self.WS=m
		for p in self.PLAYERS:
			p.send_(PACKETS["wait_status"]%(m))
	def get_plane_pos(self):
		return self.DROP_PLANE.x,self.DROP_PLANE.y
	def start_game(self):
		thr=Thread(target=self._s_game,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def _s_game(self):
		self.send_ws("3...")
		Sleep(1)
		self.send_ws("2...")
		Sleep(1)
		self.send_ws("1...")
		Sleep(1)
		self.send_ws("Start!")
		self.GAME_STATE=1
		for p in self.PLAYERS:
			p.send_game_board()
		self.DROP_PLANE.start()
	def get_spawn(self):
		b=self.get_board()
		return b.BOARD_WIDTH/2,b.BOARD_HEIGHT/2
	def get_board(self):
		if (self.GAME_STATE==0):
			if (self.WAIT_BOARD.DONE==True):
				return self.WAIT_BOARD
			while (True):
				Sleep(1/30)
				if (self.WAIT_BOARD.DONE==True):
						return self.WAIT_BOARD
		return self.GAME_BOARD
	def log(self,m):
		log("&&RED,NORMAL&&"+str(self.GAME_ID)+"&&CYAN,NORMAL&& => &&RESET_ALL&&"+m)



class GameClient(WebSocket):
	def handleMessage(self):
		self.send_("null")
		thr=Thread(target=self.process_message,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def handleConnected(self):
		self.sendMessage("null")
		if (END==True):
			self.close()
			return
		thr=Thread(target=self.setup,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def handleClose(self):
		if (hasattr(self,"GAME")):
			self.GAME.remove_player(self)
		SOCKETS.remove(self)
		del IDS[self.ID]
		global PLAYERS
		PLAYERS[self.ID]["on"]=False
		save_players(PLAYERS)
		if (self.DEAD==False):
			self.sendall(PACKETS["leave"]%(self.ID))
			self.sendall(PACKETS["remove_player"]%(self.ID))
		else:
			if (self.SPECTATE):
				self.SPECTATE.spectators.remove(self)
	def send_(self,m):
		self.sendMessage(m)
		if (hasattr(self,"spectators")):
			for s in self.spectators:
				s.sendMessage(m)
	def log_(self,m):
		if (hasattr(self,"GAME")):
			self.GAME.log(m)
		else:
			log("&&RED,NORMAL&&GLOBAL&&CYAN,NORMAL&& => &&RESET_ALL&&"+m)
	def sendall(self,m):
		if ((LOG_MOVE_PACKETS==True or (m[:2]!="cm" and m[:2]!="bl" and m[:2]!="mv" and m[:2]!="dp")) and (LOG_INV_DATA==True or (m[:2]!="m" and m[:2]!="mi" and m[:2]!="mh" and m[:2]!="iv" and m[:2]!="mm" and m[:2]!="sh" and m[:2]!="di" and m[:2]!="it" and m[:2]!="ri"))):self.log_(f"&&CYAN,BRIGHT&&PUBLIC: &&RESET_ALL,GREEN&&(ALL)&&RESET_ALL&&\t{self.decode_packet(m)}")
		for p in self.GAME.PLAYERS:
			p.send_(m)
	def check_ban(self):
		a=get_address(self.address[0])
		if (a in BANS.keys() and BANS[a][0]>Time()):
			self.send_(PACKETS["banned"]%(BANS[a][0],BANS[a][1]))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVATE: &&RESET_ALL,GREEN&&({a})&&RESET_ALL&&\t{self.decode_packet(PACKETS['banned']%(BANS[a][0],BANS[a][1]))}")
			self.setup_done=True
			return True
	def is_not_new(self):
		global PLAYERS
		a=get_address(self.address[0])
		for p in PLAYERS.keys():
			if (PLAYERS[p]["addr"]==a):
				if (PLAYERS[p]["on"]==True):return self._already_open()
				PLAYERS[p]["on"]=True
				save_players(PLAYERS)
				return PLAYERS[p]
		return False
	def check_water(self):
		def chk_bridges():
			for b in self.GAME.get_board().board["bridges"]:
				if (self.GAME.get_board().pointPoly(self.POS_X,self.POS_Y,self.GAME.get_board().path_to_arr(b))):
					return True
			return False
		i=self.GAME.get_board().board["island"]
		if (not self.GAME.get_board().pointPoly(self.POS_X,self.POS_Y,self.GAME.get_board().path_to_arr(self.GAME.get_board().board["ground_path"])) or (i!=-1 and self.GAME.get_board().pointPoly(self.POS_X,self.POS_Y,self.GAME.get_board().path_to_arr(i["w_path"])) and not self.GAME.get_board().pointPoly(self.POS_X,self.POS_Y,self.GAME.get_board().path_to_arr(i["path"])) and chk_bridges()==False)):
			d=Sqrt((self.POS_X-self.px)**2+(self.POS_Y-self.py)**2)*PLAYER_WATER_SPEED_PROC
			self.POS_X=self.px+d*Cos(Radians(self.FACING_ROT))
			self.POS_Y=self.py+d*Sin(Radians(self.FACING_ROT))
	def check_box_collision(self):
		def circleRect(cx,cy,cr,rx,ry,rw,rh):
			tX=cx
			tY=cy
			if (cx<rx):tX=rx
			elif (cx>rx+rw):tX=rx+rw
			if (cy<ry):tY=ry
			elif (cy>ry+rh):tY=ry+rh
			return (Sqrt((cx-tX)**2+(cy-tY)**2)<=cr)
		x=self.POS_X
		y=self.POS_Y
		if (hasattr(self.GAME,"COLLISION_BOXES")):
			for b in self.GAME.COLLISION_BOXES:
				if (circleRect(x,y,PLAYER_NOMOVE_CIRCLE_RADIUS,b.x,b.y,b.w,b.h)):
					if (x<=b.x and y<=b.y+b.h and y>=b.y):
						self.POS_X=b.x-PLAYER_NOMOVE_CIRCLE_RADIUS
					elif (x>=b.x+b.w and y<=b.y+b.h and y>=b.y):
						self.POS_X=b.x+b.w+PLAYER_NOMOVE_CIRCLE_RADIUS
					elif (y<=b.y and x<=b.x+b.w and x>=b.x):
						self.POS_Y=b.y-PLAYER_NOMOVE_CIRCLE_RADIUS
					elif (y>=b.y and x<=b.x+b.w and x>=b.x):
						self.POS_Y=b.y+b.h+PLAYER_NOMOVE_CIRCLE_RADIUS
	def send_inv(self):
		self.send_(PACKETS["inventory"]%(self.INVENTORY.encode()))
		if (LOG_INV_DATA==True):log(f"&&YELLOW,BRIGHT&&PRIVATE: &&RESET_ALL,GREEN&&({get_address(self.address[0])})&&RESET_ALL&&\t{self.decode_packet(PACKETS['inventory']%(self.INVENTORY.encode()))}")
	def send_mainhand(self):
		self.sendall(PACKETS["mainhand"]%(self.ID,self.INVENTORY.encode(True)))
	def _u_inv(self):
		while True:
			self.INVENTORY.update()
			self.send_inv()
			if (self.INVENTORY.updated==False):return
			Sleep(1/30)
	def start_update_inv(self):
		thr=Thread(target=self._u_inv,args=(),kwargs={})
		thr.deamon=True
		thr.start()
	def _already_open(self):
		self.setup_done=True
		a=get_address(self.address[0])
		self.send_(PACKETS["already_address_connected"]%(a))
		self.log_(f"&&YELLOW,BRIGHT&&PRIVATE: &&RESET_ALL,GREEN&&({a})&&RESET_ALL&&\t{self.decode_packet(PACKETS['already_address_connected']%(a))}")
		return "close"
	def setup(self):
		if (self.check_ban()==True):return
		SOCKETS.append(self)
		self.TEXTURE=TexturePack(self,"default")
		self.PLAYING=False
		self.WAITING_FOR=-1
		self.PLAYER_SETUP_DONE=False
		dt=self.is_not_new()
		if (dt==False):
			global USED_NAMES
			pid=1
			while True:
				self.NAME=NEW_PLAYER_TEMPLATE%(pid)
				if (PREVENT_PLAYER_ESCAPED_NAMES==True):
					self.NAME=self.NAME.replace("&&","")
				pid+=1
				if (USED_NAMES.count(self.NAME)==0):
					break
			USED_NAMES.append(self.NAME)
			save_used_names(USED_NAMES)
			global NEXT_ID
			self.ID=NEXT_ID
			NEXT_ID+=1
		else:
			if (dt=="close"):return
			self.NAME=dt["name"]
			self.ID=dt["id"]
			if (PREVENT_PLAYER_ESCAPED_NAMES==True):
				self.NAME=self.NAME.replace("&&","")
				PLAYERS[self.ID]["name"]=self.NAME
				save_players(PLAYERS)
			PLAYERS[self.ID]["on"]=False
			save_players(PLAYERS)
		self.sendMessage(PACKETS["setup_name"]%(self.ID,self.NAME))
		self.setup_done=True
	def setup_game(self):
		self.GAME=enter_game(self)
		dt=self.is_not_new()
		if (dt==False):
			# global USED_NAMES
			# pid=1
			# while True:
			# 	self.NAME=NEW_PLAYER_TEMPLATE%(pid)
			# 	if (PREVENT_PLAYER_ESCAPED_NAMES==True):
			# 		self.NAME=self.NAME.replace("&&","")
			# 	pid+=1
			# 	if (USED_NAMES.count(self.NAME)==0):
			# 		break
			# USED_NAMES.append(self.NAME)
			# save_used_names(USED_NAMES)
			# global NEXT_ID
			# IDS[NEXT_ID]=self
			# self.ID=NEXT_ID
			a=get_address(self.address[0])
			log(f"&&GREEN,BRIGHT&&JOIN: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t&&BLACK,BRIGHT&&{a} &&WHITE,BRIGHT&&(NAME=&&CYAN,NORMAL&&{self.NAME}&&WHITE,BRIGHT&&,ID=&&CYAN,NORMAL&&{str(self.ID)}&&WHITE,BRIGHT&&)")
			save_next_id(NEXT_ID)
			self.POS_X,self.POS_Y=self.GAME.get_spawn()
			self.FACING_ROT=int(Random()*360)
			self.INVENTORY=Inventory(self.GAME,self)
			self.HP=10
			self.DEAD=False
			self.JUMPPED_OFF=False
			self.SPECTATE=-1
			self.spectators=[]
			self.START_COINS+0
			global PLAYERS
			PLAYERS[self.ID]={"id":self.ID,"name":self.NAME,"addr":a,"on":True,"admin":False}
			save_players(PLAYERS)
			self.send_(PACKETS["setup_name"]%(self.ID,self.NAME))
			self.send_(PACKETS["setup_board"]%(self.GAME.get_board().encode()))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['setup_name']%(self.ID,self.NAME))}")
			self.damage(0)
		else:
			if (dt=="close"):return
			# self.NAME=dt["name"]
			# IDS[dt["id"]]=self
			# self.ID=dt["id"]
			# if (PREVENT_PLAYER_ESCAPED_NAMES==True):
			# 	self.NAME=self.NAME.replace("&&","")
			# 	PLAYERS[self.ID]["name"]=self.NAME
			# 	save_players(PLAYERS)
			a=get_address(self.address[0])
			self.log_(f"&&GREEN,BRIGHT&&JOIN: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t&&BLACK,BRIGHT&&{a} &&WHITE,BRIGHT&&(NAME=&&CYAN,NORMAL&&{self.NAME}&&WHITE,BRIGHT&&,ID=&&CYAN,NORMAL&&{str(self.ID)}&&WHITE,BRIGHT&&)")
			self.POS_X,self.POS_Y=self.GAME.get_spawn()
			self.FACING_ROT=int(Random()*360)
			self.INVENTORY=Inventory(self.GAME,self)
			self.HP=10
			self.DEAD=False
			self.JUMPPED_OFF=False
			self.SPECTATE=-1
			self.spectators=[]
			self.COINS=START_COINS+0
			self.send_(PACKETS["setup_name"]%(self.ID,self.NAME))
			self.send_(PACKETS["setup_board"]%(self.GAME.get_board().encode()))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['setup_name']%(self.ID,self.NAME))}")
			self.damage(0)
		self.PLAYER_SETUP_DONE=True
		for p in self.GAME.PLAYERS:
			if (hasattr(p,"DEAD") and p.DEAD==True):continue
			if (p==self):continue
			if (self.WAITING_FOR!=p):p.wait(self)
			self.send_(PACKETS["setup_data"]%(p.ID,p.NAME,p.POS_X,p.POS_Y,p.FACING_ROT,p.INVENTORY.encode(True)))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['setup_data']%(p.ID,p.NAME,p.POS_X,p.POS_Y,p.FACING_ROT,p.INVENTORY.encode(True)))}")
		if (hasattr(self.GAME,"ITEMS")):
			for i in self.GAME.ITEMS:
				t=GUN_DATA[i.type]["id"]
				self.send_(PACKETS["item"]%(i.i_id,i.x,i.y,i.dir,t,i.g_type))
				self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['item']%(i.i_id,i.x,i.y,i.dir,t,i.g_type))}")
		self.send_inv()
		self.sendall(PACKETS["setup_data"]%(self.ID,self.NAME,self.POS_X,self.POS_Y,self.FACING_ROT,self.INVENTORY.encode(True)))
		self.sendall(PACKETS["join"]%(self.ID))
		self.PLAYING=True
	def wait(self,p):
		self.WAITING_FOR=p
		while (True):
			Sleep(1/30)
			if (self.PLAYER_SETUP_DONE==True):
				self.WAITING_FOR=-1
				return
	def end_game(self):
		if (hasattr(self,"GAME")):
			ns=self.GAME.next_sp(self,1)
			for s in self.spectators:
				s.SPECTATE=ns
				s.SPECTATE.spectators.append(s)
				s.SPECTATE.setup_spectator(s)
			self.GAME.remove_player(self)
			delattr(self,"GAME")
		self.spectators=[]
		self.PLAYER_SETUP_DONE=False
		if (hasattr(self,"ID")):
			global PLAYERS
			PLAYERS[self.ID]["on"]=False
			save_players(PLAYERS)
		self.PLAYING=False
	def chn(self,msg):
		msg=msg.replace(";","")
		if (self.NAME==msg):
			self.send_(PACKETS["name_change_false"]%(msg,0))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['name_change_false']%(msg,0))}")
			return
		if (len(msg)<MIN_NAME_LENGTH):
			self.send_(PACKETS["name_change_false"]%(msg,1))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['name_change_false']%(msg,1))}")
			return
		if (len(msg)>MAX_NAME_LENGTH):
			self.send_(PACKETS["name_change_false"]%(msg,2))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['name_change_false']%(msg,2))}")
			return
		if (USED_NAMES.count(msg)>0):
			self.send_(PACKETS["name_change_false"]%(msg,3))
			self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['name_change_false']%(msg,3))}")
			return
		self.send_(PACKETS["name_change_true"]%(msg))
		self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['name_change_true']%(msg))}")
		global PLAYERS
		USED_NAMES.remove(self.NAME)
		self.NAME=msg
		if (PREVENT_PLAYER_ESCAPED_NAMES==True):
			self.NAME=self.NAME.replace("&&","")
		USED_NAMES.append(self.NAME)
		PLAYERS[self.ID]["name"]=self.NAME
		save_players(PLAYERS)
		save_used_names(USED_NAMES)
		self.sendall(PACKETS["name_change"]%(self.ID,self.NAME))
	def setup_spectator(self,s):
		s.sendMessage(PACKETS["setup_name"]%(self.ID,self.NAME))
		s.sendMessage(PACKETS["setup_data"]%(self.ID,self.NAME,self.POS_X,self.POS_Y,self.FACING_ROT,self.INVENTORY.encode(True)))
		s.sendMessage(PACKETS["hp"]%(self.HP*2))
		s.sendMessage(PACKETS["move"]%(self.ID,self.POS_X,self.POS_Y,self.FACING_ROT))
	def next_spectator(self,d):
		if (self.SPECTATE==-1):return
		self.SPECTATE.spectators.remove(self)
		self.SPECTATE=self.GAME.next_sp(self.SPECTATE,d)
		self.SPECTATE.spectators.append(self)
		self.SPECTATE.setup_spectator(self)
	def jump_off(self):
		self.JUMPPED_OFF=True
		self.INVENTORY.add(Gun(self.GAME,self.INVENTORY,"basic",0))
		self.POS_X,self.POS_Y=self.GAME.get_plane_pos()
		self.FACING_ROT=int(Random()*360)
		self.sendall(PACKETS["move"]%(self.ID,self.POS_X,self.POS_Y,self.FACING_ROT))
	def send_game_board(self):
		if (not hasattr(self,"COINS")):
			self.COINS=START_COINS+0
		self.send_(PACKETS["start_game"])
		self.send_(PACKETS["wait_status"]%("-1"))
		self.send_(PACKETS["coins"]%(self.COINS))
		self.send_(PACKETS["setup_board"]%(self.GAME.get_board().encode()))
	def damage(self,a,p=None):
		self.HP=max(self.HP-a,0)
		self.last_damage=p
		self.send_(PACKETS["hp"]%(self.HP*2))
		self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['hp']%(self.HP*2))}")
		if (self.HP==0):
			self.kill()
	def drop_coins(self):
		for i in range(0,self.COINS):
			x=self.POS_X+int(Random()*MIN_PICKUP_DIST-MIN_PICKUP_DIST/2)
			y=self.POS_Y+int(Random()*MIN_PICKUP_DIST-MIN_PICKUP_DIST/2)
			CoinItem(self.GAME,x,y)
	def kill(self):
		self.INVENTORY.drop()
		self.DEAD=True
		self.drop_coins()
		self.sendall(PACKETS["remove_player"]%(self.ID))
		self.SPECTATE=self.last_damage
		self.SPECTATE.spectators.append(self)
		self.SPECTATE.setup_spectator(self)
		for s in self.spectators:
			s.SPECTATE=self.SPECTATE
			self.SPECTATE.spectators.append(s)
			self.SPECTATE.setup_spectator(s)
	def interact(self,mx,my,w,h):
		def lineLine(l1sx,l1sy,l1ex,l1ey,l2sx,l2sy,l2ex,l2ey):
			return (((l2ex-l2sx)*(l1sy-l2sy)-(l2ey-l2sy)*(l1sx-l2sx))/((l2ey-l2sy)*(l1ex-l1sx)-(l2ex-l2sx)*(l1ey-l1sy))>=0 and ((l2ex-l2sx)*(l1sy-l2sy)-(l2ey-l2sy)*(l1sx-l2sx))/((l2ey-l2sy)*(l1ex-l1sx)-(l2ex-l2sx)*(l1ey-l1sy))<=1 and ((l1ex-l1sx)*(l1sy-l2sy)-(l1ey-l1sy)*(l1sx-l2sx))/((l2ey-l2sy)*(l1ex-l1sx)-(l2ex-l2sx)*(l1ey-l1sy))>=0 and ((l1ex-l1sx)*(l1sy-l2sy)-(l1ey-l1sy)*(l1sx-l2sx))/((l2ey-l2sy)*(l1ex-l1sx)-(l2ex-l2sx)*(l1ey-l1sy))<=1)
		def lineRect(sx,sy,ex,ey,rx,ry,rw,rh):
			return (lineLine(sx,sy,ex,ey,rx,ry,rx,ry+rh) or lineLine(sx,sy,ex,ey,rx+rw,ry,rx+rw,ry+rh) or lineLine(sx,sy,ex,ey,rx,ry,rx+rw,ry) or lineLine(sx,sy,ex,ey,rx,ry+rh,rx+rw,ry+rh))
		tx=self.POS_X-w/2
		ty=self.POS_Y-h/2
		for i in self.GAME.INTERACTIVE_ITEMS:
			if (i.mouse_over(mx,my,tx,ty) and Sqrt((w/2-mx)**2+(h/2-my)**2)<=MAX_INTERACT_DIST and lineRect(self.POS_X,self.POS_Y,self.POS_X+MAX_INTERACT_DIST*Cos(Radians(self.FACING_ROT)),self.POS_Y+MAX_INTERACT_DIST*Sin(Radians(self.FACING_ROT)),*i.get_box())):
				i.interact()
				return
	def process_message(self,*args):
		def _c(v,a,b):
			return min(max(v,a),b)
		msg=self.data
		if (not hasattr(self,"setup_done")):
			return
		if (hasattr(self,"DEAD") and self.DEAD==True and self.SPECTATE==-1):return
		if (type(msg)!=str):return
		d=get_address(self.address[0])
		if (hasattr(self,"ID")):d=self.ID
		if ((LOG_MOVE_PACKETS==True or (msg[:2]!="cm" and msg[:2]!="bl" and msg[:2]!="mv" and msg[:2]!="dp")) and (LOG_INV_DATA==True or (msg[:2]!="m" and msg[:2]!="mi" and msg[:2]!="mh" and msg[:2]!="iv" and msg[:2]!="mm" and msg[:2]!="sh" and msg[:2]!="di" and msg[:2]!="it" and msg[:2]!="ri"))):self.log_(f"&&MAGENTA,BRIGHT&&RECIVE: &&RESET_ALL,GREEN&&({d})&&RESET_ALL&&\t{self.decode_packet(msg)}")
		if (msg[:2]=="dc"):
			self.close()
		if (msg[:2]=="sg"):
			self.setup_game()
			return
		if (msg[:2]=="tc"):
			self.TEXTURE.ch_key(*msg[2:].split(":"))
			return
		if (msg[:2]=="ns"):
			msg=msg[2:]
			if (msg=="-"):
				self.next_spectator(-1)
			if (msg=="+"):
				self.next_spectator(1)
			return
		if (msg[:2]=="eg"):
			self.end_game()
			return
		if (self.PLAYING==False or self.DEAD==True):
			return
		if (msg[:2]=="jp"):
			self.jump_off()
			return
		if (msg[:2]=="cn"):
			self.chn(msg[2:])
			return
		if (msg[:2]=="cm"):
			if (self.JUMPPED_OFF==False and self.GAME.GAME_STATE==1):return
			msg=msg[2:]
			nX,nY,fc_r=int(msg.split(":")[0]),int(msg.split(":")[1]),int(msg.split(":")[2])
			self.px=int(self.POS_X)
			self.py=int(self.POS_Y)
			self.POS_X=_c(nX,PLAYER_NOMOVE_CIRCLE_RADIUS,self.GAME.get_board().BOARD_WIDTH-PLAYER_NOMOVE_CIRCLE_RADIUS)
			self.POS_Y=_c(nY,PLAYER_NOMOVE_CIRCLE_RADIUS,self.GAME.get_board().BOARD_HEIGHT-PLAYER_NOMOVE_CIRCLE_RADIUS)
			self.FACING_ROT=fc_r
			self.check_water()
			self.check_box_collision()
			if (hasattr(self.GAME,"ITEMS")):
				for i in range(len(self.GAME.ITEMS)-1,-1,-1):
					self.GAME.ITEMS[i].pick_up(self)
			self.POS_X=_c(self.POS_X,PLAYER_NOMOVE_CIRCLE_RADIUS,self.GAME.get_board().BOARD_WIDTH-PLAYER_NOMOVE_CIRCLE_RADIUS)
			self.POS_Y=_c(self.POS_Y,PLAYER_NOMOVE_CIRCLE_RADIUS,self.GAME.get_board().BOARD_HEIGHT-PLAYER_NOMOVE_CIRCLE_RADIUS)
			self.sendall(PACKETS["move"]%(d,self.POS_X,self.POS_Y,self.FACING_ROT))
			return
		if (msg[:2]=="mm"):
			msg=msg[2:]
			if (msg=="-"):
				self.INVENTORY.scroll_min()
			if (msg=="+"):
				self.INVENTORY.scroll_max()
			self.send_inv()
			self.send_mainhand()
			return
		if (msg[:2]=="mi"):
			self.INVENTORY.move_item(int(msg[2:]))
			self.send_inv()
			self.send_mainhand()
			return
		if (msg[:2]=="di"):
			self.INVENTORY.drop_item()
			return
		if (msg[:2]=="sh"):
			if (self.INVENTORY.can_shoot()):
				self.INVENTORY.shoot()
			return
		if (msg[:2]=="in"):
			msg=[int(msg[2:].split(":")[0]),int(msg[2:].split(":")[1]),int(msg[2:].split(":")[2]),int(msg[2:].split(":")[3])]
			self.interact(*msg)
			return
	def decode_packet(self,p):
		if (DECODE_CONSOLE_CHAT==False):return p
		t=p[:2]
		d=p[2:]
		# TO SERVER
		if (t=="sg"):return "&&BLACK,BRIGHT&&Player game join request"
		if (t=="tc"):return "&&BLACK,BRIGHT&&Texture change request &&WHITE,BRIGHT&&(GROUP=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,KEY=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&,VALUE=&&CYAN,NORMAL&&"+d.split(":")[2]+"&&WHITE,BRIGHT&&)"
		if (t=="jp"):return "&&BLACK,BRIGHT&&Player jump request"
		if (t=="cm"):return "&&BLACK,BRIGHT&&Move request &&WHITE,BRIGHT&&(X=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,Y=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&,ROT=&&CYAN,NORMAL&&"+d.split(":")[2]+"&&WHITE,BRIGHT&&)"
		if (t=="cn"):return "&&BLACK,BRIGHT&&Name change request &&WHITE,BRIGHT&&(NEW-NAME=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="mm"):return "&&BLACK,BRIGHT&&Player inventory scroll request &&WHITE,BRIGHT&&(DIR=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="mi"):return "&&BLACK,BRIGHT&&Player inventory item move request &&WHITE,BRIGHT&&(NEW-SLOT=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="di"):return "&&BLACK,BRIGHT&&Player drop item request"
		if (t=="sh"):return "&&BLACK,BRIGHT&&Player shoot request"
		if (t=="in"):return "&&BLACK,BRIGHT&&Player interact request"
		if (t=="ns"):return "&&BLACK,BRIGHT&&Player next spectator request &&WHITE,BRIGHT&&(DIR=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="eg"):return "&&BLACK,BRIGHT&&Player game exit request"
		if (t=="dc"):return "&&BLACK,BRIGHT&&Player logout request"
		# FROM SERVER
		if (t=="ac"):return "&&BLACK,BRIGHT&&IPv4 already connected &&WHITE,BRIGHT&&(IP=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="sn"):return "&&BLACK,BRIGHT&&Default name & id setup &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,DEFAULT-NAME=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&)"
		if (t=="sb"):return "&&BLACK,BRIGHT&&Board setup"
		if (t=="sd"):return "&&BLACK,BRIGHT&&Player data &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,NAME=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&,X=&&CYAN,NORMAL&&"+d.split(":")[2]+"&&WHITE,BRIGHT&&,Y=&&CYAN,NORMAL&&"+d.split(":")[3]+"&&WHITE,BRIGHT&&,ROT=&&CYAN,NORMAL&&"+d.split(":")[4]+"&&WHITE,BRIGHT&&,MAIN_HAND=&&CYAN,NORMAL&&"+d.split(":")[5]+"&&WHITE,BRIGHT&&)"
		if (t=="jn"):return "&&BLACK,BRIGHT&&Server join notification &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="np"):return "&&BLACK,BRIGHT&&Plane remove packet"
		if (t=="nt"):return "&&BLACK,BRIGHT&&Name change approved &&WHITE,BRIGHT&&(NEW-NAME=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="nf"):return "&&BLACK,BRIGHT&&Name change rejected &&WHITE,BRIGHT&&(REJECTED-NAME=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,REASON=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&)"
		if (t=="nc"):return "&&BLACK,BRIGHT&&Player name change &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,NEW-NAME=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&)"
		if (t=="mh"):return "&&BLACK,BRIGHT&&Player mainhand item change &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,ITEM=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&)"
		if (t=="iv"):return "&&BLACK,BRIGHT&&Player inventory change &&WHITE,BRIGHT&&(&&WHITE,BRIGHT&&INVENTORY-DATA=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="mv"):return "&&BLACK,BRIGHT&&Player position change &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,NEW-X=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&,NEW-Y=&&CYAN,NORMAL&&"+d.split(":")[2]+"&&WHITE,BRIGHT&&,NEW-ROT=&&CYAN,NORMAL&&"+d.split(":")[3]+"&&WHITE,BRIGHT&&)"
		if (t=="bl"):return "&&BLACK,BRIGHT&&Bullet position change &&WHITE,BRIGHT&&(BULLETS-DATA=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="hp"):return "&&BLACK,BRIGHT&&Player health points change &&WHITE,BRIGHT&&(NEW-HP=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="it"):return "&&BLACK,BRIGHT&&New item data &&WHITE,BRIGHT&&(ITEM-ID=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,X=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&,Y=&&CYAN,NORMAL&&"+d.split(":")[2]+"&&WHITE,BRIGHT&&,ROT=&&CYAN,NORMAL&&"+d.split(":")[3]+"&&WHITE,BRIGHT&&,ITEM_DATA=&&CYAN,NORMAL&&"+d.split(":")[4]+"&&WHITE,BRIGHT&&)"
		if (t=="cd"):return "&&BLACK,BRIGHT&&Player coin data packet&&WHITE,BRIGHT&&(COIN(S)=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="ri"):return "&&BLACK,BRIGHT&&Item remove packet &&WHITE,BRIGHT&&(ITEM-ID=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="rc"):return "&&BLACK,BRIGHT&&Loot chest remove packet &&WHITE,BRIGHT&&(LOOT-CHEST-ID=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="rp"):return "&&BLACK,BRIGHT&&Player remove packet &&WHITE,BRIGHT&&(PLAYER-ID=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="lv"):return "&&BLACK,BRIGHT&&Server leave notification &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="kk"):return "&&BLACK,BRIGHT&&Player got kicked from the server &&WHITE,BRIGHT&&(ID=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="pk"):return "&&BLACK,BRIGHT&&Player got kicked from the server &&WHITE,BRIGHT&&(REASON=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		if (t=="bn"):return "&&BLACK,BRIGHT&&Player got banned from the server &&WHITE,BRIGHT&&(TIME=&&CYAN,NORMAL&&"+d.split(":")[0]+"&&WHITE,BRIGHT&&,REASON=&&CYAN,NORMAL&&"+d.split(":")[1]+"&&WHITE,BRIGHT&&)"
		if (t=="sc"):return "&&BLACK,BRIGHT&&Server closed &&WHITE,BRIGHT&&(REASON=&&CYAN,NORMAL&&"+d+"&&WHITE,BRIGHT&&)"
		return "None:\t"+p
	def kick(self,r):
		self.sendall(PACKETS["kick"]%(self.ID))
		self.send_(PACKETS["private_kick"]%(r))
		self.log_(f"&&YELLOW,BRIGHT&&PRIVAT: &&RESET_ALL,GREEN&&({self.ID})&&RESET_ALL&&\t{self.decode_packet(PACKETS['private_kick']%(r))}")



#============================
#         TO SERVER
#============================
# sg -> Player game join request
# tc[GROUP]:[KEY]:[VALUE] -> Texture change packet
# jp -> Player drop plane jump off request
# cm[X]:[Y]:[ROT] -> Player move validation packet
# cn[NAME] -> Name change packet
# mm[DIR] -> Player inv scroll packet
# mi[INVENTORY-SLOT] -> Player item move request
# di -> Player drop item request
# sh -> Player shoot request
# in[MOUSE-X]:[MOUSE-Y]:[CNV-WIDTH]:[CNV-HEIGHT] -> Player interact request
# ns[DIR] -> PLayer next spectator request
# eg -> Player game exit request
# dc -> Player logout request



#============================
#        FROM SERVER
#============================
# ac[IP] -> Player already connected packet
# sp -> Start playing packet
# tp[TEXTURE-PACK-DATA] -> Texture pack data packet
# sn[ID]:[NAME] -> Default player name packet
# sb[BOARD] -> Board setup packet
# sd[ID]:[NAME]:[X]:[Y]:[ROT]:[INVENTORY-MAINHAND] -> Player data packet
# jn[ID] -> Player join packet
# ws[TEXT] -> Game wait status message
# dp[X]:[Y]:[END-X]:[END-Y] -> Drop plane data packet
# np -> Drop plane remove packet
# nt[NAME] -> Name change confirmed packet
# nf[NAME]:[REASON] -> Name change uncormifmed packet
# nc[ID]:[NAME] -> Name chnage packet
# mh[ID]:[INVENTORY-MAINHAND] -> Player mainhand inventory packet
# iv[INVENTORY] -> PLayer inventory packet
# mv[ID]:[X]:[Y]:[ROT] -> Player move packet
# bl[BULLETS_DATA] -> Bullets data packet
# hp[HP] -> Player health points packet
# it[ITEM-ID]:[X]:[Y]:[ROT]:[ITEM-TYPE]:[ITEM-DATA] -> New item data
# cd[COINS] -> PLayer coin data packet
# ri[ITEM-ID] -> Item delete packet
# rc[CHEST-ID] -> Loot chest delete packet
# rp[PLAYER-ID] -> Player remove packet
# lv[ID] -> Player leave packet
# kk[ID] -> Player kick packet
# pk[REASON] -> Player kick reason packet
# bn[TIME]:[REASON] -> Player ban notification packet
# sc[REASON] -> Server closed packet



date=Date.today()
fp=LOG_FILE_PATH+Strftime("%d_%m_%y",Gmtime())+".log"
if (not Exists(fp)):
	with open(fp,"w") as f:
		f.write("LOG - "+Strftime("%a,%d %b %Y %H:%M:%S",Gmtime())+"\n\n")
else:
	with open(fp,"a") as f:
		f.write("\nLOG - "+Strftime("%a,%d %b %Y %H:%M:%S",Gmtime())+"\n\n")


USED_NAMES=load_used_names()
NEXT_ID=load_next_id()
PLAYERS=load_players()
BANS=load_bans()



Init()



thr=Thread(target=start_console,args=(),kwargs={})
thr.deamon=True
thr.start()
Sleep(0.5)
server=SimpleWebSocketServer("192.168.178.65",8080,GameClient)
print_queue(format("&&RED,BRIGHT&&WebSocket has started on port 8080!"))
server.serveforever()