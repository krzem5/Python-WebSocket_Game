function decode_board(s){
	function decode_ground_path(s){
		gp=[]
		for (var p of s.split(":")){
			gp.push({"x":parseInt(p.split(",")[0]),"y":parseInt(p.split(",")[1])})
		}
		return gp
	}
	function decode_island(s){
		function decode_island_path(s){
			p=[]
			for (var v of s.split(",")){
				p.push({"x":parseInt(v.split(".")[0]),"y":parseInt(v.split(".")[1])})
			}
			return p
		}
		if (s=="-1"){return null}
		i={"start":{},"end":{}}
		s=s.split(":")
		i.type=parseInt(s[0])
		i.start.x=parseInt(s[1].split(",")[0])
		i.start.y=parseInt(s[1].split(",")[1])
		i.end.x=parseInt(s[2].split(",")[0])
		i.end.y=parseInt(s[2].split(",")[1])
		i.w_path=decode_island_path(s[3])
		i.path=decode_island_path(s[4])
		return i
	}
	function decode_bridges(s){
		if (s=="-1"){return []}
		br=[]
		for (var b of s.split(":")){
			cb=[]
			for (p of b.split(",")){
				cb.push({"x":parseInt(p.split(".")[0]),"y":parseInt(p.split(".")[1])})
			}
			br.push(cb)
		}
		return br
	}
	function decode_paths(s){
		if (s==""){
			return []
		}
		ps=[]
		for (var p of s.split(":")){
			cp=[]
			for (v of p.split(",")){
				cp.push({"x":parseInt(v.split(".")[0]),"y":parseInt(v.split(".")[1])})
			}
			ps.push(cp)
		}
		return ps
	}
	function decode_trees(s){
		if (s==""){
			return []
		}
		ts=[]
		for (var t of s.split(":")){ 
			ct={}
			ct.x=parseInt(t.split(",")[0])
			ct.y=parseInt(t.split(",")[1])
			ct.r=parseInt(t.split(",")[2])
			ct.c=parseInt(t.split(",")[3])
			ct.p=[]
			for (var v of t.split(",")[4].split(".")){
				ct.p.push({"x":parseInt(v.split("/")[0]),"y":parseInt(v.split("/")[1])})
			}
			ts.push(ct)
		}
		return ts
	}
	function decode_loot_chests(s){
		if (s==""){
			return []
		}
		lc={}
		i=0
		for (var c of s.split(":")){
			lc[i]={"x":parseInt(c.split(",")[0]),"y":parseInt(c.split(",")[1])}
			i++
		}
		return lc
	}
	function decode_graphics(s){
		gs=[]
		for (var g of s.split(":")){
			cg=[]
			for (var p of g.split(",")){
				cg.push({"x":parseFloat(p.split("/")[0]),"y":parseFloat(p.split("/")[1])})
			}
			gs.push(cg)
		}
		return gs
	}
	b={}
	s=s.split(";")
	b.w=BOARD_WIDTH=parseInt(s[0].split(":")[0])
	b.h=BOARD_HEIGHT=parseInt(s[0].split(":")[1])
	b.ground=GROUND_PATH=decode_ground_path(s[1])
	b.island=ISLAND=decode_island(s[2])
	b.bridges=BRIDGES=decode_bridges(s[3])
	b.paths=PATHS=decode_paths(s[4])
	b.trees=TREES=decode_trees(s[5])
	b.loot_chests=LOOT_CHESTS=decode_loot_chests(s[6])
	b.graphics=GRAPHICS=decode_graphics(s[7])
	return b
}
function decode_tex_pack(s){
	tp={}
	for (var g of s.split(";")){
		gk=g.split(":")[0]
		tp[gk]={}
		for (var sg of g.split(":")[1].split(",")){
			tp[gk][sg.split("/")[0]]=sg.split("/")[1]
		}
	}
	return tp
}