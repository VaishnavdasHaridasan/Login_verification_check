import win32com.client
import spacy
import pythoncom
import math

# Connect to SolidWorks
swApp = win32com.client.Dispatch("SldWorks.Application")

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")


def create_rectangle(length, breadth):
    # Create a new part document
    template_path = "C:\\ProgramData\\SOLIDWORKS\\SOLIDWORKS 2022\\templates\\Part.prtdot"
    swModel = swApp.NewDocument(template_path, 0, 0, 0)

    if not swModel:
        print("Failed to create a new part document.")
        return

    # Activate the front plane
    variant_null = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    result = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, variant_null, 0)

    if not result:
        print("Failed to select the front plane.")
        return

    # Create a new sketch
    swSketch = swModel.SketchManager
    swSketch.InsertSketch(True)

    # Draw a rectangle
    swSketch.CreateCenterRectangle(0, 0, 0, length / 1000, breadth / 1000, 0)  # Dimensions are in meters

    # Exit the sketch
    swSketch.InsertSketch(False)

    # Extrude the sketch
    swFeatureMgr = swModel.FeatureManager
    swFeatureMgr.FeatureExtrusion2(True,  # bAdd
                                   False,  # bFlip
                                   False,  # bDirection
                                   0,  # End condition type 1
                                   0,  # End condition type 2
                                   0.01,  # Depth 1
                                   0.01,  # Depth 2
                                   False,  # Draft outward
                                   False,  # Draft outward second direction
                                   False,  # Draft angle
                                   False,  # Draft angle second direction
                                   0,  # Draft type
                                   0,  # Draft type second direction
                                   False,  # Merge result
                                   False,  # Use draft
                                   False,  # Use draft second direction
                                   False,  # Auto preview
                                   True,  # Flip side to cut
                                   True,  # Thin feature
                                   True,  # Thin type
                                   0,  # Wall thickness
                                   0,  # Wall thickness 2
                                   False)  # Wall type

    # Fit the model to screen
    swModel.ViewZoomToFit2()


def create_line(length):
    # Create a new part document
    template_path = "C:\\ProgramData\\SOLIDWORKS\\SOLIDWORKS 2022\\templates\\Part.prtdot"
    swModel = swApp.NewDocument(template_path, 0, 0, 0)

    if not swModel:
        print("Failed to create a new part document.")
        return

    # Activate the front plane
    variant_null = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    result = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, variant_null, 0)

    if not result:
        print("Failed to select the front plane.")
        return

    # Create a new sketch
    swSketch = swModel.SketchManager
    swSketch.InsertSketch(True)

    # Draw a line
    swSketch.CreateLine(0, 0, 0, length / 1000, 0, 0)  # Dimensions are in meters

    # Exit the sketch
    swSketch.InsertSketch(False)

    # Fit the model to screen
    swModel.ViewZoomToFit2()


def create_circle(diameter):
    # Create a new part document
    template_path = "C:\\ProgramData\\SOLIDWORKS\\SOLIDWORKS 2022\\templates\\Part.prtdot"
    swModel = swApp.NewDocument(template_path, 0, 0, 0)

    if not swModel:
        print("Failed to create a new part document.")
        return

    # Activate the front plane
    variant_null = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    result = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, variant_null, 0)

    if not result:
        print("Failed to select the front plane.")
        return

    # Create a new sketch
    swSketch = swModel.SketchManager
    swSketch.InsertSketch(True)

    # Draw a circle
    swSketch.CreateCircleByRadius(0, 0, 0, diameter / 2000)  # Radius is half the diameter

    # Exit the sketch
    swSketch.InsertSketch(False)

    # Fit the model to screen
    swModel.ViewZoomToFit2()


def create_polygon(sides, radius):
    # Create a new part document
    template_path = "C:\\ProgramData\\SOLIDWORKS\\SOLIDWORKS 2022\\templates\\Part.prtdot"
    swModel = swApp.NewDocument(template_path, 0, 0, 0)

    if not swModel:
        print("Failed to create a new part document.")
        return

    # Activate the front plane
    variant_null = win32com.client.VARIANT(pythoncom.VT_DISPATCH, None)
    result = swModel.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, variant_null, 0)

    if not result:
        print("Failed to select the front plane.")
        return

    # Create a new sketch
    swSketch = swModel.SketchManager
    swSketch.InsertSketch(True)

    # Calculate the vertices of the polygon
    vertices = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        x = radius / 1000 * math.cos(angle)
        y = radius / 1000 * math.sin(angle)
        vertices.append((x, y))

    # Draw the polygon
    for i in range(sides):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % sides]
        swSketch.CreateLine(x1, y1, 0, x2, y2, 0)

    # Exit the sketch
    swSketch.InsertSketch(False)

    # Fit the model to screen
    swModel.ViewZoomToFit2()


def parse_instruction(instruction):
    doc = nlp(instruction)
    shape = None
    params = {}

    for token in doc:
        if token.text.lower() in ["rectangle", "line", "circle", "polygon"]:
            shape = token.text.lower()
        if token.text.lower() in ["length", "breadth", "diameter", "sides", "radius"]:
            for child in token.children:
                if child.like_num:
                    params[token.text.lower()] = int(child.text)

    for param in ["length", "breadth", "diameter", "sides", "radius"]:
        if param not in params:
            params[param] = None

    return shape, params


def main():
    instruction = input("Please provide design instructions: ")
    shape, params = parse_instruction(instruction)
    if shape == "rectangle" and params["length"] and params["breadth"]:
        create_rectangle(params["length"], params["breadth"])
        print("Rectangle created successfully.")
    elif shape == "line" and params["length"]:
        create_line(params["length"])
        print("Line created successfully.")
    elif shape == "circle" and params["diameter"]:
        create_circle(params["diameter"])
        print("Circle created successfully.")
    elif shape == "polygon" and params["sides"] and params["radius"]:
        create_polygon(params["sides"], params["radius"])
        print("Polygon created successfully.")
    else:
        print("Invalid instruction. Please provide valid instructions.")


if __name__ == "__main__":
    main()

