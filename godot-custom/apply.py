#!/usr/bin/env python3
"""apply.py <godot-dir>

BlockComet Engine = Godot (MIT) with a different look and layout:
  * name and branding: window/project-manager title, splash, application icon, logos
  * theme: dark grey panels with a blue selection, thin borders, small corner radius, compact spacing (the defaults of a
    fresh editor; the user can still change everything in Editor Settings)
  * layout: Hierarchy (scene tree) on the left, Inspector on the right, Project and Console in an open bottom panel; the
    2D / 3D / Script / Game buttons are a tab strip above the viewport and Play / Pause / Stop are the centre of the title bar.
Every replacement asserts that the text it changes is really there, so a different Godot version fails loudly.
"""
import os
import re
import shutil
import sys

root = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(here, "assets")


def edit(rel, old, new, count=1):
    path = os.path.join(root, rel)
    text = open(path, encoding="utf-8").read()
    assert old in text, f"{rel}: text not found:\n{old}"
    open(path, "w", encoding="utf-8").write(text.replace(old, new, count))


# ---- name -----------------------------------------------------------------------------------------------------------
edit("version.py", 'name = "Godot Engine"', 'name = "BlockComet Engine"')

# ---- theme defaults (a fresh editor) ---------------------------------------------------------------------------------------
S = "editor/settings/editor_settings.cpp"
edit(S, '"interface/theme/color_preset", "Default",', '"interface/theme/color_preset", "Custom",')
edit(S, '"interface/theme/spacing_preset", "Default", "Compact,Default,Spacious,Custom"',
        '"interface/theme/spacing_preset", "Compact", "Compact,Default,Spacious,Custom"')
edit(S, '"interface/theme/base_color", Color(0.14, 0.14, 0.14)', '"interface/theme/base_color", Color(0.22, 0.22, 0.22)')
edit(S, '"interface/theme/accent_color", Color(0.34, 0.62, 1.0)', '"interface/theme/accent_color", Color(0.24, 0.47, 0.76)')
edit(S, '"interface/theme/contrast", 0.3,', '"interface/theme/contrast", 0.2,')
edit(S, '"interface/theme/draw_extra_borders", false,', '"interface/theme/draw_extra_borders", true,')
edit(S, '"interface/theme/border_size", 0,', '"interface/theme/border_size", 1,')
edit(S, '"interface/theme/corner_radius", 4,', '"interface/theme/corner_radius", 2,')

# ---- layout: "Project" panel at the bottom -----------------------------------------------------------------------------------------
edit("editor/docks/filesystem_dock.cpp", "set_default_slot(EditorDock::DOCK_SLOT_LEFT_BR);",
     "set_default_slot(EditorDock::DOCK_SLOT_BOTTOM);")
# The editor adds the file system dock before it creates and registers the bottom panel. A dock whose slot is the bottom
# panel must be added after it, or the editor crashes at start (null bottom slot). The tab order stays: Project first.
edit("editor/editor_node.cpp",
     "\teditor_dock_manager->add_dock(filesystem_dock);\n\n\tmemnew(InspectorDock(editor_data));",
     "\n\tmemnew(InspectorDock(editor_data));")
edit("editor/editor_node.cpp",
     "\tcenter_split->set_dragger_visibility(SplitContainer::DRAGGER_HIDDEN);\n\n\tlog = memnew(EditorLog);",
     "\tcenter_split->set_dragger_visibility(SplitContainer::DRAGGER_HIDDEN);\n\n"
     "\t// BlockComet: the Project dock lives in the bottom panel, so it is added once that panel exists.\n"
     "\teditor_dock_manager->add_dock(filesystem_dock);\n\n\tlog = memnew(EditorLog);")

# ---- Stage 2: structure ----------------------------------------------------------------------------------------------------------------
N = "editor/editor_node.cpp"
# 2D / 3D / Script / Game / Asset Store buttons: from the middle of the title bar to a tab strip above the viewport
edit(N, "\ttitle_bar->add_child(main_editor_button_hb);\n\ttitle_bar->set_center_control(main_editor_button_hb);\n",
     "\t// BlockComet: the screen buttons form a tab strip above the viewport instead of sitting in the title bar.\n"
     "\tNode *main_screen_parent = editor_main_screen->get_parent();\n"
     "\tmain_screen_parent->add_child(main_editor_button_hb);\n"
     "\tmain_screen_parent->move_child(main_editor_button_hb, editor_main_screen->get_index());\n")
# Play / Pause / Stop in the middle of the title bar
edit(N, "\ttitle_bar->add_child(project_run_bar);\n",
     "\ttitle_bar->add_child(project_run_bar);\n"
     "\t// BlockComet: the run controls are the centre of the title bar.\n"
     "\ttitle_bar->move_child(project_run_bar, right_spacer->get_index());\n"
     "\ttitle_bar->set_center_control(project_run_bar);\n")
# the Project / Console panel is open from the first start
edit(N, "\t\t\tbottom_panel->load_layout_from_config(default_layout, EDITOR_NODE_CONFIG_SECTION);\n",
     "\t\t\tbottom_panel->load_layout_from_config(default_layout, EDITOR_NODE_CONFIG_SECTION);\n"
     "\t\t\tbottom_panel->make_item_visible(FileSystemDock::get_singleton());\n")
# names of the panels
edit("editor/docks/scene_tree_dock.cpp", 'set_name(TTRC("Scene"));', 'set_name(TTRC("Hierarchy"));')
edit("editor/docks/filesystem_dock.cpp", 'set_name(TTRC("FileSystem"));', 'set_name(TTRC("Project"));')
edit("editor/editor_log.cpp", 'set_name(TTRC("Output"));', 'set_name(TTRC("Console"));')
# the left column is only the Hierarchy: Import and History go under the Inspector
edit("editor/docks/import_dock.cpp", "set_default_slot(EditorDock::DOCK_SLOT_LEFT_UR);", "set_default_slot(EditorDock::DOCK_SLOT_RIGHT_BL);")
edit("editor/docks/history_dock.cpp", "set_default_slot(EditorDock::DOCK_SLOT_LEFT_BR);", "set_default_slot(EditorDock::DOCK_SLOT_RIGHT_BL);")

# ---- branding images -------------------------------------------------------------------------------------------------------------------
shutil.copy(os.path.join(assets, "splash.png"), os.path.join(root, "main", "splash.png"))
shutil.copy(os.path.join(assets, "app_icon.png"), os.path.join(root, "main", "app_icon.png"))

svg = open(os.path.join(assets, "logo.svg"), encoding="utf-8").read()
for name, size in (("TitleBarLogo.svg", 24), ("Godot.svg", 16), ("Logo.svg", 128)):
    sized = re.sub(r'width="512" height="512"', f'width="{size}" height="{size}"', svg, count=1)
    assert f'width="{size}"' in sized, "logo svg has an unexpected header"
    open(os.path.join(root, "editor", "icons", name), "w", encoding="utf-8").write(sized)

print("BlockComet Engine changes applied")
