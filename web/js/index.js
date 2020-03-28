function setup(){
	wr=document.getElementsByClassName("wr")[0]
	cnv=document.getElementsByClassName("mainCnv")[0]
	cnv.width=cnv.getBoundingClientRect().width
	cnv.height=cnv.getBoundingClientRect().height
	ctx=cnv.getContext("2d")
	audioCtx=new AudioContext()
	SOUNDS.audioCtx=audioCtx
	_socket_init()
	requestAnimationFrame(draw)
}