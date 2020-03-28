function _socket_init(){
	window.SOCKET=null
	function join(){
		var old_r
		if (SOCKET!=null){
			NEW=SOCKET.NEW
		}
		else{
			NEW=true
		}
		SOCKET=new WebSocket("ws://192.168.178.65:8080/")
		SOCKET.NO_RECONNECT=false
		SOCKET.NEW=NEW
		SOCKET.onopen=function(){
			CONNECTED=true
			cnv.classList.add("h")
			if (this.NEW==true){
				MENU.o("main")
			}
			this.NEW=false
		}
		SOCKET.onclose=function(){
			CONNECTED=false
			cnv.classList.remove("h")
			if (this.NO_RECONNECT==false){join()}
		}
		SOCKET.onmessage=function(e){
			try{
				function p_mh(dt){
					if (dt=="-1"){
						return -1
					}
					else{
						dt.split(",").forEach(function(a,b,c){
							if (dt.length!=c.length){
								dt=Array(c.length)
							}
							dt[b]=parseInt(a)
						})
						return dt
					}
				}
				if (e.data=="null"){return}
				e={type:e.data.substring(0,2),data:e.data.substring(2)}
				_={
					ac:function(dt){
						SOCKET.send("dc")
						SOCKET.NO_RECONNECT=true
						document.body.innerHTML="<div style=\"position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:Teko;text-align:center;white-space:nowrap;user-select:none;\"><div style=\"font-size:150px;\">Already Connected</div><br><div style=\"font-size:60px\">Your IP("+dt+") is already logged into the game</div></div>"
					},
					sp:function(){
						MODE=0
						PLAYING=true
						if (PLAYER==null){
							PLAYER=new Player()
						}
						HEART_VELS=[]
						for (var i=0;i<10;i++){
							HEART_VELS.push(i*2)
						}
					},
					tp:function(dt){
						TEXTURE=decode_tex_pack(dt)
					},
					sb:function(dt){
						BOARD=decode_board(dt)
					},
					sn:function(dt){
						if (PLAYER==null||DATA.NAME==null||DATA.ID==-1){
							DATA.ID=parseInt(dt.split(":")[0])
							DATA.NAME=dt.split(":")[1]
						}
						else{
							PLAYER.ID=parseInt(dt.split(":")[0])
							PLAYER.NAME=dt.split(":")[1]
						}
					},
					sd:function(dt){
						PLAYER.PLAYERS[parseInt(dt.split(":")[0])]={id:parseInt(dt.split(":")[0]),name:dt.split(":")[1],pos:{x:parseFloat(dt.split(":")[2]),y:parseFloat(dt.split(":")[3])},fdir:parseInt(dt.split(":")[4]),mh:p_mh(dt.split(":")[5]),state:0}
						if (parseInt(dt.split(":")[0])==PLAYER.ID){
							PLAYER.NAME=dt.split(":")[1]
							PLAYER.pos.x=parseFloat(dt.split(":")[2])
							PLAYER.pos.y=parseFloat(dt.split(":")[3])
							PLAYER.fdir=parseInt(dt.split(":")[4])
							PLAYER.mh=dt.split(":")[5]
							PLAYER.STATE=0
						}
					},
					jn:function(dt){
						console.log(PLAYER.PLAYERS[parseInt(dt)].name+" joined the game")
					},
					ws:function(dt){
						if (dt=="-1"){
							WAIT_STATUS=-1
						}
						else{
							WAIT_STATUS=dt
						}
					},
					dp:function(dt){
						if (PLAYING==false){
							DROP_PLANE=null
							return
						}
						dt=dt.split(":")
						dt.forEach(function(a,b,c){
							c[b]=parseInt(a)
						})
						var DIR=-1
						if (DROP_PLANE!=null){
							DIR=DROP_PLANE.d
							X2=DROP_PLANE.x2
							Y2=DROP_PLANE.y2
						}
						else{
							DIR=Math.atan2(dt[5]-dt[3],dt[4]-dt[2])
							X2=20*Math.cos(DIR)
							Y2=20*Math.sin(DIR)
						}
						DROP_PLANE={x:dt[0],y:dt[1],sx:dt[2],sy:dt[3],ex:dt[4],ey:dt[5],d:DIR,x2:X2,y2:Y2}
						for (var id of Object.keys(PLAYER.PLAYERS)){
							if (PLAYER.PLAYERS[id].state==2){continue}
							PLAYER.PLAYERS[id].pos.x=dt[0]
							PLAYER.PLAYERS[id].pos.y=dt[1]
							if (id==PLAYER.ID){
								PLAYER.pos.x=dt[0]
								PLAYER.pos.y=dt[1]
							}
						}
					},
					np:function(dt){
						DROP_PLANE=null
					},
					nt:function(dt){
						console.log("Name successfully changed to "+dt)
						PLAYER.NAME=dt
					},
					nf:function(dt){
						console.log("Couldn't change name to "+dt.split(":")[0]+" (REASON: "+["Name the same","Name too short","Name too long","Name already taken"][parseInt(dt.split(":")[1])]+")")
					},
					nc:function(dt){
						PLAYER.PLAYERS[parseInt(dt.split(":")[0])].name=dt.split(":")[1]
					},
					mh:function(dt){
						dt=dt.split(":")
						PLAYER.PLAYERS[parseInt(dt[0])].mh=p_mh(dt[1])
					},
					iv:function(dt){
						PLAYER.set_inv(dt)
					},
					mv:function(dt){
						PLAYER.PLAYERS[parseInt(dt.split(":")[0])].pos.x=parseFloat(dt.split(":")[1])
						PLAYER.PLAYERS[parseInt(dt.split(":")[0])].pos.y=parseFloat(dt.split(":")[2])
						PLAYER.PLAYERS[parseInt(dt.split(":")[0])].fdir=parseInt(dt.split(":")[3])
						PLAYER.PLAYERS[parseInt(dt.split(":")[0])].state=2
						if (parseInt(dt.split(":")[0])==PLAYER.ID){
							PLAYER.pos.x=parseFloat(dt.split(":")[1])
							PLAYER.pos.y=parseFloat(dt.split(":")[2])
							PLAYER.fdir=parseInt(dt.split(":")[3])
							PLAYER.STATE=2
						}
					},
					bl:function(dt){
						BULLETS=[]
						if (dt!=""){
							for (var b of dt.split(":")){
								BULLETS.push({"x":parseInt(b.split(",")[0]),"y":parseInt(b.split(",")[1]),"dir":parseInt(b.split(",")[2])})
							}
						}
					},
					hp:function(dt){
						PLAYER.HP=parseInt(dt)/2
					},
					it:function(dt){
						dt=dt.split(":")
						data=null
						if (parseInt(dt[4])==0){
							data=p_mh(dt[5])
						}
						ITEMS[parseInt(dt[0])]={x:parseInt(dt[1]),y:parseInt(dt[2]),dir:parseInt(dt[3]),type:parseInt(dt[4]),data:data}
					},
					cd:function(dt){
						if (PLAYER.COINS==-1&&MODE==0){
							for (var id of Object.keys(PLAYER.PLAYERS)){
								PLAYER.PLAYERS[id].state=0
								if (id==PLAYER.ID){
									PLAYER.STATE=0
								}
							}
						}
						PLAYER.COINS=parseInt(dt)
					},
					ri:function(dt){
						ITEMS[parseInt(dt)]=null
						delete ITEMS[parseInt(dt)]
					},
					rc:function(dt){
						LOOT_CHESTS[parseInt(dt)]=null
						delete LOOT_CHESTS[parseInt(dt)]
					},
					rp:function(dt){
						if (parseInt(dt)==PLAYER.ID){
							MODE=1
						}
						PLAYER.PLAYERS[parseInt(dt)]=null
						delete PLAYER.PLAYERS[parseInt(dt)]
					},
					lv:function(dt){
						console.log(PLAYER.PLAYERS[parseInt(dt)].name+" left the game")
					},
					kk:function(dt){
						console.log(PLAYER.PLAYERS[parseInt(dt)].name+" got kicked from the server")
					},
					pk:function(dt){
						dt=dt||"Manual kick"
						SOCKET.send("dc")
						SOCKET.NO_RECONNECT=true
						document.body.innerHTML="<div style=\"position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:Teko;text-align:center;white-space:nowrap;user-select:none;\"><div style=\"font-size:150px;\">Kicked</div><br><div style=\"font-size:60px\">Reason - "+dt+"</div></div>"
					},
					bn:function(dt){
						date=new Date(parseInt(dt.split(":")[0])*1000)
						date=date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear()+" "+parseInt(date.getHours())%12+":"+date.getMinutes()+(parseInt(date.getHours())<13?"am":"pm")
						dt.split(":")[1]=dt.split(":")[1]||"Manual ban"
						SOCKET.send("dc")
						SOCKET.NO_RECONNECT=true
						document.body.innerHTML="<div style=\"position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:Teko;text-align:center;white-space:nowrap;user-select:none;\"><div style=\"font-size:150px;\">Banned</div><br><div style=\"font-size:80px\">Until "+date+"</div><br><div style=\"font-size:60px\">Reason - "+dt.split(":")[1]+"</div></div>"
					},
					sc:function(dt){
						dt=dt||"Manual shutdown"
						SOCKET.send("dc")
						SOCKET.NO_RECONNECT=true
						document.body.innerHTML="<div style=\"position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:Teko;text-align:center;white-space:nowrap;user-select:none;\"><div style=\"font-size:150px;\">Server Closed</div><br><div style=\"font-size:60px\">Reason - "+dt+"</div></div>"
					}
				}[e.type](e.data)
			}
			catch (e){
				console.warn(e)
			}
		}
		SOCKET.onerror=function(e){
			e.stopImmediatePropagation()
			e.stopPropagation()
			e.preventDefault()
			console.clear()
		}
	}
	join()
}