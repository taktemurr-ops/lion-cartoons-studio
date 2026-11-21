"""Lion Cartoons scene 03: rig-control motion test, Blender 5, 72 frames."""
import bpy
from pathlib import Path
from mathutils import Vector
O=Path(__file__).resolve().parent/"output";O.mkdir(exist_ok=True)
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine="CYCLES";s.cycles.device="CPU";s.cycles.samples=8
s.frame_start=1;s.frame_end=72;s.render.fps=24
s.render.resolution_x=480;s.render.resolution_y=270
s.render.image_settings.file_format="PNG";s.render.filepath=str(O/"scene03_frame_")
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True
 m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*c,1);return m
yellow=mat("Leo fur",(.94,.49,.08));mane=mat("Mane",(.53,.24,.07))
white=mat("Lila fur",(.93,.90,.86));pink=mat("Lila ears",(.94,.33,.52))
black=mat("Eyes",(.03,.02,.03));green=mat("Grass",(.20,.52,.22))
soil=mat("Seed",(.45,.26,.12));teal=mat("Scarf",(.05,.60,.72))
def orb(name,loc,size,m,par=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=loc)
 o=bpy.context.object;o.name=name;o.scale=size;o.data.materials.append(m)
 if par:o.parent=par
 return o
def pivot(name,loc,par=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc
 if par:o.parent=par
 return o
def keys(o,track,k):
 for f,v in k:
  if track=="location":o.location=v
  elif track=="rotation_euler":o.rotation_euler[1]=v
  else:o.scale=v
  o.keyframe_insert(data_path=track,frame=f)
bpy.ops.mesh.primitive_cube_add(size=2,location=(0,0,-.35))
bpy.context.object.scale=(8,7,.18);bpy.context.object.data.materials.append(green)
leo=pivot("Leo root",(-2,0,0))
orb("Leo torso",(0,0,.88),(.45,.37,.58),yellow,leo)
head=pivot("Leo head",(0,0,1.55),leo)
orb("Mane",(0,0,.12),(.64,.43,.59),mane,head)
orb("Face",(0,-.37,.12),(.49,.27,.45),yellow,head)
orb("Muzzle",(0,-.62,-.10),(.3,.14,.17),white,head)
orb("Nose",(0,-.76,-.05),(.09,.06,.08),black,head)
for sign in (-1,1):
 orb("Leo eye",(.2*sign,-.61,.27),(.09,.06,.12),black,head)
 orb("Leo ear",(.47*sign,0,.5),(.17,.13,.18),yellow,head)
 orb("Leo foot",(.23*sign,-.15,.20),(.18,.20,.20),yellow,leo)
arm=pivot("Leo waving arm",(.50,-.02,1.13),leo)
orb("Leo arm",(.1,-.12,-.2),(.16,.2,.35),yellow,arm)
orb("Scarf",(0,-.25,1.20),(.43,.14,.11),teal,leo)
lila=pivot("Lila root",(1.75,0,0))
orb("Lila torso",(0,0,.75),(.34,.31,.5),white,lila)
face=pivot("Lila head",(0,0,1.42),lila)
orb("Face",(0,-.10,0),(.43,.35,.42),white,face)
orb("Nose",(0,-.48,-.09),(.08,.06,.06),pink,face)
for sign in (-1,1):
 orb("Eye",(.16*sign,-.41,.12),(.09,.055,.11),black,face)
 orb("Ear",(.20*sign,-.02,.62),(.13,.12,.48),white,face)
 orb("Inner ear",(.20*sign,-.15,.62),(.06,.04,.32),pink,face)
 orb("Foot",(.18*sign,-.1,.15),(.16,.20,.14),white,lila)
seed=orb("Flying seed",(-1,-.45,1.35),(.15,.12,.16),soil)
sprout=pivot("Seedling",(2.75,-.45,0))
orb("Sprout stem",(0,0,.22),(.035,.04,.25),green,sprout)
orb("Sprout leaf",(.15,0,.37),(.2,.05,.10),green,sprout)
keys(leo,"location",[(1,(-2,0,0)),(30,(-1.75,0,.08)),(52,(-1.7,0,0)),(72,(-1.75,0,0))])
keys(head,"rotation_euler",[(1,0),(20,-.1),(43,.15),(72,0)])
keys(arm,"rotation_euler",[(1,0),(24,-.4),(42,-1.0),(58,-.3),(72,0)])
keys(lila,"location",[(1,(1.75,0,0)),(28,(1.75,0,.17)),(43,(1.75,0,0)),(59,(1.9,0,.23)),(72,(1.9,0,0))])
keys(face,"rotation_euler",[(1,0),(30,.15),(50,-.1),(72,0)])
keys(seed,"location",[(1,(-1,-.45,1.35)),(25,(0,-.45,2.35)),(45,(1.6,-.45,2.1)),(68,(2.75,-.45,.15)),(72,(2.75,-.45,.15))])
keys(sprout,"scale",[(1,(.001,.001,.001)),(63,(.001,.001,.001)),(72,(1,1,1))])
bpy.ops.object.camera_add(location=(0,-11,4.2));c=bpy.context.object
c.rotation_euler=(Vector((0,0,1.25))-c.location).to_track_quat("-Z","Y").to_euler()
c.data.type="ORTHO";c.data.ortho_scale=7;s.camera=c
bpy.ops.object.light_add(type="AREA",location=(-3,-5,8))
bpy.context.object.data.energy=1600;bpy.context.object.data.size=5
w=s.world;w.use_nodes=True
w.node_tree.nodes["Background"].inputs["Color"].default_value=(.50,.75,1,1)
bpy.ops.wm.save_as_mainfile(filepath=str(O/"scene03.blend"))
bpy.ops.render.render(animation=True)
