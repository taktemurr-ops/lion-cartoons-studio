import bpy, math
from mathutils import Vector
from pathlib import Path
p=Path(__file__).resolve().parent/'output'
p.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine = "CYCLES"
s.cycles.device = "CPU"
s.cycles.samples = 4
s.frame_start=1; s.frame_end=24; s.render.fps=24
s.render.resolution_x=320; s.render.resolution_y=180
s.render.image_settings.file_format='FFMPEG'
s.render.ffmpeg.format='MPEG4'; s.render.ffmpeg.codec='H264'
s.render.filepath=str(p/'scene02.mp4')
def mat(name,color):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); return m
gold=mat('Leo gold',(.95,.49,.07))
brown=mat('Mane',(.5,.22,.04))
white=mat('Lila white',(.97,.93,.87))
green=mat('Garden green',(.16,.53,.25))
pink=mat('Lila pink',(.91,.29,.48))
black=mat('Eyes',(.02,.02,.03))
def ball(name,pos,scale,material,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=pos)
 o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material)
 if parent: o.parent=parent
 return o
def control(name,pos):
 o=bpy.data.objects.new(name,None); bpy.context.collection.objects.link(o); o.location=pos; return o
def movement(ob,points):
 for frame,pos in points:
  ob.location=pos;ob.keyframe_insert(data_path='location',frame=frame)
bpy.ops.mesh.primitive_cube_add(size=2,location=(0,0,-.35))
bpy.context.object.scale=(9,6,.2)
bpy.context.object.data.materials.append(green)
leo=control('Leo control',(-3,0,0))
lila=control('Lila control',(2,0,0))
ball('Leo body',(0,0,.9),(.48,.38,.65),gold,leo)
ball('Leo mane',(0,-.03,1.82),(.65,.49,.63),brown,leo)
ball('Leo face',(0,-.38,1.82),(.51,.29,.48),gold,leo)
ball('Lila body',(0,0,.78),(.33,.30,.58),white,lila)
ball('Lila face',(0,-.07,1.48),(.44,.35,.43),white,lila)
for sign in (-1,1):
 ball('Leo eye',(.19*sign,-.65,1.93),(.08,.05,.11),black,leo)
 ball('Lila eye',(.17*sign,-.43,1.58),(.085,.05,.12),black,lila)
 ball('Lila ear',(.2*sign,0,2.06),(.13,.12,.52),white,lila)
 ball('Lila inner ear',(.2*sign,-.13,2.06),(.06,.05,.36),pink,lila)
seed=ball('Flying seed',(-1,-.4,1),(.2,.13,.15),brown)
movement(seed,[(1,(-1,-.4,1)),(65,(.2,-.4,2.5)),(135,(2.4,-.4,3)),(190,(3.7,-.4,1.4)),(240,(4,-.4,.3))])
movement(leo,[(1,(-3,0,0)),(80,(-2,0,0)),(160,(-.8,0,.18)),(240,(0,0,0))])
movement(lila,[(1,(2,0,0)),(70,(2,0,.1)),(125,(2.3,0,.4)),(180,(3,0,0)),(240,(3.5,0,0))])
bpy.ops.object.camera_add(location=(0,-12,4.8))
cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,1.4))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=10;s.camera=cam
movement(cam,[(1,(0,-12,4.8)),(140,(.5,-12,4.8)),(240,(1,-12,4.8))])
bpy.ops.object.light_add(type='AREA',location=(-3,-4,8))
bpy.context.object.data.energy=1600
bpy.context.object.data.size=6
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene02.blend'))
bpy.ops.render.render(animation=True)
