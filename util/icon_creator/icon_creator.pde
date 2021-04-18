int NOMOVE_CIRCLE_RADIUS;
PGraphics logo;



void setup(){
	size(120,120);
	NOMOVE_CIRCLE_RADIUS=width/2;
	logo=createGraphics(width,height);
}



void draw(){
	background(#00ff00);
	logo.beginDraw();
	logo.fill(#ffd296);
	logo.stroke(#0a0a0a);
	logo.strokeWeight(NOMOVE_CIRCLE_RADIUS*0.1);
	logo.translate(width/2,height/2);
	logo.rotate(PI/4);
	logo.ellipseMode(CENTER);
	logo.circle(NOMOVE_CIRCLE_RADIUS*0.6,-NOMOVE_CIRCLE_RADIUS*0.4,NOMOVE_CIRCLE_RADIUS*0.3*2);
	logo.circle(-NOMOVE_CIRCLE_RADIUS*0.6,-NOMOVE_CIRCLE_RADIUS*0.4,NOMOVE_CIRCLE_RADIUS*0.3*2);
	logo.circle(0,0,NOMOVE_CIRCLE_RADIUS*0.6*2);
	logo.endDraw();
	image(logo,0,0);
	logo.save("icon.png");
	logo.save("../../web/icon/icon.png");
	noLoop();
}
