window.onkeydown=function(e){
	switch (e.keyCode){
		case 27:
			MENU.esc()
			SETTINGS.esc()
			break
	}
	if (PLAYER!=null){
		PLAYER.keyPress(e)
	}
}
window.onmousedown=function(e){
	MOUSEPOS={x:e.x,y:e.y}
	if (e.button==2){
		if (PLAYER!=null){
			PLAYER.start_follow()
		}
	}
	if (e.button==0){
		MOUSEDOWN=true
		MENU.update()
		SETTINGS.update()
	}
}
window.oncontextmenu=function(e){
	e.preventDefault();
	e.stopPropagation();
	e.stopImmediatePropagation();
}
window.onmousemove=function(e){
	MOUSEPOS={x:e.clientX,y:e.clientY}
}
window.onmouseup=function(e){
	MOUSEDOWN=false
	if (e.button==2){
		if (PLAYER!=null){
			PLAYER.stop_follow()
		}
	}
}
window.ontouchstart=function(e){
	MOUSEDOWN=true
	MOUSEPOS={x:e.touches[0].clientX,y:e.touches[0].clientY}
	MENU.update()
}
window.ontouchmove=function(e){
	MOUSEPOS={x:e.touches[0].clientX,y:e.touches[0].clientY}
}
window.ontouchend=function(e){
	MOUSEDOWN=false
}
window.ontouchcancel=function(e){
	MOUSEDOWN=false
}
window.onresize=function(){
	cnv.width=cnv.getBoundingClientRect().width
	cnv.height=cnv.getBoundingClientRect().height
}