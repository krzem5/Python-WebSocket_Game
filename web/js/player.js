class Player{
	constructor(){
		this.NAME=null
		this.ID=-1
		this.PLAYERS={}
		this.pos={x:0,y:0}
		this.fdir=0
		this.inv=[-1,-1,-1,-1,-1]
		this.main_h=0
		this.FOLLOW=false
		this.STATE=0
		this.HP=-1
		this.COINS=-1
	}
	keyPress(e){
		if (MENU.open==true){return}
		if (MODE==0){
			if (this.STATE==0){
				if (e.keyCode==32){
					SOCKET.send("jp")
					this.STATE=2
				}
			}
			if (this.STATE==2){
					if (e.keyCode==32){
						this.shoot()
					}
					if (e.keyCode==38||e.keyCode==39){
						SOCKET.send("mm+")
					}
					if (e.keyCode==37||e.keyCode==40){
						SOCKET.send("mm-")
					}
					if (e.keyCode>=49&&e.keyCode<=52){
						SOCKET.send("mi"+(e.keyCode-49))
					}
					if (e.keyCode==81){
						SOCKET.send("di")
					}
					if (e.keyCode==69){
						SOCKET.send("in"+MOUSEPOS.x+":"+MOUSEPOS.y+":"+cnv.width+":"+cnv.height)
					}
			}
		}
		if (MODE==1){
			if (e.keyCode==38||e.keyCode==39){
				SOCKET.send("ns+")
			}
			if (e.keyCode==37||e.keyCode==40){
				SOCKET.send("ns-")
			}
		}
	}
	mouseMove(e){
		if (CONNECTED==false||MODE!=0||(this.STATE==0&&this.COINS!=-1)){return}
		function _c(v,a,b){
			return Math.min(Math.max(v,a),b)
		}
		this.follow(e)
		var d=Math.min(Math.sqrt((e.x-cnv.width/2)**2+(e.y-cnv.height/2)**2),300)
		var p={x:cnv.width/2,y:cnv.height/2}
		if (d>=NOMOVE_CIRCLE_RADIUS){
			d=d.map(0,300,0,MAX_SPEED)
			var nx=_c(Math.floor(Math.cos(this.fdir.toRadians())*d+this.pos.x),NOMOVE_CIRCLE_RADIUS,BOARD_WIDTH-NOMOVE_CIRCLE_RADIUS),ny=_c(Math.floor(Math.sin(this.fdir.toRadians())*d+this.pos.y),NOMOVE_CIRCLE_RADIUS,BOARD_HEIGHT-NOMOVE_CIRCLE_RADIUS)
			this.pos.x=nx
			this.pos.y=ny
		}
		SOCKET.send("cm"+this.pos.x+":"+this.pos.y+":"+this.fdir)
	}
	start_follow(){
		this.FOLLOW=true
	}
	stop_follow(){
		this.FOLLOW=false
	}
	follow(e){
		if (CONNECTED==false||MODE!=0||(this.STATE==0&&this.COINS!=-1)){return}
		function _c(v,a,b){
			return Math.min(Math.max(v,a),b)
		}
		var p={x:cnv.width/2,y:cnv.height/2}
		var dir=(parseInt(parseInt(Math.atan2(e.y-p.y,e.x-p.x).toDegrees()+180).map(-180,180,0,360)))%360
		if (dir+180<this.fdir){this.fdir-=360}
		else if (this.fdir+180<dir){this.fdir+=360}
		dir=this.fdir+_c(dir-this.fdir,-MAX_ANGLE_CHANGE,MAX_ANGLE_CHANGE)
		this.fdir=parseInt(dir%360)
		SOCKET.send("cm"+this.pos.x+":"+this.pos.y+":"+this.fdir)
	}
	set_inv(dt){
		function p_item(s){
			if (s=="-1"){
				return -1
			}
			s=s.split(".")
			i={}
			i.type=parseInt(s[0])
			i.g_type=parseInt(s[1])
			i.name=s[2]
			i.m_ammo=parseInt(s[3])
			i.ammo=parseInt(s[4])
			i.reloading=parseInt(s[5])
			return i
		}
		function is_same_item(i1,i2){
			return (i1.name==i2.name&&i1.type==i2.type&&i1.g_type==i2.g_type)
		}
		dt=dt.split(",")
		var f=this.main_h!=parseInt(dt[0])||(this.inv[this.main_h]==-1&&dt[this.main_h+1]!="-1")||(p_item(dt[this.main_h+1])!=-1&&!is_same_item(this.inv[this.main_h],p_item(dt[this.main_h+1])))
		this.main_h=parseInt(dt[0])
		for (var i in dt){
			if (i==0){continue}
			this.inv[i-1]=p_item(dt[i])
		}
		if (f==true){
			ITEM_TEXT=[this.inv[this.main_h].name,0]
		}
		if (this.inv[this.main_h]==-1){
			ITEM_TEXT=["",-1]
		}
	}
	update(){
		if (MENU.open==true){return}
		if (MOUSEDOWN==true){this.mouseMove(MOUSEPOS)}
		if (this.FOLLOW==true){this.follow(MOUSEPOS)}
	}
	shoot(){
		if (MENU.open==true){return}
		SOCKET.send("sh")
	}
}