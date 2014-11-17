//<script>

function OnlineProtein(static_path)
{
  var that = this;
  var current_url = "";
  var isAnimating_ = false;

  var sphere_;
  var sphereShader_;
  var cylinder_;
  var cylinderShader_;

  //var lastFrame_ = new Date();

  function animate() {
    gCamera.display();
    requestAnimationFrame(animate);
    //this_frame = new Date();
    //console.log(this_frame.getTime() - lastFrame_.getTime());
    //lastFrame_ = this_frame;
  }

  this.initWebGL = function() {
    try
    {
      var canvas = document.getElementById("canvas-protgl");
      gCamera = new Camera(canvas);
      var mm = new MovementManager(gCamera);

      // Load the shaders before continuing...
      $.get(static_path + "shaders.json", that.loadShaders);
    } catch (e) {
      alert(e);
    }
  }

  this.loadScripts = function() {
    initWebGL();
  }

  this.loadShaders = function(shader) {
    var refinements = 2; // 3;

    sphereShader_ = new Shader(gCamera.getGLContext());
    sphereShader_.init(shader["sphere"]["v"], shader["sphere"]["f"]);
    sphere_ = createGLSphere(gCamera.getGLContext(), refinements);

    cylinderShader_ = new Shader(gCamera.getGLContext());
    cylinderShader_.init(shader["cylinder"]["v"], shader["cylinder"]["f"]);
    cylinder_ = createGLOpenCylinder(gCamera.getGLContext(), Math.pow(2, refinements) * 4, 4);


    $.ajax({
      url: current_url,
      dataType: "binary",
      success: parseProtein,
      error: function() {
        hide_dialog();
        show_dialog("No such protein found.", "ok", "").done(function(result) {
          hide_dialog();
        });
      }
    });
  }

  this.onStart = function(base_url) {
    show_dialog("Requesting protein. Please wait...", "", "");

    // Prepare scripts, WebGL, ...
    current_url = base_url;
    that.loadScripts();
  }

  function parseProtein(pdb) {
    hide_dialog();
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

  //SNIP
  this.loadScripts = function() {
    var allScripts = [
      "jquery_binary.js",
      "base.js",
      "webgl/boundingbox.js",
      "webgl/camera.js",
      "webgl/fast.js",
      /*"webgl/mouse.js",*/
      "webgl/shader.js",
      "webgl/shaderparameter.js",
      "webgl/shape.js",
      "webgl/basicshapes.js",
      "webgl/transform.js",
      "webgl/movementmanager.js",
      "jdataview.js",
      "protein.js"];
    var totalScripts = allScripts.length;
    var loadedScripts = 0;

    var onScriptLoaded = function() {
      ++loadedScripts;
      if (loadedScripts < totalScripts)
        return;

      that.initWebGL();
    }

    for (script in allScripts)
    {
      var url = static_path + allScripts[script];
      var head = document.getElementsByTagName("head")[0];
      var script = document.createElement("script");
      script.type="text/javascript";
      script.src=url;

      // Cross-browser compatibility
      script.onreadystatechange = onScriptLoaded;
      script.onload = onScriptLoaded;

      // Start loading
      head.appendChild(script);
    }
  }
  //SNAP

}
/*
WebGLProtein.prototype.getScene = function() {
  return gCamera.getGLScene();
}

WebGLProtein.prototype.show = function(visibility) {
  gCamera.getGLScene().setVisibility(visibility);
}

window["WebGLProtein"] = WebGLProtein;
*/
