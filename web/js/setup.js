var wr,
	cnv,
	ctx,
	audioCtx
var PLAYER=null,
	BOARD=null,
	TEXTURE=null,
	ISLAND=null,
	MODE=0,
	BRIDGES=[],
	GROUND_PATH=[],
	PATHS=[],
	TREES=[],
	CONNECTED=false,
	ITEM_TEXT=[
		"",
		-1
	],
	DROP_PLANE=null,
	MOUSEDOWN=false,
	MOUSEPOS={
		x:-1,
		y:-1
	},
	WAIT_STATUS=-1,
	DRAW_BOUNDING_BOX=false,
	NOMOVE_CIRCLE_RADIUS=50,
	MAX_SPEED=35,
	LOOT_CHESTS=[],
	GRAPHICS=[],
	ITEMS={},
	BULLETS=[],
	HEART_VELS=[],
	PLAYING=false,
	MENU={
		open:false,
		type:"",
		buttons:[],
		o:function(mn){
			this.open=true
			this.type=mn
			this.buttons=[]
			if (this.type=="pause"){
				this.add_button("Resume Game",function(){
					MENU.esc()
				},cnv.width/2,cnv.height/2-125,650,100)
				this.add_button("Exit Game",function(){
					MENU.o("main")
					PLAYING=false
					DROP_PLANE=null
					PLAYER=null
				},cnv.width/2,cnv.height/2+25,650,100)
			}
			else if (this.type=="main"){
				SOCKET.send("eg")
				this.add_button("PLAY",function(){
					SOCKET.send("sg")
					MENU.open=false
					MENU.type=""
					MENU.buttons=[]
				},cnv.width/2,cnv.height/2,700,200,true)
			}
		},
		add_button:function(t,f,x,y,w,h,p){
			this.buttons.push(new Button(x,y,w,h,t,f,p))
		},
		esc:function(){
			if (this.open==true&&this.type=="pause"){
				this.open=false
				this.type=""
				this.buttons=[]
			}
			else if (this.open==false){
				this.o("pause")
			}
		},
		update:function(){
			this.buttons.forEach((b)=>b.mousePressed(MOUSEPOS))
		}
	},
	SETTINGS={
		open:false,
		off_open:-500,
		off_dir:0,
		off_speed:100,
		o:function(w){
			if (this.open==false){
				this.start_u_loop()
			}
			this.off_dir=this.off_speed+0
			if (w=="main"){
				//
			}
		},
		esc:function(){
			if (this.open==true){
				this.off_dir=0-this.off_speed
				if (this.open==true){
					this.start_u_loop()
				}
			}
		},
		update:function(){
			var X=MOUSEPOS.x,Y=MOUSEPOS.y
			if (this.off_dir==0&&this.open==false&&X>=40&&X<=100&&Y>=40&&Y<=100){
				this.o("main")
			}
		},
		start_u_loop:function(){
			f=function(){
				if (SETTINGS.off_dir<0){
					if (Math.abs(-500-SETTINGS.off_open)<250){
						SETTINGS.off_dir=Math.abs(-500-SETTINGS.off_open).map(0,250,1,-SETTINGS.off_speed,true,true)
					}
				}
				if (SETTINGS.off_dir>0){
					if (Math.abs(0-SETTINGS.off_open)<250){
						SETTINGS.off_dir=Math.abs(0-SETTINGS.off_open).map(0,250,1,SETTINGS.off_speed,true,true)
					}
				}
				SETTINGS.off_open+=SETTINGS.off_dir
				if (SETTINGS.off_open>=0&&SETTINGS.off_dir>0){
					SETTINGS.off_open=0
					SETTINGS.open=true
					SETTINGS.off_dir=0
					return
				}
				else{
					SETTINGS.open=false
					if (SETTINGS.off_open<=-500&&SETTINGS.off_dir<0){
						SETTINGS.off_open=-500
						SETTINGS.off_dir=0
						return
					}
				}
				setTimeout(f,1/30*1000)
			}
			setTimeout(f,1/30*1000)
		}
	},
	DATA={
		NAME:null,
		ID:-1
	},
	BOARD_WIDTH=-1,
	BOARD_HEIGHT=-1,
	MINIMAP_WIDTH=200,
	MINIMAP_HEIGHT=200,
	MAX_ANGLE_CHANGE=15,
	TILE_SIZE=100,
	SPAWN_CIRCLE_POINTS=100