function draw(){
	ctx.clearRect(0,0,cnv.width,cnv.height)
	if (CONNECTED==false){
		ctx.fillStyle="#0a0a0a"
		ctx.textAlign="center"
		ctx.textBaseline="middle"
		ctx.font="55px SnigletB"
		ctx.fillText("Connecting...",cnv.width/2,cnv.height/2-40)
		ctx.fillStyle="#696969"
		ctx.font="25px SnigletB"
		ctx.fillText("Please Wait",cnv.width/2,cnv.height/2+10)
	}
	if (TEXTURE==null||CONNECTED==false){
		requestAnimationFrame(draw)
		return
	}
	function draw_gun(g,hand=false){
		ctx.fillStyle=color(40)
		if (hand==false){
			ctx.fillRect(-8,-20,16,40)
		}
		else{
			ctx.fillRect(-8,-30,16,40)
		}
	}
	function draw_player(p,x,y){
		x=x||p.pos.x-TRANSLATE.x
		y=y||p.pos.y-TRANSLATE.y
		ctx.fillStyle=to_rgba(TEXTURE.player.body)
		ctx.strokeStyle=to_rgba(TEXTURE.player.body_border)
		ctx.lineWidth=5
		ctx.translate(x,y)
		ctx.rotate(p.fdir.toRadians()+Math.PI/2)
		ctx.beginPath()
		ctx.arc(30,-20,NOMOVE_CIRCLE_RADIUS*0.3,0,Math.PI*2)
		ctx.fill()
		ctx.stroke()
		if (p.mh!=-1){
			ctx.translate(30,-20)
			draw_gun(p.mh,true)
			ctx.translate(-30,20)
			ctx.fillStyle=to_rgba(TEXTURE.player.body)
			ctx.strokeStyle=to_rgba(TEXTURE.player.body_border)
			ctx.lineWidth=5
		}
		ctx.beginPath()
		ctx.arc(-30,-20,NOMOVE_CIRCLE_RADIUS*0.3,0,Math.PI*2)
		ctx.fill()
		ctx.stroke()
		ctx.beginPath()
		ctx.arc(0,0,NOMOVE_CIRCLE_RADIUS*0.6,0,Math.PI*2)
		ctx.fill()
		ctx.stroke()
		ctx.rotate(-p.fdir.toRadians()-Math.PI/2)
		ctx.translate(-x,-y)
	}
	function draw_coin(x,y){
		p=GRAPHICS[6]
		ctx.fillStyle=to_rgba(TEXTURE.object.coin)
		ctx.strokeStyle=to_rgba(TEXTURE.object.coin_border)
		ctx.lineWidth=3
		ctx.translate(x,y)
		ctx.beginPath()
		ctx.moveTo(p[p.length-1].x,p[p.length-1].y)
		for (var p of p){
			ctx.lineTo(p.x,p.y)
		}
		ctx.fill()
		ctx.stroke()
		ctx.translate(-x,-y)
	}
	function draw_button(b){
		ctx.lineCap="round"
		ctx.lineJoin="round"
		ctx.fillStyle=to_rgba(TEXTURE.menu.button)
		ctx.strokeStyle=to_rgba(TEXTURE.menu.button_border)
		if (b.PLAY==true){
			ctx.fillStyle=to_rgba(TEXTURE.menu.play_button)
			ctx.strokeStyle=to_rgba(TEXTURE.menu.play_button_border)
		}
		ctx.lineWidth=10
		ctx.beginPath()
		ctx.arc(b.pos.x-b.size.w/2+b.size.h/2,b.pos.y,b.size.h/2,Math.PI/2,Math.PI*1.5)
		ctx.lineTo(b.pos.x+b.size.w/2-b.size.h/2,b.pos.y-b.size.h/2)
		ctx.arc(b.pos.x+b.size.w/2-b.size.h/2,b.pos.y,b.size.h/2,Math.PI*1.5,Math.PI/2)
		ctx.lineTo(b.pos.x-b.size.w/2+b.size.h/2,b.pos.y+b.size.h/2)
		ctx.fill()
		ctx.stroke()
		ctx.fillStyle=to_rgba(TEXTURE.menu.button_text)
		if (b.PLAY==true){
			ctx.fillStyle=to_rgba(TEXTURE.menu.play_button_text)
		}
		ctx.textAlign="center"
		ctx.font=(b.PLAY==true?"120px SnigletB":"80px SnigletB")
		ctx.textBaseline="middle"
		ctx.fillText(b.txt,b.pos.x,b.pos.y)
	}
	if (PLAYING==true){
		if (BOARD==null||PLAYER.PLAYERS[PLAYER.ID]==undefined){
			requestAnimationFrame(draw)
			return
		}
		ctx.fillStyle=to_rgba(TEXTURE.world.water)
		ctx.fillRect(0,0,cnv.width,cnv.height)
		var TRANSLATE={x:0,y:0}
		PLAYER.update()
		for (var i=0;i<10;i++){
			HEART_VELS[i]++
		}
		if (PLAYER.ID!=-1){
			TRANSLATE.x=PLAYER.PLAYERS[PLAYER.ID].pos.x-cnv.width/2
			TRANSLATE.y=PLAYER.PLAYERS[PLAYER.ID].pos.y-cnv.height/2
		}
		ctx.fillStyle=to_rgba(TEXTURE.world.grass)
		ctx.beginPath()
		ctx.moveTo(GROUND_PATH[GROUND_PATH.length-1].x-TRANSLATE.x,GROUND_PATH[GROUND_PATH.length-1].y-TRANSLATE.y)
		for (var p of GROUND_PATH){
			ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
		}
		ctx.fill()
		if (ISLAND!=null){
			ctx.fillStyle=to_rgba(TEXTURE.world.water)
			ctx.strokeStyle=to_rgba(TEXTURE.world.grass_border)
			ctx.lineWidth=10
			ctx.beginPath()
			ctx.moveTo(ISLAND.w_path[ISLAND.w_path.length-1].x-TRANSLATE.x,ISLAND.w_path[ISLAND.w_path.length-1].y-TRANSLATE.y)
			for (var p of ISLAND.w_path){
				ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
			}
			ctx.fill()
			if (ISLAND.type==2){
				ctx.stroke()
			}
			ctx.fillStyle=to_rgba(TEXTURE.world.sand)
			ctx.strokeStyle=to_rgba(TEXTURE.world.sand_border)
			ctx.lineWidth=10
			ctx.beginPath()
			ctx.moveTo(ISLAND.path[ISLAND.path.length-1].x-TRANSLATE.x,ISLAND.path[ISLAND.path.length-1].y-TRANSLATE.y)
			for (var p of ISLAND.path){
				ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
			}
			ctx.fill()
			ctx.stroke()
		}
		for (var b of BRIDGES){
			ctx.fillStyle=to_rgba(TEXTURE.world.bridge)
			ctx.beginPath()
			ctx.moveTo(b[b.length-1].x-TRANSLATE.x,b[b.length-1].y-TRANSLATE.y)
			for (var p of b){
				ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
			}
			ctx.fill()
		}
		for (var p of PATHS){
			ctx.fillStyle=to_rgba(TEXTURE.world.path)
			ctx.beginPath()
			ctx.moveTo(p[p.length-1].x-TRANSLATE.x,p[p.length-1].y-TRANSLATE.y)
			for (var v of p){
				ctx.lineTo(v.x-TRANSLATE.x,v.y-TRANSLATE.y)
			}
			ctx.fill()
		}
		ctx.globalAlpha=0.3
		ctx.lineWidth=1
		ctx.strokeStyle=to_rgba(TEXTURE.other.grid)
		for (var j=0;j<BOARD_WIDTH/TILE_SIZE;j++){
			for (var i=0;i<BOARD_HEIGHT/TILE_SIZE;i++){
				if (!on_board(i*TILE_SIZE-TRANSLATE.x,j*TILE_SIZE-TRANSLATE.y,TILE_SIZE)){continue}
				ctx.strokeRect(i*TILE_SIZE-TRANSLATE.x,j*TILE_SIZE-TRANSLATE.y,TILE_SIZE,TILE_SIZE)
			}
		}
		ctx.globalAlpha=1
		S=5
		ctx.fillStyle=to_rgba(TEXTURE.world.water)
		ctx.beginPath()
		ctx.moveTo(-TRANSLATE.x-S,-TRANSLATE.y-S)
		ctx.lineTo(BOARD_WIDTH-TRANSLATE.x+S,-TRANSLATE.y-S)
		ctx.lineTo(BOARD_WIDTH-TRANSLATE.x+S,BOARD_HEIGHT-TRANSLATE.y+S)
		ctx.lineTo(-TRANSLATE.x-S,BOARD_HEIGHT-TRANSLATE.y+S)
		ctx.lineTo(-TRANSLATE.x-S,-TRANSLATE.y-S)
		for (var pi=GROUND_PATH.length-1;pi>=0;pi--){
			p=GROUND_PATH[pi]
			ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
		}
		ctx.lineTo(GROUND_PATH[GROUND_PATH.length-1].x-TRANSLATE.x,GROUND_PATH[GROUND_PATH.length-1].y-TRANSLATE.y)
		ctx.lineTo(-TRANSLATE.x-S,-TRANSLATE.y-S)
		ctx.fill()
		ctx.beginPath()
		ctx.strokeStyle=to_rgba(TEXTURE.world.grass_border)
		ctx.lineWidth=10
		ctx.moveTo(GROUND_PATH[GROUND_PATH.length-1].x-TRANSLATE.x,GROUND_PATH[GROUND_PATH.length-1].y-TRANSLATE.y)
		for (var p of GROUND_PATH){
			ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
		}
		ctx.stroke()
		for (var i of Object.values(ITEMS)){
			ctx.translate(i.x-TRANSLATE.x,i.y-TRANSLATE.y)
			ctx.rotate(i.dir.toRadians())
			if (i.type==0){
				draw_gun(i.data)
			}
			if (i.type==1){
				draw_coin(0,0)
			}
			ctx.rotate(-i.dir.toRadians())
			ctx.translate(-i.x+TRANSLATE.x,-i.y+TRANSLATE.y)
		}
		for (var pi of Object.keys(PLAYER.PLAYERS)){
			if (PLAYER.PLAYERS[pi].id==PLAYER.ID||PLAYER.ID==-1){continue}
			var p=PLAYER.PLAYERS[pi]
			if (!on_board(p.pos.x-TRANSLATE.x,p.pos.y-TRANSLATE.y,NOMOVE_CIRCLE_RADIUS*2)){continue}
			draw_player(p)
		}
		if (PLAYER.ID>-1&&PLAYER.PLAYERS!=undefined&&PLAYER.PLAYERS[PLAYER.ID]!=undefined){
			var p=PLAYER.PLAYERS[PLAYER.ID]
			draw_player(p,cnv.width/2,cnv.height/2)
		}
		for (var c of Object.values(LOOT_CHESTS)){
			ctx.fillStyle=to_rgba(TEXTURE.object.loot_chest)
			ctx.strokeStyle=to_rgba(TEXTURE.object.loot_chest_border)
			ctx.lineWidth=5
			ctx.translate(c.x-TRANSLATE.x,c.y-TRANSLATE.y)
			ctx.fillRect(0,0,100,100)
			ctx.strokeRect(0,0,100,100)
			ctx.translate(-c.x+TRANSLATE.x,-c.y+TRANSLATE.y)
		}
		for (var b of BULLETS){
			p=GRAPHICS[3]
			ctx.fillStyle=to_rgba(TEXTURE.object.bullet)
			ctx.strokeStyle=to_rgba(TEXTURE.object.bullet_border)
			ctx.lineWidth=5
			ctx.translate(b.x-TRANSLATE.x,b.y-TRANSLATE.y)
			ctx.rotate(b.dir.toRadians())
			ctx.beginPath()
			ctx.moveTo(p[p.length-1].x,p[p.length-1].y)
			for (var v of p){
				ctx.lineTo(v.x,v.y)
			}
			ctx.fill()
			ctx.stroke()
			ctx.rotate(-b.dir.toRadians())
			ctx.translate(-b.x+TRANSLATE.x,-b.y+TRANSLATE.y)
		}
		for (var t of TREES){
			if (on_board(t.x-TRANSLATE.x,t.y-TRANSLATE.y,t.r)){
				[C,BC]=calc_tree_color(t.c)
				ctx.fillStyle=C
				ctx.strokeStyle=BC
				ctx.lineWidth=10
				ctx.beginPath()
				ctx.moveTo(t.p[t.p.length-1].x-TRANSLATE.x,t.p[t.p.length-1].y-TRANSLATE.y)
				for (var p of t.p){
					ctx.lineTo(p.x-TRANSLATE.x,p.y-TRANSLATE.y)
				}
				if (PLAYER.STATE==2&&Math.sqrt((t.x-TRANSLATE.x-cnv.width/2)*(t.x-TRANSLATE.x-cnv.width/2)+(t.y-TRANSLATE.y-cnv.height/2)*(t.y-TRANSLATE.y-cnv.height/2))<=t.r){
					ctx.fillStyle=color(C,75)
				}
				ctx.fill()
				ctx.stroke()
			}
		}
		if (DROP_PLANE!=null){
			p=GRAPHICS[5]
			ctx.fillStyle=to_rgba(TEXTURE.object.drop_plane)
			ctx.strokeStyle=to_rgba(TEXTURE.object.drop_plane_border)
			ctx.lineWidth=10
			ctx.translate(DROP_PLANE.x-TRANSLATE.x,DROP_PLANE.y-TRANSLATE.y)
			ctx.rotate(DROP_PLANE.d+Math.PI/2)
			ctx.beginPath()
			ctx.moveTo(p[p.length-1].x,p[p.length-1].y)
			for (var v of p){
				ctx.lineTo(v.x,v.y)
			}
			ctx.fill()
			ctx.stroke()
			ctx.rotate(-DROP_PLANE.d-Math.PI/2)
			ctx.translate(-DROP_PLANE.x+TRANSLATE.x,-DROP_PLANE.y+TRANSLATE.y)
		}
		for (var pi of Object.keys(PLAYER.PLAYERS)){
			if (PLAYER.PLAYERS[pi].id==PLAYER.ID){continue}
			var p=PLAYER.PLAYERS[pi]
			if (!on_board(p.pos.x-TRANSLATE.x,p.pos.y-TRANSLATE.y,NOMOVE_CIRCLE_RADIUS*2+25)){continue}
			ctx.translate(p.pos.x-TRANSLATE.x,p.pos.y-TRANSLATE.y)
			ctx.font="20px SnigletB"
			ctx.textAlign="center"
			ctx.lineCap="round"
			ctx.lineJoin="round"
			ctx.textBaseline="middle"
			ctx.fillStyle=to_rgba(TEXTURE.player.nametag)
			ctx.fillText(p.name,0,-NOMOVE_CIRCLE_RADIUS-7)
			ctx.translate(-p.pos.x+TRANSLATE.x,-p.pos.y+TRANSLATE.y)
		}
		ctx.beginPath()
		ctx.fillStyle=to_rgba(TEXTURE.world.water)
		ctx.moveTo(cnv.width-30,30)
		ctx.lineTo(cnv.width-30,30+MINIMAP_HEIGHT)
		ctx.lineTo(cnv.width-30-MINIMAP_WIDTH,30+MINIMAP_HEIGHT)
		ctx.lineTo(cnv.width-30-MINIMAP_WIDTH,30)
		ctx.lineTo(cnv.width-30,30)
		ctx.fill()
		ctx.beginPath()
		ctx.fillStyle=to_rgba(TEXTURE.world.grass)
		ctx.moveTo(GROUND_PATH[GROUND_PATH.length-1].x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),GROUND_PATH[GROUND_PATH.length-1].y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
		for (var p of GROUND_PATH){
			ctx.lineTo(p.x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),p.y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
		}
		ctx.fill()
		if (ISLAND!=null){
			ctx.fillStyle=to_rgba(TEXTURE.world.water)
			ctx.beginPath()
			ctx.moveTo(parseInt(ISLAND.w_path[ISLAND.w_path.length-1].x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(ISLAND.w_path[ISLAND.w_path.length-1].y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			for (var p of ISLAND.w_path){
				ctx.lineTo(parseInt(p.x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(p.y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			}
			ctx.fill()
			ctx.fillStyle=to_rgba(TEXTURE.world.sand)
			ctx.beginPath()
			ctx.moveTo(parseInt(ISLAND.path[ISLAND.path.length-1].x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(ISLAND.path[ISLAND.path.length-1].y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			for (var p of ISLAND.path){
				ctx.lineTo(parseInt(p.x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(p.y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			}
			ctx.fill()
		}
		for (var b of BRIDGES){
			ctx.fillStyle=to_rgba(TEXTURE.world.bridge)
			ctx.beginPath()
			ctx.moveTo(parseInt(b[b.length-1].x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(b[b.length-1].y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			for (var p of b){
				ctx.lineTo(parseInt(p.x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(p.y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			}
			ctx.fill()
		}
		for (var p of PATHS){
			ctx.fillStyle=to_rgba(TEXTURE.world.path)
			ctx.beginPath()		
			ctx.moveTo(parseInt(p[p.length-1].x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(p[p.length-1].y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			for (var v of p){
				ctx.lineTo(parseInt(v.x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(v.y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			}
			ctx.fill()
		}
		for (var t of TREES){
			ctx.fillStyle=calc_tree_color(t.c)[0]
			p=t.p
			ctx.beginPath()
			ctx.moveTo(parseInt(p[p.length-1].x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(p[p.length-1].y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			for (var v of p){
				ctx.lineTo(parseInt(v.x).map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),parseInt(v.y).map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			}
			ctx.fill()
		}
		ctx.beginPath()
		ctx.strokeStyle=to_rgba(TEXTURE.gui.border)
		ctx.lineWidth=2
		ctx.lineJoin="round"
		ctx.moveTo(cnv.width-30,30)
		ctx.lineTo(cnv.width-30,30+MINIMAP_HEIGHT)
		ctx.lineTo(cnv.width-30-MINIMAP_WIDTH,30+MINIMAP_HEIGHT)
		ctx.lineTo(cnv.width-30-MINIMAP_WIDTH,30)
		ctx.lineTo(cnv.width-30,30)
		ctx.stroke()
		for (var c of Object.values(LOOT_CHESTS)){
			p=GRAPHICS[4]
			X=c.x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true)
			Y=c.y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true)
			ctx.fillStyle=to_rgba(TEXTURE.map.loot_chest)
			ctx.translate(X,Y)
			ctx.rotate(Math.PI/4)
			ctx.beginPath()
			ctx.moveTo(p[p.length-1].x,p[p.length-1].y)
			for (var v of p){
				ctx.lineTo(v.x,v.y)
			}
			ctx.fill()
			ctx.rotate(-Math.PI/4)
			ctx.translate(-X,-Y)
		}
		if (DROP_PLANE!=null){
			ctx.lineWidth=5
			ctx.strokeStyle=to_rgba(TEXTURE.map.drop_plane_A)
			ctx.beginPath()
			ctx.setLineDash([20,20])
			ctx.moveTo(DROP_PLANE.sx.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),DROP_PLANE.sy.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			ctx.lineTo(DROP_PLANE.ex.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),DROP_PLANE.ey.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			ctx.stroke()
			ctx.strokeStyle=to_rgba(TEXTURE.map.drop_plane_B)
			ctx.beginPath()
			ctx.setLineDash([20,20])
			ctx.moveTo(DROP_PLANE.sx.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true)+DROP_PLANE.x2,DROP_PLANE.sy.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true)+DROP_PLANE.y2)
			ctx.lineTo(DROP_PLANE.ex.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),DROP_PLANE.ey.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			ctx.stroke()
			ctx.setLineDash([])
		}
		for (var pi of Object.keys(PLAYER.PLAYERS)){
			if (PLAYER.PLAYERS[pi].id==PLAYER.ID||PLAYER.ID==-1){continue}
			var p=PLAYER.PLAYERS[pi]
			ctx.translate(p.pos.x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),p.pos.y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
			ctx.fillStyle=to_rgba(TEXTURE.map.other_player)
			ctx.beginPath()
			ctx.arc(0,0,5,0,Math.PI*2)
			ctx.fill()
			ctx.translate(-p.pos.x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),-p.pos.y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
		}
		ctx.translate(PLAYER.pos.x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),PLAYER.pos.y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
		ctx.fillStyle=to_rgba(TEXTURE.map.current_player)
		ctx.beginPath()
		ctx.arc(0,0,7,0,Math.PI*2)
		ctx.fill()
		ctx.translate(-PLAYER.pos.x.map(0,BOARD_WIDTH,cnv.width-30-MINIMAP_WIDTH,cnv.width-30,true),-PLAYER.pos.y.map(0,BOARD_HEIGHT,30,30+MINIMAP_HEIGHT,true))
		for (var i in PLAYER.inv){
			if (i==PLAYER.main_h){
				ctx.strokeStyle=to_rgba(TEXTURE.gui.main_hand_border)
				ctx.lineWidth=5
			}
			else{
				ctx.strokeStyle=to_rgba(TEXTURE.gui.other_slot_border)
				ctx.lineWidth=2
			}
			ctx.fillStyle=to_rgba(TEXTURE.gui.slot)
			SIZE=60
			ctx.fillRect(cnv.width-PLAYER.inv.length*SIZE-SIZE*0.5+i*SIZE,cnv.height-SIZE*1.5,SIZE-20,SIZE-20)
			ctx.strokeRect(cnv.width-PLAYER.inv.length*SIZE-SIZE*0.5+i*SIZE,cnv.height-SIZE*1.5,SIZE-20,SIZE-20)
			if (PLAYER.inv[i]!=-1){
				x=cnv.width-PLAYER.inv.length*SIZE-SIZE*0.5+i*SIZE+SIZE/2-10
				y=cnv.height-SIZE*1.5+SIZE/2-10
				ctx.translate(x,y)
				ctx.rotate(Math.PI/4)
				draw_gun(PLAYER.inv[i])
				ctx.rotate(-Math.PI/4)
				ctx.translate(-x,-y)
				if (PLAYER.inv[i].reloading>-1){
					ctx.fillStyle=to_rgba(TEXTURE.gui.slot_overlay)
					ctx.fillRect(cnv.width-PLAYER.inv.length*SIZE-SIZE*0.5+i*SIZE,cnv.height-SIZE*1.5+(SIZE-20)*(1-PLAYER.inv[i].reloading/100),SIZE-20,SIZE-20-(SIZE-20)*(1-PLAYER.inv[i].reloading/100))
				}
			}
			if (PLAYER.inv[i]!=-1&&PLAYER.inv[i].ammo>0){
				x=cnv.width-PLAYER.inv.length*SIZE+SIZE*0.5+i*SIZE-20
				y=cnv.height-SIZE*0.5-20
				ctx.fillStyle=to_rgba(TEXTURE.gui.small_slot_text)
				ctx.textAlign="right"
				ctx.textBaseline="middle"
				ctx.font="20px SnigletB"
				ctx.fillText(PLAYER.inv[i].ammo,x,y)
			}
		}
		if (ITEM_TEXT[1]>-1){
			a=100
			if (ITEM_TEXT[1]>125){
				a=parseInt(ITEM_TEXT[1]-125).map(0,15,100,0)
			}
			if (ITEM_TEXT[1]>=140){
				ITEM_TEXT[1]=-2
			}
			ITEM_TEXT[1]++
			x=cnv.width-PLAYER.inv.length*SIZE-SIZE*0.5+2.5*SIZE-10
			y=cnv.height-SIZE*2
			ctx.textAlign="center"
			ctx.font="25px SnigletB"
			ctx.textBaseline="middle"
			ctx.fillStyle=color(TEXTURE.gui.big_slot_text,a)
			ctx.fillText(ITEM_TEXT[0],x,y)
		}
		if (PLAYER.HP>0){
			function path(p){
				ctx.beginPath()
				if (p.length==0){return}
				ctx.moveTo(p[p.length-1].x,p[p.length-1].y)
				for (var v of p){
					ctx.lineTo(v.x,v.y)
				}
			}
			function heart(x,y,t){
				ctx.translate(x,y)
				ctx.fillStyle=to_rgba(TEXTURE.gui.heart)
				ctx.strokeStyle=to_rgba(TEXTURE.gui.heart_border)
				ctx.lineWidth=3
				if (t!=-1){
					path(GRAPHICS[t])
					ctx.fill()
				}
				ctx.stroke()
				path(GRAPHICS[2])
				ctx.stroke()
				ctx.translate(-x,-y)
			}
			x=cnv.width-PLAYER.inv.length*SIZE-SIZE*0.75
			y=cnv.height-SIZE*1.5
			v=10
			for (var i=0;i<10;i++){
				ox=0
				oy=0
				if (HEART_VELS[i]>=150&&PLAYER.HP>3){
					if (HEART_VELS[i]<155){
						oy=Math.sigmoid((HEART_VELS[i]-150).map(0,5,-10,10))*15
					}
					if (HEART_VELS[i]>=155){
						oy=Math.sigmoid((HEART_VELS[i]-155).map(0,5,10,-10))*15
					}
					if (HEART_VELS[i]>=160){
						HEART_VELS[i]=0
					}
				}
				if (PLAYER.HP<=3){
					ox=(HEART_VELS[i]%3-1)*2
					if (HEART_VELS[i]>=160){
						HEART_VELS[i]=0
					}
				}
				if (PLAYER.HP>=v){
					heart(x-19.5-i*40-ox,y+17-oy,0)
				}
				else if (PLAYER.HP>=v-0.5){
					heart(x-19.5-i*40-ox,y+17-oy,1)
				}
				else{
					heart(x-19.5-i*40-ox,y+17-oy,-1)
				}
				v--
			}
		}
		if (PLAYER.COINS!=-1){
			draw_coin(30,30)
			ctx.textAlign="left"
			ctx.font="30px SnigletB"
			ctx.textBaseline="middle"
			ctx.fillStyle=to_rgba(TEXTURE.gui.coin_text)
			ctx.fillText(PLAYER.COINS,52,33)
		}
		if (MODE==1){
			ctx.textAlign="left"
			ctx.font="40px SnigletB"
			ctx.textBaseline="middle"
			ctx.fillStyle=to_rgba(TEXTURE.gui.spectating_text)
			w=ctx.measureText("Now spectating: "+PLAYER.NAME).width
			w2=ctx.measureText("Now spectating: ").width
			ctx.fillText("Now spectating: ",cnv.width/2-w/2,50)
			ctx.fillStyle=to_rgba(TEXTURE.gui.spectating_name_text)
			ctx.fillText(PLAYER.NAME,cnv.width/2-w/2+w2,50)
		}
		if (WAIT_STATUS!=-1){
			ctx.textAlign="center"
			ctx.font="30px SnigletB"
			ctx.textBaseline="middle"
			ctx.fillStyle=to_rgba(TEXTURE.gui.wait_status_text)
			ctx.fillText(WAIT_STATUS,cnv.width/2,50)
		}
	}
	if (MENU.open==true){
		if (MENU.type=="main"){
			ctx.fillStyle=to_rgba(TEXTURE.menu.main)
			ctx.fillRect(0,0,cnv.width,cnv.height)
			ctx.strokeStyle=to_rgba(TEXTURE.settings.icon)
			ctx.lineWidth=6
			for (y=40;y<40+3*20;y+=20){
				ctx.beginPath()
				ctx.moveTo(40,y)
				ctx.lineTo(100,y)
				ctx.stroke()
			}
		}
		if (MENU.type=="pause"){
			ctx.fillStyle=to_rgba(TEXTURE.menu.pause)
			ctx.fillRect(0,0,cnv.width,cnv.height)
		}
		MENU.buttons.forEach((b)=>draw_button(b))
	}
	if (SETTINGS.off_open>-500){
		ctx.fillStyle=color(TEXTURE.settings.cover_bg,Math.abs(SETTINGS.off_open).map(500,0,0,75,true,true))
		ctx.fillRect(0,0,cnv.width,cnv.height)
		ctx.translate(SETTINGS.off_open,0)
		ctx.fillStyle=TEXTURE.settings.bg
		ctx.strokeStyle=TEXTURE.settings.border
		ctx.lineWidth=8
		ctx.beginPath()
		ctx.moveTo(500-40,cnv.height-20)
		ctx.arcTo(20,cnv.height-20,20,20,20)
		ctx.arcTo(20,20,500-20,20,20)
		ctx.arcTo(500-20,20,500-20,cnv.height-20,20)
		ctx.arcTo(500-20,cnv.height-20,20,cnv.height-20,20)
		ctx.fill()
		ctx.stroke()
		ctx.textAlign="left"
		ctx.textBaseline="middle"
		ctx.font="50px Sniglet"
		var w1=ctx.measureText("Hi, "+DATA.NAME+"!").width
		var w2=ctx.measureText("Hi, ").width
		var w3=ctx.measureText("Hi, "+DATA.NAME).width
		ctx.fillStyle=to_rgba(TEXTURE.settings.name_text)
		ctx.fillText("Hi, ",250-w1/2,59)
		ctx.fillText("!",250-w1/2+w3,59)
		ctx.fillStyle=to_rgba(TEXTURE.settings.name)
		ctx.fillText(DATA.NAME,250-w1/2+w2,59)
		ctx.translate(-SETTINGS.off_open,0)
	}
	ctx.fillStyle=to_rgba(TEXTURE.other.mouse)
	ctx.beginPath()
	ctx.arc(MOUSEPOS.x,MOUSEPOS.y,20,0,2*Math.PI)
	ctx.fill()
	requestAnimationFrame(draw)
}
function to_rgba(c){
	if (c.length==7){return c}
	return "rgba("+parseInt(c.slice(1,3),16)+","+parseInt(c.slice(3,5),16)+","+parseInt(c.slice(5,7),16)+","+parseInt(c.slice(7,9),16)/255+")"
}
function color(r,g,b,a){
	function _c(args,s1,s2,s3,s4){
		function _cmp(a,s){
			return ((s==1&&a!=undefined)||(s==0&&a==undefined))
		}
		return (_cmp(args[0],s1)==true&&_cmp(args[1],s2)==true&&_cmp(args[2],s3)==true&&_cmp(args[3],s4)==true)
	}
	function _h(v){
		if (v.toString(16).length==2){return v.toString(16)}
		if (v.toString(16).length==1){return "0"+v.toString(16)}
		return "00"
	}
	if (_c([r,g,b,a],1,1,0,0)==true&&r.toString()===r){
		a=g+0
		g=parseInt(r.substring(3,5),16)
		b=parseInt(r.substring(5,7),16)
		r=parseInt(r.substring(1,3),16)
	}
	if (_c([r,g,b,a],1,0,0,0)==true){
		if (typeof r==String){
			return r
		}
		else{
			return "#"+_h(r)+_h(r)+_h(r)
		}
	}
	if (_c([r,g,b,a],1,1,0,0)==true){
		return "rgba("+r+","+r+","+r+","+g/100+")"
	}
	if (_c([r,g,b,a],1,1,1,0)==true){
		return "#"+_h(r)+_h(g)+_h(b)
	}
	if (_c([r,g,b,a],1,1,1,1)==true){
		return "rgba("+r+","+g+","+b+","+a/100+")"
	}
	return null
}
function calc_tree_color(v){
	function lc(a,b,c){
		function l(a,b,c){
			s=Math.min(Math.max(parseInt(a*(1-c/100)+b*c/100),0),255).toString(16)
			if (s.length==1){
				return "0"+s
			}
			return s
		}
		a=[parseInt(a.substring(1,3),16),parseInt(a.substring(3,5),16),parseInt(a.substring(5,7),16)]
		b=[parseInt(b.substring(1,3),16),parseInt(b.substring(3,5),16),parseInt(b.substring(5,7),16)]
		return "#"+l(a[0],b[0],c+0)+l(a[1],b[1],c+0)+l(a[2],b[2],c+0)
	}
	return [lc(TEXTURE.world.min_tree,TEXTURE.world.max_tree,v+0),lc(TEXTURE.world.min_tree,TEXTURE.world.max_tree,v-30)]
}
function on_board(x,y,t){
	return (x>=-t&&x<=cnv.width+t&&y>=-t&&y<=cnv.height+t)
}