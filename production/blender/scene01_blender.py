"""Lion Cartoons original 3D moving proof-of-concept. Blender 3.6+/4.x, 5 seconds, silent."""
import bpy, math
from pathlib import Path
from mathutils import Vector
out = Path(__file__).resolve().parent / "output"
out.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
s = bpy.context.scene
s.render.engine = "CYCLES"\ns.cycles.device = "CPU"\ns.cycles.samples = 4
s.frame_start, s.frame_end, s.render.fps = 1, 24, 24
s.render.resolution_x, s.render.resolution_y = 320, 180
s.render.resolution_percentage = 100
s.render.image_settings.file_format = "FFMPEG"
s.render.ffmpeg.format = "MPEG4"
s.render.ffmpeg.codec = "H264"
s.render.filepath = str(out / "scene01_preview.mp4")
def material(name, col):
    m=bpy.data.materials.new(name);m.diffuse_color=(*col,1)
    m.use_nodes=True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*col,1)
    return m
gold=material("Leo gold",(0.96,.50,.09)); mane=material("Mane",(.58,.25,.04))
cream=material("Cream",(.94,.75,.52)); white=material("Lila",(.95,.92,.88))
pink=material("Pink",(.98,.43,.56)); black=material("Eyes",(.025,.024,.04))
green=material("Garden",(.16,.50,.24)); soil=material("Soil",(.38,.21,.11))
sky=material("Blue scarf",(.04,.62,.78)); brass=material("Seed launcher",(.72,.49,.19))
def ball(name, pos, scale, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=pos)
    o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mat)
    if parent:o.parent=parent
    return o
def cylinder(name,pos,r,d,mat,rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=d,location=pos)
    o=bpy.context.object;o.name=name;o.data.materials.append(mat)
    if rot:o.rotation_euler=rot
    return o
def ctrl(name,pos):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=pos
    return o
def animate(o,points):
    for f,p in points:o.location=p;o.keyframe_insert(data_path="location",frame=f)
cylinder("Grass",(0,0,-.3),12,.5,green)
for i in range(20):
    x=-6+(i%10)*1.2;y=2+(i//10)*2.1
    cylinder("Tree trunk",(x,y,.7),.12,1.4,soil)
    ball("Tree crown",(x,y,1.65),(.65,.6,.62),green)
for i in range(15):
    x=-5+(i%5)*.9;y=-2+(i//5)*.9
    ball("Garden bed",(x,y,0),(.36,.27,.07),soil)
leo=ctrl("Leo_CTRL",(-3,-.3,0))
for name,pos,scale,mat in [
    ("Leo body",(0,0,.9),(.5,.4,.65),gold),
    ("Leo mane",(0,0,1.85),(.68,.52,.67),mane),
    ("Leo face",(0,-.4,1.85),(.51,.26,.48),gold),
    ("Leo muzzle",(0,-.63,1.55),(.3,.16,.16),cream),
    ("Leo nose",(0,-.79,1.61),(.09,.07,.07),black),
    ("Leo scarf",(0,-.25,1.28),(.51,.32,.12),sky)]:
    ball(name,pos,scale,mat,leo)
for sign in [-1,1]:
    for name,pos,scale,mat in [
        ("Leo ear",(.5*sign,0,2.36),(.18,.15,.18),gold),
        ("Leo eye white",(.2*sign,-.63,1.97),(.13,.08,.16),white),
        ("Leo pupil",(.2*sign,-.70,1.98),(.055,.045,.085),black),
        ("Leo arm",(.54*sign,-.02,.98),(.17,.19,.40),gold),
        ("Leo foot",(.27*sign,-.16,.22),(.21,.28,.19),gold)]:
        ball(name,pos,scale,mat,leo)
lila=ctrl("Lila_CTRL",(2,-.4,0))
for name,pos,scale,mat in [
    ("Lila body",(0,0,.65),(.35,.3,.55),white),
    ("Lila head",(0,-.06,1.4),(.45,.37,.42),white),
    ("Lila nose",(0,-.46,1.32),(.075,.07,.06),pink)]:
    ball(name,pos,scale,mat,lila)
for sign in [-1,1]:
    for name,pos,scale,mat in [
        ("Lila ear",(.2*sign,0,2.0),(.14,.14,.60),white),
        ("Lila inner ear",(.2*sign,-.13,2.02),(.065,.05,.45),pink),
        ("Lila eye",(.16*sign,-.41,1.51),(.09,.055,.13),black),
        ("Lila arm",(.34*sign,-.03,.74),(.12,.15,.32),white),
        ("Lila foot",(.2*sign,-.17,.16),(.17,.23,.14),white)]:
        ball(name,pos,scale,mat,lila)
cylinder("Launcher base",(-.2,-.2,.3),.42,.22,brass)
cylinder("Launcher stem",(-.2,-.2,.8),.10,.9,brass)
cylinder("Launcher barrel",(-.2,-.2,1.35),.15,.9,brass,(0,math.pi/2,0))
seed=ball("Seed",(.3,-.2,1.35),(.14,.11,.14),soil)
animate(leo,[(1,(-3,-.3,0)),(35,(-1.9,-.3,0)),(60,(-1.8,-.3,.1)),(90,(-2.2,-.3,0)),(120,(-2.2,-.3,0))])
animate(lila,[(1,(2,-.4,0)),(40,(2,-.4,0)),(60,(2,-.4,.42)),(78,(2,-.4,0)),(120,(2,-.4,0))])
animate(seed,[(1,(.3,-.2,1.35)),(55,(.3,-.2,1.35)),(76,(1.4,-.2,2.5)),(92,(2.8,-.2,2.0)),(115,(3.3,-.2,.15)),(120,(3.3,-.2,.15))])
bpy.ops.object.camera_add(location=(.3,-12,4.5))
camera=bpy.context.object
direction=Vector((0,0,1.2))-camera.location
camera.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()
camera.data.type="ORTHO";camera.data.ortho_scale=9.5;s.camera=camera
animate(camera,[(1,(.3,-12,4.5)),(60,(.6,-11.5,4.2)),(120,(.3,-12,4.5))])
bpy.ops.object.light_add(type="AREA",location=(-3,-4,9))
light=bpy.context.object;light.data.energy=1400;light.data.size=6
world=bpy.data.worlds.new("Morning") if not s.world else s.world
s.world=world;world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.55,.75,1,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.8
bpy.ops.wm.save_as_mainfile(filepath=str(out/"scene01.blend"))
bpy.ops.render.render(animation=True)
print("RENDER_FINISHED",s.render.filepath)
