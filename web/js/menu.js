class Menu{
	constructor(){
		this.BUTTONS=[]
		this.type=null
		this.draw_data={}
		this.bgl={main:"main_bg",used_ip:"error_bg",kick:"error_bg",ban:"error_bg",server:"error_bg",disconnect:"error_bg"}
		this.TRANS_TIMER=-1
		this.SLIDE_NEXT=null
		this.SLIDE_NEXT_ARGS=null
		this.TRANS_TIME=30
	}
	_o(mn,...args){
		this.BUTTONS=[]
		this.type=null
		this.draw_data={}
		var _={
			main:function(ths){
				ths.type="main"
			},
			exit_game:function(ths){
				console.log("esc")
			},
			used_ip:function(ths,ip){
				ths.BUTTONS.push(new Button(30,30,190,60,IMGS.get("buttons/back"),function(){MENU.open_menu("main")}))
				ths.type="used_ip"
				ths.draw_data.ip=ip
			},
			kick:function(ths,r){
				ths.BUTTONS.push(new Button(30,30,190,60,IMGS.get("buttons/back"),function(){MENU.open_menu("main")}))
				ths.type="kick"
				ths.draw_data.r=r
			},
			ban:function(ths,tm,r){
				ths.BUTTONS.push(new Button(30,30,190,60,IMGS.get("buttons/back"),function(){MENU.open_menu("main")}))
				ths.type="ban"
				ths.draw_data.tm=tm
				ths.draw_data.r=r
			},
			server_close:function(ths,r){
				ths.BUTTONS.push(new Button(30,30,190,60,IMGS.get("buttons/back"),function(){MENU.open_menu("main")}))
				ths.type="server"
				ths.draw_data.r=r
			}
		}[mn](this,...args)
	}
	update_buttons(e){
		for (var b of this.BUTTONS){
			b.mousePressed(e)
		}
	}
	open_menu(t,...targs){
		this.sound=SOUNDS.play("page_sweep",75)
		this.TRANS_TIMER=0
		this.SLIDE_NEXT=t
		this.SLIDE_NEXT_ARGS=targs
	}
	draw(){
		if (this.type!=null){
			ctx.drawImage(IMGS.get(this.bgl[this.type]),0,0,cnv.width,cnv.height)
		}
		for (var b of this.BUTTONS){
			b.draw()
		}
		if (this.type=="kick"){
			ctx.font="150px Teko"
			ctx.lineCap="square"
			ctx.textAlign="center"
			ctx.fillStyle=color(160,20,20)
			ctx.fillText("Kicked.",cnv.width/2,cnv.height/2-100)
			ctx.font="45px Teko"
			ctx.fillStyle=color(113,10,10)
			ctx.fillText("Reason - "+this.draw_data.r,cnv.width/2,cnv.height/2-50)
		}
		else if (this.type=="ban"){
			ctx.font="150px Teko"
			ctx.lineCap="square"
			ctx.textAlign="center"
			ctx.fillStyle=color(160,20,20)
			ctx.fillText("Banned.",cnv.width/2,cnv.height/2-100)
			ctx.font="70px Teko"
			ctx.fillStyle=color(113,10,10)
			ctx.fillText("Until "+this.draw_data.tm,cnv.width/2,cnv.height/2-40)
			ctx.font="55px Teko"
			ctx.fillStyle=color(123,16,16)
			ctx.fillText("Reason - "+this.draw_data.r,cnv.width/2,cnv.height/2+10)
		}
		else if (this.type=="used_ip"){
			ctx.font="150px Teko"
			ctx.lineCap="square"
			ctx.textAlign="center"
			ctx.fillStyle=color(160,20,20)
			ctx.fillText("Already Connected.",cnv.width/2,cnv.height/2-100)
			ctx.font="45px Teko"
			ctx.fillStyle=color(113,10,10)
			ctx.fillText("Your IP ("+this.draw_data.ip+") is already connected",cnv.width/2,cnv.height/2-50)
		}
		else if (this.type=="server"){
			ctx.font="150px Teko"
			ctx.lineCap="square"
			ctx.textAlign="center"
			ctx.fillStyle=color(160,20,20)
			ctx.fillText("Server Closed.",cnv.width/2,cnv.height/2-100)
			ctx.font="45px Teko"
			ctx.fillStyle=color(113,10,10)
			ctx.fillText("Reason - "+this.draw_data.r,cnv.width/2,cnv.height/2-50)
		}
		else if (this.type=="disconnected"){
			ctx.font="150px Teko"
			ctx.lineCap="square"
			ctx.textAlign="center"
			ctx.fillStyle=color(160,20,20)
			ctx.fillText("Disconnected.",cnv.width/2,cnv.height/2-100)
		}
		if (this.TRANS_TIMER>-1&&this.TRANS_TIMER<parseInt(this.TRANS_TIME*2.5)){
			this.TRANS_TIMER++
		}
		if (this.TRANS_TIMER>-1&&this.TRANS_TIMER<this.TRANS_TIME){
			ctx.fillStyle=color(5)
			ctx.fillRect(this.TRANS_TIMER.map(0,this.TRANS_TIME,-cnv.width,0),0,cnv.width,cnv.height)
			this.TRANS_TIMER++
		}
		else if (this.TRANS_TIMER>=this.TRANS_TIME&&this.TRANS_TIMER<parseInt(this.TRANS_TIME*1.5)){
			ctx.fillStyle=color(5)
			ctx.fillRect(0,0,cnv.width,cnv.height)
		}
		else if (this.TRANS_TIMER>=parseInt(this.TRANS_TIME*1.5)&&this.TRANS_TIMER<parseInt(this.TRANS_TIME*2.5)){
			ctx.fillStyle=color(5)
			ctx.fillRect(this.TRANS_TIMER.map(parseInt(this.TRANS_TIME*1.5),parseInt(this.TRANS_TIME*2.5),0,cnv.width),0,cnv.width,cnv.height)
			this.TRANS_TIMER++
		}
		if (this.TRANS_TIMER==parseInt(this.TRANS_TIME*1.25)){
			this._o(this.SLIDE_NEXT,...this.SLIDE_NEXT_ARGS)
			this.SLIDE_NEXT=null
			this.SLIDE_NEXT_ARGS=null
		}
		if (this.TRANS_TIMER>=parseInt(this.TRANS_TIME*2.5)){
			this.TRANS_TIMER=-1
			this.sound.stop()
		}
	}
}