Number.prototype.map=function(as,ae,bs,be,c,d){
	return d==true?parseInt(c==true?Math.min(Math.max((this-as)/(ae-as)*(be-bs)+bs,bs),be):(this-as)/(ae-as)*(be-bs)+bs):(c==true?Math.min(Math.max((this-as)/(ae-as)*(be-bs)+bs,bs),be):(this-as)/(ae-as)*(be-bs)+bs)
}
Number.prototype.toDegrees=function(){
	return this/(Math.PI/180)
}
Number.prototype.toRadians=function(){
	return this*(Math.PI/180)
}
Math.sigmoid=function(a){
	return 1/(1+Math.exp(-a))
}
window.requestAnimationFrame=window.requestAnimationFrame||window.mozRequestAnimationFrame||window.webkitRequestAnimationFrame||window.msRequestAnimationFrame
window.AudioContext=window.AudioContext||window.webkitAudioContext