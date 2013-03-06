//<script>

function TargetRotationHandler(camera, target, position, baseHandler)
{
  this.onActivate = function(mouse) {
    if (mouse.evt_ == "up") {
      camera_.setMouseHandler(default_);
      //TODO: save changes
    }

    var diff = [mouse.screenX - start_[0], mouse.screenY - start_[1]];
    if (diff[0] == 0. && diff[1] == 0.) {
      camera_.lookAt([eye0_[0] + target_[0], eye0_[1] + target_[1], eye0_[2] + target_[2]], direction0_, up0_);
      return;
    }

    var axis = [up0_[0] * diff[0] + right0_[0] * diff[1],
                up0_[1] * diff[0] + right0_[1] * diff[1],
                up0_[2] * diff[0] + right0_[2] * diff[1]];
    var angle = -Math.sqrt(diff[0] * diff[0] + diff[1] * diff[1]) * 0.005;

    var rot = [];
    tdl.fast.matrix4.axisRotation(rot, axis, angle);
    var temp = [0., 0., 0., 0.];
    var newEye = [];
    tdl.fast.columnMajor.mulMatrix4Vector(temp, rot, eye0_);
    tdl.fast.addVector(newEye, temp, target_);

    var newTgt = [];
    tdl.fast.columnMajor.mulMatrix4Vector(newTgt, rot, direction0_);

    var newUp = [];
    tdl.fast.columnMajor.mulMatrix4Vector(newUp, rot, up0_);

    camera_.lookAt(newEye, newTgt, newUp);
  }

  var camera_ = camera;
  var default_ = baseHandler;
  var target_ = target;
  var start_ = position;
  cam0_ = camera.getLookAt();
  var eye0_ = [cam0_[0][0] - target_[0], cam0_[0][1] - target_[1], cam0_[0][2] - target_[2], 0.];
  var direction0_ = [cam0_[1][0], cam0_[1][1], cam0_[1][2], 0.];
  var up0_ = [cam0_[2][0], cam0_[2][1], cam0_[2][2], 0.];
  var right0_ = [];
  tdl.fast.cross(right0_, direction0_, up0_);
  tdl.fast.normalize(right0_, right0_);
}

function CameraMovementManager(camera, stepSize)
{
  this.onActivate = function(mouse) {
    switch (mouse.evt_) {
      case "wheelUp":
        camera_.step(stepSize_);
        break;
      case "wheelDown":
        camera_.step(-stepSize_);
        break;
      case "down":
        switch (mouse.button) {
          case 0: // Left
            camera_.setMouseHandler(new TargetRotationHandler(camera_, target_.getBarycenter(), [mouse.screenX, mouse.screenY], that));
            break;
          case 1: // Middle
            break;
          case 2: // Right
            break;
        }
        break;
      default:
        camera_.castRay([mouse.screenX, mouse.screenY]);
        break;
    }
  }

  this.setTarget = function(target) {
    target_ = target;
  }

  var that = this;
  var camera_ = camera;
  var stepSize_ = stepSize;
  var target_;
}

function MovementManager(camera)
{
  var camera_ = camera;

  camera_.setMouseHandler(new CameraMovementManager(camera_, 1.));

  document.addEventListener('mousedown',   function(event) { onMouseDown(event);  }, false);
  document.addEventListener('mouseup',     function(event) { onMouseUp(event);    }, false);
  document.addEventListener('mousemove',   function(event) { onMouseMove(event);  }, false);
  document.addEventListener('mousewheel',  function(event) { onMouseWheel(event); }, false);
  // Firefox
  document.addEventListener('DOMMouseScroll',  function(event) { onMouseWheel(event); }, false);

  //onMouseDown  = function(event) { console.log(event);console.log(event.button);console.log(event.buttons);camera_.onMouseEvent("down"); }
  onMouseDown  = function(event) { event.evt_ = "down"; camera_.onMouseEvent(event); }
  onMouseUp    = function(event) { event.evt_ = "up"; camera_.onMouseEvent(event); }
  onMouseMove  = function(event) { event.evt_ = "move"; camera_.onMouseEvent(event); }
  onMouseWheel = function(event) {
    if (event.wheelDelta) {
      if (event.wheelDelta > 0)
        event.evt_ = "wheelUp";
      else
        event.evt_ = "wheelDown";
    } else if (event.detail < 0) {
      event.evt_ = "wheelUp";
    } else {
      event.evt_ = "wheelDown";
    }

    camera_.onMouseEvent(event);
  }
}
