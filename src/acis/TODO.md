# Refactoring Status

## Completed
- [x] Created `src` directory for the standalone module.
- [x] Created `src/geometry.py` to replace `FreeCAD.Vector`, `Matrix`, and `Placement`.
- [x] Created `src/shapes.py` to replace FreeCAD `Part` topological shapes (`Edge`, `Face`, `Wire`, etc.) and geometry (`Line`, `Circle`, `BSplineCurve`, etc.).
- [x] Ported `src/importerUtils.py`:
    - Removed dependencies on `FreeCAD`, `FreeCADGui`, `PySide`, and `olefile`.
    - Replaced logging with standard `print`.
    - Mocked GUI functions and settings.
    - Fixed `unicode` compatibility for Python 3.
- [x] Started porting `src/Acis.py`:
    - Updated imports to use local `shapes` and `geometry`.
    - Removed `FreeCAD.ConfigGet` usage.

## To Do
- [x] **Dependencies**: Copy `importerConstants.py` to `src/`.
- [x] **Geometry**: Add `Vector2d` to `Base` mock in `src/geometry.py`.
- [x] **Shapes**: Add `Point` class to `src/shapes.py` (required by `Acis.py`).
- [x] **Acis.py**:
    - Fix relative import of `importerConstants`.
    - Ensure all `Part` object creations map correctly to `shapes` classes.
- [x] **Acis2Step.py**:
    - Port to `src/Acis2Step.py`.
    - Remove `FreeCAD` and `Part` imports.
    - Update logic to interact with `shapes` classes instead of FreeCAD objects.
- [x] **Verification**: Ensure no FreeCAD modules are imported when using the `src` package.
- [x] **CLI**: Create `src/cli.py` with `argparse` to convert ACIS to STEP.
- [x] **Fixes**:
    - Resolved `AttributeError: 'NoneType' object has no attribute 'GetInt'` in `importerUtils.py`.
    - Ensured `colors.json` is available in `src/acis/` for standalone execution.
