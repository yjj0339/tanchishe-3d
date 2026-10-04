import bpy, math, os

bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene

def mat(name, color, rough=0.55, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    return m

skin = mat("Skin", (1.0, 1.0, 1.0), 0.5)
eyewhite = mat("EyeWhite", (1.0, 1.0, 1.0), 0.25)
pupil = mat("Pupil", (0.05, 0.05, 0.07), 0.2)
tongue = mat("Tongue", (0.92, 0.16, 0.22), 0.4)

def sph(name, r, loc, scale, material, seg=32, ring=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=r, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o

skull = sph("Skull", 1.0, (0, 0, 0), (1.05, 0.85, 0.95), skin)
snout = sph("Snout", 0.58, (0.78, -0.10, 0), (1.15, 0.72, 0.85), skin)

for i, z in enumerate((-0.58, 0.58)):
    eye = sph(f"Eye{i}", 0.42, (0.40, 0.48, z), (1, 1, 1), eyewhite)
    pup = sph(f"Pupil{i}", 0.185, (0.53, 0.66, z * 1.18), (1, 1, 1), pupil)
    shine = sph(f"Shine{i}", 0.055, (0.56, 0.74, z * 1.28), (1, 1, 1), eyewhite)

for i, z in enumerate((-0.15, 0.15)):
    sph(f"Nostril{i}", 0.065, (1.32, 0.10, z), (1, 0.7, 1), pupil)

bpy.ops.mesh.primitive_cube_add(size=1, location=(1.55, -0.28, 0))
t = bpy.context.active_object
t.name = "Tongue"
t.scale = (0.42, 0.045, 0.10)
t.data.materials.append(tongue)
for i, z in enumerate((-0.09, 0.09)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.0, -0.28, z))
    f = bpy.context.active_object
    f.name = f"Tip{i}"
    f.scale = (0.22, 0.045, 0.08)
    f.rotation_euler = (0, math.radians(18 * (1 if z > 0 else -1)), 0)
    f.data.materials.append(tongue)

root = bpy.data.objects.new("SnakeHeadRoot", None)
bpy.context.scene.collection.objects.link(root)
for o in bpy.context.scene.objects:
    if o.type == "MESH":
        o.parent = root

bpy.ops.object.select_all(action="DESELECT")
for o in bpy.context.scene.objects:
    if o.type == "MESH":
        o.select_set(True)
bpy.context.view_layer.objects.active = skull
bpy.ops.object.join()
bpy.context.active_object.name = "SnakeHead"
head_obj = bpy.context.active_object
head_obj.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "snake_head.glb")
bpy.ops.export_scene.gltf(filepath=os.path.abspath(out), export_format="GLB", export_apply=True, export_materials="EXPORT")

S.render.engine = "BLENDER_WORKBENCH"
S.display.shading.light = "STUDIO"
S.display.shading.color_type = "MATERIAL"
S.render.resolution_x = 800
S.render.resolution_y = 500
S.render.filepath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots", "head_front.png"))
cam = bpy.data.cameras.new("Cam")
camo = bpy.data.objects.new("Cam", cam)
bpy.context.scene.collection.objects.link(camo)
target = bpy.data.objects.new("CamTarget", None)
bpy.context.scene.collection.objects.link(target)
con = camo.constraints.new("TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"
S.camera = camo

def snap(loc):
    camo.location = loc
    bpy.context.view_layer.update()

snap((7.2, -1.2, 2.2))
bpy.ops.render.render(write_still=True)

camo.location = (1.5, -7.0, 5.5)
bpy.context.view_layer.update()
S.render.filepath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots", "head_top.png"))
bpy.ops.render.render(write_still=True)
print("HEAD_EXPORT_OK")
