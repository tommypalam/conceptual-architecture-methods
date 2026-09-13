"""Create original PARIA diorama assets inside Blender and export glTF binaries.

Execute through the connected Blender addon with PARIA_ROOT set to the repo.
Only creates new named scenes. Refuses to overwrite prior generated assets.
"""
import bpy
import math
import json
import hashlib
from pathlib import Path
from mathutils import Vector

ROOT = Path(PARIA_ROOT)
OUT = ROOT / "viewer" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
blend_path = ROOT / "output" / "paria_dioramas.blend"
if blend_path.exists() or (OUT / "manifest.json").exists() or any((OUT / f"{name}.glb").exists() for name in ("council", "boardroom", "laboratory", "agent")):
    raise RuntimeError("Assets already exist; use a new reviewed output designation")


def material(name, color, metallic=0, roughness=.5):
    m = bpy.data.materials.new("PARIA_" + name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return m


porcelain = material("Porcelain", (.88, .92, .94), .05, .3)
stone = material("Stone", (.58, .69, .72), 0, .75)
trim = material("Edge", (.20, .34, .40), .3, .4)
oak = material("Oak", (.55, .33, .15), 0, .55)
oak_light = material("Pale_oak", (.77, .60, .37), 0, .55)
leaf = material("Leaves", (.18, .37, .29), 0, .7)
leaf_light = material("Leaves_light", (.32, .52, .36), 0, .7)
ink = material("Visor", (.025, .065, .09), .35, .23)
screen = material("Display", (.20, .50, .60), .1, .3)
brass = material("Brass", (.62, .43, .18), .6, .3)
carpet = material("Carpet", (.34, .51, .55), 0, 1)


def finish(obj, name, mat):
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def box(name, loc, scale, mat, bevel=.05):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    finish(obj, name, mat)
    if bevel:
        mod = obj.modifiers.new("Soft_edges", "BEVEL")
        mod.width = bevel
        mod.segments = 3
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.modifiers.new("Weighted_normals", "WEIGHTED_NORMAL")
    return obj


def cylinder(name, loc, radius, depth, mat, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = finish(bpy.context.object, name, mat)
    bevel = obj.modifiers.new("Edge", "BEVEL")
    bevel.width = .035
    bevel.segments = 2
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    for poly in obj.data.polygons:
        poly.use_smooth = abs(poly.normal.z) < .9
    return obj


def sphere(name, loc, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=1, location=loc)
    obj = finish(bpy.context.object, name, mat)
    obj.scale = scale
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def plant(x, y, size=1):
    cylinder("Planter", (x, y, .35), .30 * size, .65, porcelain)
    cylinder("Stem", (x, y, .98), .04, 1.0, oak, 12)
    for i in range(7):
        a = i * 2.4
        obj = sphere("Leaf", (x + math.cos(a)*.26*size, y + math.sin(a)*.26*size, .9 + i*.12), (.16*size, .32*size, .12), leaf if i%2 else leaf_light)
        obj.rotation_euler = (.3, .4, a)


def base(name, wall_material=porcelain):
    scene = bpy.data.scenes.new("PARIA_" + name)
    bpy.context.window.scene = scene
    box("Foundation", (0, 0, -.38), (9.6, 8.4, .55), trim, .22)
    box("Floor", (0, 0, -.10), (9.4, 8.2, .24), stone, .12)
    for i in range(-4, 5):
        box("Floor_joint", (i, 0, .028), (.012, 8.0, .005), trim, 0)
    box("Back_wall", (0, 4.02, 1.10), (9.35, .18, 2.2), wall_material, .06)
    box("Left_wall", (-4.55, 1.65, .72), (.18, 4.85, 1.44), wall_material, .05)
    box("Back_cap", (0, 4.02, 2.24), (9.5, .30, .10), trim)
    box("Entry_step", (0, -4.35, -.28), (2.8, .65, .22), porcelain, .06)
    box("Entry_step_lower", (0, -4.65, -.46), (3.2, .55, .15), stone, .06)
    plant(-3.9, 3.25)
    plant(3.9, 3.25, .85)
    return scene


def export(name):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(OUT / f"{name}.glb"), export_format="GLB", use_selection=True, use_active_scene=True,
                              export_apply=True, export_materials="EXPORT", export_cameras=False,
                              export_lights=False, export_animations=False)


# Council chamber: radial furnishings with five evenly spaced places.
council = base("Council")
cylinder("Council_rug", (0, 0, .045), 3.5, .035, carpet, 64)
cylinder("Table_column", (0, 0, .50), .62, 1.0, oak)
cylinder("Council_table", (0, 0, 1.12), 1.62, .16, oak_light, 64)
cylinder("Table_inset", (0, 0, 1.21), 1.28, .015, oak, 64)
for i in range(5):
    a = i * math.tau / 5
    x, y = math.sin(a)*2.65, -math.cos(a)*2.65
    cylinder("Seat", (x, y, .48), .43, .13, porcelain)
    cylinder("Seat_stem", (x, y, .24), .12, .44, brass)
    cylinder("Seat_foot", (x, y, .05), .32, .05, trim)
for x in (-2.4, 0, 2.4):
    box("Wall_panel", (x, 3.88, 1.25), (1.8, .12, 1.2), oak_light)
    for j in range(5):
        box("Acoustic_rib", (x-.65+j*.32, 3.78, 1.25), (.08, .12, 1.1), oak)
export("council")

# Boardroom: six places, shared plan display, credenza.
board = base("Boardroom")
box("Board_rug", (0, 0, .035), (7.2, 5.4, .025), carpet, .25)
box("Board_table", (0, 0, 1.12), (4.1, 1.95, .20), oak, .25)
for x in (-1.4, 1.4):
    box("Table_leg", (x, 0, .55), (.18, 1.3, 1.05), brass)
for x, y in [(-2.8,0),(-1.35,-1.8),(1.35,-1.8),(2.8,0),(1.35,1.8),(-1.35,1.8)]:
    cylinder("Chair_base", (x, y, .07), .36, .1, trim)
    cylinder("Chair_stem", (x, y, .3), .1, .5, brass)
    box("Chair", (x, y, .55), (.7,.68,.16), porcelain, .1)
box("Plan_display_frame", (0, 3.82, 1.45), (3.5,.12,1.35), trim)
box("Plan_display", (0, 3.74, 1.45), (3.2,.04,1.10), screen, .03)
for i, width in enumerate((2.3,1.7,2.0)):
    box("Plan_line", (-.3,3.70,1.74-i*.25), (width,.02,.055), porcelain, .01)
box("Credenza", (2.5, 3.28, .48), (1.8, .8, .9), oak_light)
for x in (2.05,2.65):
    box("Cabinet_handle", (x, 2.85, .55), (.3,.03,.04), brass, .01)
export("boardroom")

# Laboratory: evidence bench, cabinets, storage and microscope-like instruments.
lab = base("Laboratory")
box("Lab_table", (0,0,1.10), (3.0,2.1,.18), porcelain,.12)
for x in (-1.1,1.1):
    for y in (-.65,.65):
        cylinder("Bench_leg",(x,y,.55),.06,1.05,trim,12)
for x,y in [(0,-2.5),(2.5,0),(0,2.5),(-2.5,0)]:
    cylinder("Lab_stool",(x,y,.51),.35,.12,screen)
    cylinder("Stool_leg",(x,y,.25),.09,.5,trim)
box("Back_bench",(0,3.35,.58),(5.0,.85,1.15),porcelain)
box("Back_worktop",(0,3.35,1.20),(5.15,.95,.10),trim)
for x in (-1.8,-.6,.6,1.8):
    box("Drawer",(x,2.89,.65),(.95,.04,.65),stone,.04)
    box("Drawer_pull",(x,2.84,.8),(.35,.03,.045),brass,.01)
for x in (-1.8,-1.45,-1.1):
    cylinder("Sample_vial",(x,3.35,1.44),.085,.37,screen,16)
    cylinder("Vial_cap",(x,3.35,1.65),.09,.06,porcelain,16)
box("Instrument_base",(1.5,3.3,1.3),(.65,.6,.12),trim)
box("Instrument_arm",(1.6,3.4,1.63),(.12,.16,.60),porcelain)
scope=cylinder("Instrument_lens",(1.45,3.23,1.89),.13,.45,trim,20)
scope.rotation_euler=(.5,0,0)
box("Information_board",(0,3.88,1.8),(1.6,.05,.42),screen)
export("laboratory")

# A neutral ceramic agent. Orientation: faces -Y in Blender, +Z after glTF export.
agent_scene = bpy.data.scenes.new("PARIA_Agent")
bpy.context.window.scene = agent_scene
sphere("Agent_body",(0,0,.88),(.28,.22,.37),porcelain)
sphere("Agent_head",(0,0,1.43),(.34,.29,.32),porcelain)
sphere("Agent_visor",(0,-.255,1.44),(.26,.065,.14),ink)
for x in (-.10,.10):
    sphere("Agent_eye",(x,-.315,1.47),(.033,.018,.035),screen)
    sphere("Agent_foot",(x,-.12,.23),(.095,.19,.09),trim)
    cylinder("Agent_leg",(x,0,.43),.075,.34,porcelain,16)
for x in (-.34,.34):
    arm=sphere("Agent_arm",(x,0,.88),(.09,.10,.25),porcelain)
    arm.rotation_euler[1]= .18 if x>0 else -.18
cylinder("Agent_neck",(0,0,1.18),.12,.16,brass,20)
export("agent")
bpy.context.window.scene = council
blend_path.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
manifest = {"created_with": bpy.app.version_string, "design": "Original procedural PARIA dioramas",
            "files": {p.name: {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in sorted(OUT.glob("*.glb"))},
            "illustrative_only": True, "external_assets": False}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest))
