<img src="https://i.imgur.com/vCVdnQ2.jpg">

VAMP generates mesh silhouettes, and removes hidden lines.  Has features similar to Blender Freestyle, but is dynamic (i.e. live, not only render-time.)  VAMP was built for use with [OsciStudio](https://oscilloscopemusic.com/oscistudio.php) for making [Oscilloscope Music](https://www.youtube.com/c/ChrisAllenMusic), but may be useful otherwise!

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
    - _flatSliced and flatSilhouette are remapped versions of the above meshes, translated onto the XY plane
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

**Note:** There are two versions of VAMP. One works with Blender 2.79, and the other is meant for Blender 2.8x.  It has been tested extensively with Oscistudio 5.5.  Even so, it crashes Blender OFTEN, so save your work.

## Settings:
**Ind Sil Mode -**  Normal silhouette mode takes all meshes, combines them, then calculates an overall silhouette.  Ind Sil mode will calculate silhouettes for each object in the group.

**Crop Options-** 
- None - fastest, and will display all mesh elements.  If some objects are behind the camera, will cause troubles.  
- Front -  all objects in front of the camera plane, regardless of whether they're visible within the camera frame.  
- Frame - dislpay ONLY objects visible from camera location.  

**Freestyle -**  Normal mode will display ALL visible edges when calculating _slicedFinal.  Freestyle mode will display only those edges which have been marked as Freestyle Edges in mesh edit.  Useful for simplifying results while maintaining some form.

**Freestyle Crease -** When Freestyle is selected, will also include all edges with angles sharper than the indicated angle.  Intended to behave like [Freestyle crease mode](https://docs.blender.org/manual/en/latest/render/freestyle/parameter_editor/line_style/modifiers/alpha/crease_angle.html) 

**Lim** - If using Freestyle crease mode, set the angle limit to flag creases


**VAMP Target -**  The name of the Collection of meshes to be vamp'd

**Output Scale -**  Changes the size of the _flatSliced and _flat_Silhouette meshes

**Vertex Limit -**  Limits the size of the meshes to be vamp'd.  Can be increased, but will affect performance.

**Cuts per edge -**  When analyzing, how many subedges should be created for each edge? Higher number gets better results, at the expense of performance.

**Min length -** The minimum length for any subedge.  This avoids very small source edges being subdivided.

**Raycast Distance -**  How far will the raycasting go (in blender units) for visibility testing. Make sure this is large enough to span the distance from the camera to the furthest vertex on the origin meshes.

**Hit Test Offset -**  The raycasting algorithm requires a slight offset factor when checking for visibility of vertices.  Should be very small, but not zero.  If your results are including too many small vertices that should be hidden, reduce this factor.

**Denoise -** This is a post-process of just the _flat meshes.  Will remove small edges whose length is below the threshold value.

**Denoise Limit -** The minimum length allowed for edges in final _flat meshes.  Edges below this length (aka noise) will be filtered out.

**Denoise Pct** The proportion of noise edges which will be removed. 1.0 is all of those edges, smaller proportions can make an interesting shading effect by retaining some short edges.

### Cautions & FAQs:
- VAMP is meant for relatively simple meshes.  Complex meshes (thousands of vertices) will probably choke it.  Save your work!
- VAMP is not made for speed.  Turning on VAMP and running animations will absolutely slow down your frame rate.
- Learn to use VAMP starting with small files.
- If VAMP is not working, make sure 
   1. you have an active camera, 
   2. the meshes to be vamp'd are in a named collection
   3. the vamp collection name is entered into the VAMP settings panel
   4. the Vertex Limit is set higher than the number of vertices in your meshes
   
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
