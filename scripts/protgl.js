//<script>

function WebGLProtein()
{
  this.loadpdb = function(url, onSuccess, onFinished, onFailure) {
    console.log("Looking for protein " + url);
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
    "/static/jquery_binary.js",
    "/static/base.js",
    "/static/webgl/boundingbox.js",
    "/static/webgl/camera.js",
    "/static/webgl/fast.js",
    /*"/static/webgl/mouse.js",*/
    "/static/webgl/shader.js",
    "/static/webgl/shaderparameter.js",
    "/static/webgl/shape.js",
    "/static/webgl/basicshapes.js",
    "/static/webgl/transform.js",
    "/static/webgl/movementmanager.js",
    "/static/jdataview.js",
    "/static/protein.js"];
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

      // Load the shaders before continuing...
      $.get(static_path() + "/shaders.json", shaders);
    } catch (e) {
      alert(e);
    }
  }

  function shaders(shader) {
    var refinements = 2; // 3;

    sphereShader_ = new Shader(gCamera.getGLContext());
    sphereShader_.init(shader["sphere"]["v"], shader["sphere"]["f"]);
    sphere_ = createGLSphere(gCamera.getGLContext(), refinements);

    cylinderShader_ = new Shader(gCamera.getGLContext());
    cylinderShader_.init(shader["cylinder"]["v"], shader["cylinder"]["f"]);
    cylinder_ = createGLOpenCylinder(gCamera.getGLContext(), Math.pow(2, refinements) * 4, 3);

    $.get(initial_protein(), pdbreader, "binary");
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
