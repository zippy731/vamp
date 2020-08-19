<img src="https://i.imgur.com/vCVdnQ2.jpg">

Similar to Blender Freestyle, VAMP analyzes meshes from the camera perspective, and generates mesh silhouettes and removes hidden lines.  Has features similar to Freestyle, but is dynamic (i.e. live, not only render-time.)  

VAMP was built for use with [OsciStudio](https://oscilloscopemusic.com/oscistudio.php) for making [Oscilloscope Music](https://www.youtube.com/c/ChrisAllenMusic), but may be useful otherwise!

### Inputs:
- Blender mesh(es) to be processed.
- Blender camera
 
### Outputs:
- Processed meshes, reflecting visible edges and visible silhouette from camera perspective
 
### How to Use:
- Create blender file with meshes and an active camera
- Select meshes of interest, create new collection
- In VAMP control panel (under Render properties settings):
  - Update VAMP Target with name of new collection 

  - Click **VAMP ONCE**.  Vamp will create four new meshes:
    - _slicedFinal is all visible edges from original mesh collection
    - _silhouetteFinal is just the silhouette from original mesh collection
    - _flatSliced and flatSilhouette are remapped versions of the above meshes, translated onto the flat XY plane
  - **Turn On VAMP** will **VAMP ONCE** for every frame change in the timeline.

### Tutorial Video:  https://youtu.be/9H-l_qkF8OI

### How it works:
VAMP takes input meshes, then subdivides edges into smaller subedges.  Using raycasting, it tests the visibility of subedge segments, and retains only those subedges which are visible to camera.  It then recombines those subedges into a simplified mesh.  _flat meshes are the same meshes, but with vertices remapped onto the flat XY plane.

## Using with Oscistudio
Recommended workflow is: 
- Create objects and camera animation in blender
- Simplify origin meshes wherever possible. SAVE your work!
- Enable VAMP, adjust settings to optimize final mesh.
- Hide all objects in scene except for _flatSliced and _flatSilhouette.
- Connect to Oscistudio, confirm that mesh is visible. Oscistudio default un-rotated view should display _flat meshes cleanly.
- Send Animation to Oscistudio

**Note:** There are two versions of VAMP. One works with Blender 2.79, and the other is meant for Blender 2.8x.  It has been tested extensively with Oscistudio 5.5.  Even so, it crashes Blender OFTEN, so save your work.  Also, some features are only available in the 2.8x version.

## VAMP Settings:
**Turn On VAMP / VAMP ONCE -** VAMP ONCE will run VAMP just once, for the current setup.  Turn On VAMP is an on/off toggle, and will reprocess the scene once for every frame change, and is meant for use with animations.  Recommended to leave VAMP off, and adjust all of your settings using VAMP ONCE before turning on VAMP.

**Ind Sil Mode -**  Normal silhouette mode takes all meshes, combines them, then calculates an overall silhouette.  Individual Silhouette (Ind Sil) mode will calculate silhouettes for each object in the group.

**Crop Options-** 
- None - fastest, and will display all mesh elements.  If some objects are behind the camera, rempping vertices will cause trouble.  
- Front -  all objects in front of the camera plane, regardless of whether they're visible within the camera frame.  
- Frame - dislpay ONLY objects visible within camera frame.  

**Freestyle -**  Normal mode will display ALL visible edges when calculating _slicedFinal.  Freestyle mode will display only those edges which have been marked as Freestyle Edges in mesh edit.  Useful for simplifying results while maintaining some form.

**Freestyle>Creases -** (2.8 only) When Freestyle is selected, will also include all edges with interior angles up to the indicated angle.  Intended to behave like [Freestyle crease mode](https://docs.blender.org/manual/en/latest/render/freestyle/parameter_editor/line_style/modifiers/alpha/crease_angle.html) 

**Lim** - If using Freestyle crease mode, set the angle limit to flag creases.  The larger the number, the more edges will be displayed.  Selecting 180 is the same as including all edges on flat surfaces. 

**VAMP Target -**  The name of the Collection of meshes to be vamp'd

**Output Scale -**  Changes the size of the _flatSliced and _flat_Silhouette meshes 

**Edge Limit -**  Limits the number of edges in the meshes to be VAMPed.  Can be increased, but will affect performance.

**Cuts per edge -**  When analyzing, how many subedges should be created for each edge? Higher number gets better results, at the expense of performance.

**Min length -** The minimum length for any subedge.  This avoids very small source edges being subdivided.

**Cull -** (2.8 only) Sets a maximum distance for *objects* to be included in VAMP output.  Very useful for large scenes.  When Cull is turned on, VAMP will only include objects which are within a set radius from the camera.

**Cull>Distance -** Radius setting for Cull feature.

**Raycast Distance -**  How far will the raycasting go (in blender units) for visibility testing. Make sure this is large enough to span the distance from the camera to the furthest vertex on the origin meshes.  If using Cull, be sure to set Raycast to similar distance.

**Hit Test Offset -**  The raycasting algorithm requires a slight offset factor when checking for visibility of vertices.  Should be very small, but not zero.  If your results are including too many small vertices that should be hidden, reduce this factor.

**Denoise -** This is a post-process of just the _flat meshes.  Will remove small edges whose length is below the threshold value.

**Denoise>Limit -** The minimum length allowed for edges in final _flat meshes.  Edges below this length (aka noise) will be filtered out.

**Denoise>Pct** The proportion of noise edges which will be removed. 1.0 is all of those edges, smaller proportions can make an interesting shading effect by retaining some short edges.

## Trace Mode: (2.8 only)
Trace mode will take the input mesh, generate a list of vertices, then output a curve which traces a path through the vertices.  Vertices can be generated several ways, and output curves can be Bezier or NURBS.  Trace also generates a mesh version of the resulting curve.

Trace determines the sequence of vertices by traversing the mesh, iteratively selecting the nearest vertex to the previous vertex.  This is simplistic, and not necessarily the shortest path between all of the vertices, but it is quick and creates interesting curve paths for further use.  

Trace takes the same input information as VAMP, and will output one curve, _traceFinal, plus _traceFinalMesh, which is a mesh version of the trace results.

**Turn On Trace** If VAMP is on (see above,) Trace will recalculate once for each change in animation frame.  Note: Turn On Trace has NO effect unless VAMP is also on.

**Trace ONCE** Similar to VAMP Once, Trace ONCE will calculate the trace just once, based on the user settings.

**Trace Limit** Limit the total number of vertices used in Trace.  If the origin mesh has more vertices, Trace will still work, but it will only include vertices up to the limit.  

**Trace Mode** Sets the source of vertices for Trace.  Faces (default) will use the centers of polygons in the mesh.  Edges will use centerpoints of all edges, and Verts will just use the input mesh vertices.

**Curve Type** Determines output curve type.  Bezier (default) seems to be more stable, but NURBS is also available.

***Notes:*** 
- despite requiring the same inputs as VAMP, Trace ignores camera information during analysis.  Trace will analyze and create a path through ALL vertices in the input mesh, whether or not they would be visible from the camera perspective.
- Trace works best when the origin mesh has at least some complexity for it to analyze and work from.  Broad surfaces are better than intricate details.  Experiment with different levels of subdivision in the input meshes.  
- Trace calculates the 'shortest path' sequence of vertices each time it runs.  This means that if an input mesh is animated, Trace may calculate a different vertex sequence, so the resulting trace may snap visually around during animation.  This is expected. 

## Reload Script (2.8 only)
Occasionally, VAMP will stop working properly.  This is most noticeable when using in conjunction with other add-ons, such as Oscistudio or Animation Nodes.  Reload Script will reload VAMP from disk, and also re-register the application handlers.


### Cautions & FAQs:
- VAMP is meant for relatively simple meshes.  Complex meshes (thousands of vertices) may choke it, depending on your PC's power.  Save your work!
- VAMP is not made for speed.  Turning on VAMP and running animations will absolutely slow down your frame rate.
- Learn to use VAMP starting with small files.
- If VAMP is not working, make sure 
   1. you have an active camera, 
   2. the meshes to be vamp'd are in a named collection
   3. the Vamp collection name is entered into the VAMP settings panel
   4. the Edge Limit is set higher than the number of vertices in your meshes
   5. Cull and Raycast limits are sufficiently large for your model.
   
### Installing VAMP
- VAMP is a [Blender add-on](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html), written for use with Blender 2.8x.  
- To install, 
  - Download vamp_283.zip and save to your desktop.  
  - Within Blender, go to Edit\Preferences\Add-ons, then select Install.  
  - Browse to the vamp_283.zip file and click Install.  
  - After installing, enable vamp_283 in the list of add-ons.  
  - You should see the VAMP Settings panel now, under the Render properties tab.  

 * There is also an older version of this add-on which works with Blender 2.79. Download vamp_279.zip.
  
### META

- VAMP was written by Chris Allen
- Licensed GNU GPLv3 
