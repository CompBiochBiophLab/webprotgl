//<script>

function Camera(canvas)
{
  var that = this;

  var gl_ = null;

  initPerspective = function (canvas) {
    var names = ["webgl", "experimental-webgl", "webkit-3d", "moz-webgl"];
    for (var ii = 0; ii < names.length; ++ii) // > close fake bracket
    {
      gl_ = canvas.getContext(names[ii]);
      if (gl_ == null)
        continue;

      gl_.viewportWidth = canvas.width;
      gl_.viewportHeight = canvas.height;
      gl_.viewport(0, 0, gl_.viewportWidth, gl_.viewportHeight);

      gl_.clearColor(0.0, 0.5, 0.8, 1.0);
      gl_.enable(gl_.DEPTH_TEST);
      gl_.blendFunc(gl_.SRC_ALPHA, gl_.ONE_MINUS_SRC_ALPHA);
//      gl_.enable(gl_.BLEND);

      return new Float32Array(16);
    }

    throw("WebGL could not be initialised");
  }

  var aperture_   = 1.047197551; // 60 deg
  var near_       = 1e-1;//1e-5;
  var far_        = 100000.;//1e4;
  var eye_        = [0., 0., 50.];
  var direction_  = [0., 0., -1.];
  var up_         = [0., 1., 0.];
  var right_      = [1., 0., 0.];
  var tanHalfAperture_  = Math.tan(aperture_ * 0.5);

  var handler_;
  var persp_ = initPerspective(canvas);
  var lookAt_ = new Float32Array(16);
  var scene_ = new Transform();

////////////////////////////////////////////////////////////////
// Main function (display to screen)
////////////////////////////////////////////////////////////////

  this.castRay = function(mouse)
  {
    r = [0., 0., 0.];
    u = [0., 0., 0.];
    dir = [0., 0., 0.];
    tdl.fast.mulScalarVector(r, mouse[0] * tanHalfAperture_ * gl_.viewportWidth / gl_.viewportHeight, right_);
    tdl.fast.mulScalarVector(u, mouse[1] * tanHalfAperture_, up_);
    tdl.fast.addVector(dir, direction_, r);
    tdl.fast.addVector(dir, dir, u);
    
    //console.log("Mou [" + mouse[0] + ", " + mouse[1] + "] " + tanHalfAperture_);
    //console.log("GL  [" + gl_.viewportWidth + ", " + gl_.viewportHeight + "]");
    //console.log("Pos [" + eye_[0] + ", " + eye_[1] + ", " + eye_[2] + "]");
    //console.log("Dir [" + dir[0] + ", " + dir[1] + ", " + dir[2] + "]");
    return scene_.castRay([eye_, dir]);
    //rayDir = direction_ + tdl.fast.right_
  }
  
////////////////////////////////////////////////////////////////

  this.display = function()
  {
    gl_.clear(gl_.COLOR_BUFFER_BIT | gl_.DEPTH_BUFFER_BIT);

    // Perspective matrix
    tdl.fast.matrix4.perspective(persp_, aperture_, gl_.viewportWidth / gl_.viewportHeight, near_, far_);
    // Look at: TODO: eye + direction. Use vectors !!!
    target = [0., 0., 0.];
    tdl.fast.addVector(target, eye_, direction_);
    tdl.fast.matrix4.lookAt(lookAt_, eye_, target, up_);
    tdl.fast.matrix4.mul(lookAt_, lookAt_, persp_);

    scene_.display(lookAt_, eye_, gl_);
  }

////////////////////////////////////////////////////////////////

  this.getGLContext = function() { return gl_; }
  this.getGLScene = function() { return scene_; }

  this.getLookAt = function() {
    return [eye_, direction_, up_];
    //return [eye_, [eye_[0] + direction_[0], eye_[1] + direction_[1], eye_[2] + direction_[2]], up_];
  }

//  this.lookAt = function(eye, target, up) {
  this.lookAt = function(eye, direction, up) {
    for (var i = 0; i < 3; ++i) {
      eye_[i] = eye[i];
  //    direction_[i] = target[i] - eye[i];
      direction_[i] = direction[i];
      up_[i] = up[i];
    }

    tdl.fast.normalize(direction_, direction_);
    tdl.fast.normalize(up_, up_);
    tdl.fast.cross(right_, direction_, up_);
  }

////////////////////////////////////////////////////////////////

  this.onMouseEvent = function(mouse) {
    if (handler_)
      handler_.onActivate(mouse);
  }

////////////////////////////////////////////////////////////////

  this.setMouseHandler = function(handler) {
    handler_ = handler;
  }

////////////////////////////////////////////////////////////////
// Translation along the direction_ axis
////////////////////////////////////////////////////////////////

  this.step = function(size)
  {
    eye_[0] += size * direction_[0];
    eye_[1] += size * direction_[1];
    eye_[2] += size * direction_[2];
  }

  this.setTargetObject = function(target) {
    if (handler_)
      handler_.setTarget(target);

    // Move eye to see whole target
  }
  //TODO: verify what is next !!!

////////////////////////////////////////////////////////////////
// Rotation around the left_ axis
////////////////////////////////////////////////////////////////
/*
  this.lift = function(angle, temporary)
  {
    if (temporary)
      temporaryUp_ = angle;
    else
    {
      temporaryUp_ = 0.;
      currentUp_ = Math.min(Math.max(currentUp_ + angle, -maxUp_), maxUp_);
    }

    update();
  }

////////////////////////////////////////////////////////////////
// Rotation around the up_ axis
////////////////////////////////////////////////////////////////

  this.turn = function(angle, temporary)
  {
    if (temporary)
      temporaryAngle_ = angle;
    else
    {
      var c = Math.cos(angle);
      var s = Math.sin(angle);
      var a = direction_[0];
      var b = direction_[1];
      direction_[0] = c*a + s*b;
      direction_[1] = c*b - s*a;

      temporaryAngle_ = 0.;
    }

    update();
  }

////////////////////////////////////////////////////////////////

  var update = function()
  {
    tdl.fast.identity4(matrix_);
    tdl.fast.addVector(target_, eye_, direction_);
    tdl.fast.matrix4.lookAt(matrix_, eye_, target_, up_);

    var minEye = new Float32Array(3);
    tdl.fast.negativeVector(minEye, eye_);

    tdl.fast.matrix4.translate(matrix_, eye_);
    var aLift = Math.min(Math.max(currentUp_ + temporaryUp_, -maxUp_), maxUp_);
    tdl.fast.matrix4.axisRotate(matrix_, [direction_[1], -direction_[0], 0.], aLift);
    if (temporaryAngle_ != 0.)
      tdl.fast.matrix4.axisRotate(matrix_, up_, temporaryAngle_);
    tdl.fast.matrix4.translate(matrix_, minEye);

    // TODO: ask for new frame rendering !
  }
*/
////////////////////////////////////////////////////////////////

}
