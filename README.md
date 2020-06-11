# vamp
Vector Art Motion Processor - Blender 2.79 Python add-in to remove hidden edges from meshes

Meant for use with OsciStudio [OsciStudio](https://oscilloscopemusic.com/oscistudio.php) for making [Oscilloscope Music](https://www.youtube.com/c/ChrisAllenMusic), but may be useful otherwise!

### Inputs:
- blender mesh(es) to be processed.
- blender camera
 
### Outputs:
- processed meshes reflecting visible edges and visible silhouette, from camera perspective
 
### How to Use:
- create blender file with meshes and an active camera
- select meshes of interest, create new group
- In VAMP control panel (under Render properties settings):
  - Update VAMP Target with name of new group 

  - Click **VAMP ONCE**.  Vamp will create four new meshes:
    - _slicedFinal is all visible edges from original mesh group
    - _silhouetteFinal is just the silhouette from original mesh group
    - _flatSliced and flatSilhouette are remapped versions of the above meshes, translated onto the XY plane
  - **Turn On VAMP** will **VAMP ONCE** for every frame change in the timeline.

### How it works:
VAMP takes input meshes, then subdivides edges into smaller subedges.  Using raycasting, it tests the visibility of subedge segments, and retains only those subedges which are visible to camera.  It then recombines those subedges into a simplified mesh.  _flat meshes are the same meshes, but with vertices remapped onto the flat XY plane.

## Using with Oscistudio
Recommended workflow is: 
- Create objects and camera animation in blender
- Simplify origin meshes wherever possible. SAVE your work!
- Enable VAMP, adjust settings to optimize final mesh.
- Hide all objects in scene except for _flatSliced and _flatSilhouette.
- Connect to Oscistudio, confirm that mesh is visible.
- Send Animation to Oscistudio
**Note:** VAMP currently only works with Blender 2.79, and has been tested extensively with Oscistudio 5.5.

## Settings:
**Ind Sil Mode -**  Normal silhouette mode takes all meshes, combines them, then calculates an overall silhouette.  Ind Sil mode will calculate silhouettes for each object in the group.

**Freestyle -**  Normal mode will display ALL visible edges when calculating _slicedFinal.  Freestyle mode will display only those edges which have been marked as Freestyle Edges in mesh edit.  Useful for simplifying results while maintaining some form.

**Crop -** Normal mode will display all mesh elements visible from camera location. Crop mode will excude objects which are not strictly visible in camera view.  Useful for simplifying complex scenes.

**VAMP Target -**  The name of the group of meshes to be vamp'd

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
   2. the meshes to be vamp'd are in a named group
   3. the group name is entered into the VAMP settings panel
   4. the Vertex Limit is set higher than the number of vertices in your meshes
   
### Installing VAMP
- VAMP is a Blender plugin, written for use with Blender 2.79.  Currently will not work with Blender 2.8x, but a 2.8x version is planned.
- To install, 
  - Download vamp_279.zip and save to your desktop.  
  - Within Blender, go to User Preferences, Add-ons, then select Install Add-on from File.  
  - Browse to the vamp_279.zip file and click Install.  
  - After installing, enable vamp_279 in the list of add-ons.  
  - You should see the VAMP Settings panel now, under the Render properties tab.  
  
### META

- VAMP was written by Chris Allen
- Licensed GNU GPLv3 
