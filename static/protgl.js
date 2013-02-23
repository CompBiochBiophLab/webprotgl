//<script>

function hide() {
  gCamera.getGLScene().setVisibility(false);
}

function WebGLProtein()
{
  this.loadpdb = function() {
    var input = document.getElementById("pdb_input");
    //var url = "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId=" + input.value;
    var url = "/protein/rcsb/pdb/"+input.value;
    console.log("Looking for protein " + input.value);
    $.get(url, pdbreader);
  }

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
//  console.log(url);
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

  function protgl_start() {
    try
    {
      var canvas = document.getElementById("canvas-protgl");
      gCamera = new Camera(canvas);
      var mm = new MovementManager(gCamera);

      gShader = new Shader(gCamera.getGLContext());
      gShader.init("shaders/sphere.vertex", "shaders/sphere.fragment");
      sphere_ = createGLSphere(gCamera.getGLContext(), 2); // 3);
      $.get("/protein/rcsb/pdb/3M3N", pdbreader, "binary");
    } catch (e) {
      alert(e);
    }
  }

  function pdbreader(pdb) {
    console.log("Protein found. Displaying");
    var root = gCamera.getGLScene();
    root.clear() // Replace with creating new child?

    var protein = new Protein();
    protein.parse(pdb, root, sphere_);
    protein.setID("Asdf");

    protein.print();

//    gShader = new Shader(gCamera.getGLContext());
//    gShader.init("shaders/sphere.vertex", "shaders/sphere.fragment");
//    var glSphere = createGLSphere(gCamera.getGLContext(), 2); // 3); // 3: good enough
    //protein.prepareScene(gCamera, sphere_);
    root.setShader(gShader);
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
  var isAnimating_ = false;
}
