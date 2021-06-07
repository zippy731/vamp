<img src="https://i.imgur.com/vCVdnQ2.jpg">

Similar to Blender Freestyle, VAMP analyzes meshes from the camera perspective, and generates mesh silhouettes and removes hidden lines.  Has features similar to Freestyle, but operates directly on meshes in the 3D view (i.e. not only in render view,) and can dynamically update with animation frames.  

VAMP was built for use with [OsciStudio](https://oscilloscopemusic.com/oscistudio.php) for making [Oscilloscope Music](https://www.youtube.com/c/ChrisAllenMusic), but may be useful otherwise!

### Inputs:
- Blender mesh(es), curves, or Grease Pencil objects to be processed.
- Blender camera
 
### Outputs:
- Processed meshes, reflecting visible edges and visible silhouette from camera perspective
 
### How to Use:
- Create blender file with objects and an active camera
- Select target objects to be VAMP'ed, put into new collection
  - target objects can be a mix of meshes, curves, and Grease Pencil Line Art (GPLA) objects
  - If using GPLA objects, be sure to 'bake' the GP Line Art modifier before VAMPing 
- In VAMP control panel (under Render properties settings):
  - Update VAMP Target with name of new collection 

  - Click **VAMP ONCE**.  Vamp will create six new objects, and place them into a new collection called _vampOutput:
    - _slicedFinal is all visible edges from original mesh collection
    - _silhouetteFinal is just the silhouette from original mesh collection
    - _flatSliced and flatSilhouette are remapped versions of the above meshes, translated onto the flat XY plane
    - _traceFinal and _traceFinalMesh are initially empty, and will be used by the trace function, described below.
  - **Turn On VAMP** will **VAMP ONCE** for every frame change in the timeline.

### Tutorial Videos (updated for 2.93 version):
Part 1 - VAMP Setup and Usage
https://youtu.be/OytuO1ImTd0

Part 2 - VAMP Usage with Grease Pencil Line Art
https://youtu.be/Rgv6X14iTGQ

Part 3 - VAMP Trace mode 
https://youtu.be/lnhQnsjQx6o



### How it works:
VAMP takes input meshes, then subdivides edges into smaller subedges.  Using raycasting, it tests the visibility of subedge segments, and retains only those subedges which are visible to camera.  It then recombines those subedges into a simplified mesh.  \_flat meshes are the same meshes, but with vertices remapped onto the flat XY plane, for a top-down view.  The \_flat meshes are intended for use with OsciStudio

**Note:** VAMP is meant for use with Blender 2.8x and 2.9x.  It has been tested extensively with Oscistudio 5.5.  Even so, it will sometimes crash Blender, so save your work.  There is an older version of VAMP which works with Blender 2.79, but that is no longer being developed and some features are not included. 

## VAMP Settings:
**Turn On VAMP / VAMP ONCE -** VAMP ONCE will run VAMP just once, for the current setup.  Turn On VAMP is an on/off toggle, and will reprocess the scene once for every frame change, and is meant for use with animations.  Recommended to leave VAMP off, and adjust all of your settings using VAMP ONCE before turning on VAMP.  Note: If Turn On VAMP doesn't seem to be updating with each frame in an animation, click the "Reload Script" button and try again (see below.)

**Ind Sil Mode -**  Normal silhouette mode takes all meshes, combines them, then calculates an overall silhouette.  Individual Silhouette (Ind Sil) mode will calculate silhouettes for each object in the group.

**Crop Options-** 
- None - fastest, and will display all mesh elements.  If some objects are behind the camera, rempping vertices will cause trouble.  
- Front -  all objects in front of the camera plane, regardless of whether they're visible within the camera frame.  
- Frame - dislpay ONLY objects visible within camera frame.  

**Freestyle -**  Normal mode will display ALL visible edges when calculating \_slicedFinal.  Freestyle mode will display only those edges which have been marked as Freestyle Edges or Sharp Edges in mesh edit.  Useful for simplifying results while maintaining some form.

**Freestyle>Creases -** (2.8+ only) When Freestyle is selected, will also include all edges with interior angles up to the indicated angle.  Intended to behave like [Freestyle crease mode](https://docs.blender.org/manual/en/latest/render/freestyle/parameter_editor/line_style/modifiers/alpha/crease_angle.html) 

**Lim** - If using Freestyle crease mode, set the angle limit to flag creases.  The larger the number, the more edges will be displayed.  Selecting 180 is the same as including all edges on flat surfaces. 

**VAMP Target -**  The name of the Collection of meshes to be vamp'd

**Output Scale -**  Changes the size of the \_flatSliced and \_flatSilhouette meshes 

**Edge Limit -**  Limits the number of edges in the meshes to be VAMPed.  Can be increased, but will affect performance.

**Cuts per edge -**  When analyzing, how many subedges should be created for each edge? Higher number gets better results, at the expense of performance.

**Min length -** The minimum length for any subedge.  This avoids very small source edges being subdivided.

**Cull -** (2.8+ only) Sets a maximum distance for *objects* to be included in VAMP output.  Very useful for large scenes.  When Cull is turned on, VAMP will only include objects which are within a set radius from the camera.

**Cull>Distance -** Radius setting for Cull feature.

**Raycast Distance -**  How far will the raycasting go (in blender units) for visibility testing. Make sure this is large enough to span the distance from the camera to the furthest vertex on the origin meshes.  If using Cull, be sure to set Raycast to similar distance.

**Hit Test Offset -**  The raycasting algorithm requires a slight offset factor when checking for visibility of vertices.  Should be very small, but not zero.  If your results are including too many small vertices that should be hidden, reduce this factor.

**Denoise -** This is a post-process of just the \_flat meshes.  Will remove small edges whose length is below the threshold value.

**Denoise>Limit -** The minimum length allowed for edges in final \_flat meshes.  Edges below this length (aka noise) will be filtered out.

**Denoise>Pct** The proportion of noise edges which will be removed. 1.0 is all of those edges, smaller proportions can make an interesting shading effect by retaining some short edges.

## Trace Mode: (2.8+ only)
Trace mode will take the input mesh, generate a list of vertices, then output a curve which traces a path through the vertices.  Vertices can be generated several ways, and output curves can be Bezier or NURBS.  Trace also generates a mesh version of the resulting curve.

Trace determines the sequence of vertices by traversing the mesh, iteratively selecting the nearest vertex to the previous vertex.  This is simplistic, and not necessarily the shortest path between all of the vertices, but it is quick and creates interesting curve paths for further use.  

Trace takes the same input information as VAMP, and will output one curve, \_traceFinal, plus \_traceFinalMesh, which is a mesh version of the trace results.  Two trace modes, FlatSliced and FlatSilhouette will take the results of VAMP, then feed those back through the trace algorithm.  

**Turn On Trace** If VAMP is on (see above,) Trace will recalculate once for each change in animation frame.  Note: Trace is dependent on VAMP, so Turn On Trace has NO effect unless VAMP is also on.

**Trace ONCE** Similar to VAMP Once, Trace ONCE will calculate the trace just once, based on the user settings.

**Trace Limit** Limit the total number of vertices used in Trace.  If the origin mesh has more vertices, Trace will still work, but it will only include vertices up to the limit.  

**Trace Mode** Sets the source of vertices for Trace.  Faces (default) will use the centers of polygons in the mesh.  Edges will use centerpoints of all edges, and Verts will just use the input mesh vertices.  FlatSliced and FlatSilhouette will use those respective results of VAMP as the input to the trace algorithm.

**Curve Type** Determines output curve type.  Bezier (default) seems to be more stable, but NURBS is also available.

***Notes:*** 
- despite requiring the same inputs as VAMP, Trace ignores camera information during analysis.  Trace will analyze and create a path through ALL vertices in the input mesh, whether or not they would be visible from the camera perspective.
- Trace works best when the origin mesh has at least some complexity for it to analyze and work from.  Broad surfaces are better than intricate details.  Experiment with different levels of subdivision in the input meshes.  
- Trace calculates the 'shortest path' sequence of vertices each time it runs.  This means that if an input mesh is animated, Trace may calculate a different vertex sequence, so the resulting trace may snap visually around during animation.  This is expected. 

## Reload Script (2.8+ only)
Occasionally, VAMP will stop working properly.  This is most noticeable when using in conjunction with other add-ons, such as Oscistudio or Animation Nodes.  Reload Script will reload VAMP from disk, and also re-register the application handlers.

## Using with Oscistudio
Recommended workflow is: 
- Create objects and camera animation in blender
- Simplify origin meshes wherever possible. SAVE your work!
- Enable VAMP, adjust settings to optimize final mesh.
- Hide all objects in scene except for \_flatSliced and \_flatSilhouette.
- Connect to Oscistudio, confirm that mesh is visible. Oscistudio default un-rotated view should display \_flat meshes cleanly.
- Send Animation to Oscistudio

## Using with Grease Pencil Line Art (Blender 2.93 onward)
Beginning with the Blender 2.93 release, Grease Pencil (GP) now has the ability to create intricate line drawings from existing geometry, using the [Grease Pencil Line Art (GPLA) modifier](https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html).  The GPLA modifier creates drawings from edges, accounting for marked feature lines, creases, and contours, and calculating occlusion correctly.  This new Blender feature is quite similar to the original core function of VAMP, and is much faster as it is a native Blender feature.  

VAMP can take these GPLA drawings as an input, and process and reformat them for output to OsciStudio.  Using VAMP with GPLA takes a bit of planning, but can yield some terrific results.

Recommended workflow for use with GPLA is:
- Create scene as usual.  Adjust the camera for the angle of view you desire.
- Move target mesh objects into a single new collection (e.g. GPInput)
- Create a new GP Collection Line Art object.  In the new GP object, specify the target collection in the GPLA modifier.  It will take a moment, but the GPLA should draw nice outlines of your object(s)
 - If you do not see lines immediately, make sure your camera is set correctly. GPLA will not work without a camera. For better visibility of the lines, you can set the Viewport Visibility of the GP object to 'front'.  
 - Note that GPLA is based on visible objects, so if you hide the target objects, GPLA may exclude them from the final output.  
 - Tweak the settings in GPLA modifier to your liking.
 - Once you are happy with the GPLA results, BAKE the results (In the GPLA modifier tab, Baking subpanel is at the very bottom.)
- Move the GP object into a new collection (e.g. VAMPinput)
- In VAMP, set the VAMP Target to the name of the newly created collection which contains the GP object.  
- Click VAMP Once.  If VAMP worked properly, a new collection of \_vampOutput objects will be created.  
- VAMP may be used normally beyond this point.

Notes about GPLA usage
- Performance: Because most of the edge/occlusion calculations are being done by GPLA (rather than VAMP,) GPLA is MUCH faster than VAMP.  Also, because the GPLA output is a simple object with lines/curves and no faces, many of the VAMP settings will have no effect on the output.  It is recommended that you leave the VAMP Cuts per Edge = 2, for speed.  VAMP Denoise will still have an effect, and is a useful way to simplify complex GPLA meshes.
- GP modifiers: Some GP object modifiers placed AFTER the GPLA modifier DO NOT seem to affect the data that is sent to VAMP.  Notably, the 'simplify' GP modifier does not seem to work as expected. This is a known issue, and I recommend you use the VAMP Denoise feature for similar benefits.  Other GP modifiers do seem to work normally.  Experiment with other GP modifiers to see what best suits your needs.
- Do not mix GPLA and mesh/curve objects: GPLA and other object types should not be combined, and VAMP can only handle a single GPLA object.

### Cautions & FAQs:
- VAMP is meant for relatively simple meshes.  Complex meshes (thousands of vertices) may choke it, depending on your PC's power.  Save your work!
- VAMP is not made for speed.  Turning on VAMP and running animations will absolutely slow down your frame rate.
- Learn to use VAMP starting with small files.
- If VAMP is not working, make sure: 
   1. You have an active camera, pointed at your scene. 
   2. The objects to be VAMP'd are in a named collection
   3. The Vamp collection name is entered into the VAMP settings panel
   4. The Edge Limit is set higher than the number of vertices in your meshes.
   5. Cull and Raycast limits are sufficiently large for your model.


### Installing VAMP
- VAMP is a [Blender add-on](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html), written for use with Blender 2.8+ and 2.93.  It has been tested and is stable for use with Blender 2.83 LTS and 2.93 LTS.  
- To install, 
  - Download the contents of this repository to your desktop.  It is the master file, and contains the installer, an older version, and this version.
  - From the master zip, extract vamp_293.zip and save to your desktop.  Leave it as a zip file.  
  - Within Blender, go to Edit\Preferences\Add-ons
   - (If you have any previous versions of VAMP, you should disable and remove them now)
  - Within the Add-on menu, install new VAMP: Browse to the vamp_293.zip file and click Install.  
  - After installing, enable vamp_293 in the list of add-ons.  
  - You should see the VAMP Settings panel now, under the Render properties tab.  

 * There is also an older version of this add-on which works with Blender 2.79. Download vamp_279.zip and install using instructions above.  There is also a tutorial video for this version, here: https://youtu.be/9H-l_qkF8OI
  
### META

- VAMP was written by Chris Allen
- Licensed GNU GPLv3 
