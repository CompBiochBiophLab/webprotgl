//<script>

function WebGLProtein()
{
  this.loadpdb = function(pdb_id, onSuccess, onFinished, onFailure) {
    var url = "/webglprotein/protein/rcsb/pdb/"+pdb_id;
    console.log("Looking for protein " + pdb_id);
    $.ajax({ type: "GET", dataType: "binary", url: url, timeout: 60000,
             success: function(data, textStatus) { onSuccess(); pdbreader(data); onFinished(); },
             error: function(xhr, textStatus, errorThrown) { onFailure(xhr); }
    });
  }

  //SNIP
  var loadedScripts_ = 0;

  var onScriptsLoaded = function()
  {
    ++loadedScripts_;
    if (loadedScripts_ < totalScripts_)
      return;

    protgl_start();
  }

  var loadScript = function(url)
  {
    var head = document.getElementsByTagName("head")[0];
    var script = document.createElement("script");
    script.type="text/javascript";
    script.src=url;

    // Cross-browser compatibility
    script.onreadystatechange = onScriptsLoaded;
    script.onload = onScriptsLoaded;

    // Start loading
    head.appendChild(script);
  }

  var allScripts_ = [
    "jquery_binary.js",
    "base.js",
    "webgl/boundingbox.js",
    "webgl/camera.js",
    "webgl/fast.js",
    "webgl/mouse.js",
    "webgl/shader.js",
    "webgl/shaderparameter.js",
    "webgl/shape.js",
    "webgl/basicshapes.js",
    "webgl/transform.js",
    "webgl/movementmanager.js",
    "jdataview.js",
    "protein.js"];
  var totalScripts_ = allScripts_.length;

  for (script in allScripts_)
  {
    loadScript(allScripts_[script]);
  }
  //SNAP

  function protgl_start() {
    try
    {
      var canvas = document.getElementById("canvas-protgl");
      gCamera = new Camera(canvas);
      var mm = new MovementManager(gCamera);
      
      var elt = document.getElementById("shader_sphere_vertex");
      var shader_sphere_vertex = elt.value;
      elt.parentNode.removeChild(elt);
      
      elt = document.getElementById("shader_sphere_fragment");
      var shader_sphere_fragment = elt.value;
      elt.parentNode.removeChild(elt);
      
      elt = document.getElementById("shader_cylinder_vertex");
      var shader_cylinder_vertex = elt.value;
      elt.parentNode.removeChild(elt);
      
      elt = document.getElementById("shader_cylinder_fragment");
      var shader_cylinder_fragment = elt.value;
      elt.parentNode.removeChild(elt);
      

      sphereShader_ = new Shader(gCamera.getGLContext());
      sphereShader_.init(shader_sphere_vertex, shader_sphere_fragment);
      cylinderShader_ = new Shader(gCamera.getGLContext());
      cylinderShader_.init(shader_cylinder_vertex, shader_cylinder_fragment);
//       cylinderShader_ = sphereShader_;//new Shader(gCamera.getGLContext());
//      cylinderShader_.init("shaders/cylinder.vertex", "shaders/cylinder.fragment");
      var refinements = 2; // 3;
      sphere_ = createGLSphere(gCamera.getGLContext(), refinements);
      cylinder_ = createGLOpenCylinder(gCamera.getGLContext(), Math.pow(2, refinements) * 4, 2);
      $.get("/webglprotein/protein/rcsb/pdb/2KXR", pdbreader, "binary");
    } catch (e) {
      alert(e);
    }
  }

  function pdbreader(pdb) {
    console.log("Protein found. Displaying");
    var root = gCamera.getGLScene();
    root.clear() // Replace with creating new child?

    var sphereRoot = root.addChild();
    sphereRoot.setShader(sphereShader_);
    var cylinderRoot = root.addChild();
    cylinderRoot.setShader(cylinderShader_);

    var protein = new Protein();
    protein.parse(pdb, sphereRoot, sphere_, cylinderRoot, cylinder_);
    protein.setID("Asdf");

    protein.print();

    gCamera.setTargetObject(protein);

    requestAnimationFrame = window.requestAnimationFrame;
    if (!requestAnimationFrame)
      requestAnimationFrame = window.mozRequestAnimationFrame;
    if (!requestAnimationFrame)
      requestAnimationFrame = window.webkitRequestAnimationFrame;
    if (!requestAnimationFrame)
    {
      alert ("Animation frame not created"); // TODO: localize
      return;
    }

    if (!isAnimating_) {
      isAnimating_ = true;
      animate();
    }
  }

  function animate() {
    gCamera.display();
    requestAnimationFrame(animate);
  }

  var sphere_;
  var sphereShader_;
  var cylinder_;
  var cylinderShader_;
  var isAnimating_ = false;
  //SNIP
  /*
  //SNAP
  protgl_start();
  //SNIP
  */
  //SNAP
}

WebGLProtein.prototype.getScene = function() {
  return gCamera.getGLScene();
}

WebGLProtein.prototype.show = function(visibility) {
  gCamera.getGLScene().setVisibility(visibility);
}

window["WebGLProtein"] = WebGLProtein;
