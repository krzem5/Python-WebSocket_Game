class Button{
	constructor(x,y,w,h,txt,f,p){
		this.pos={x,y}
		this.size={w,h}
		this.txt=txt
		this.f=f
		this.s=null
		this.PLAY=((p||false)==true)
	}
	mousePressed(e){
		if (this.pos.x-this.size.w/2<=e.x&&this.pos.x+this.size.w/2>=e.x&&this.pos.y-this.size.h/2<=e.y&&this.pos.y+this.size.h/2>=e.y){
			this.s=SOUNDS.play("button_click",10)
			setTimeout(this.f,100)
		}
	}
}