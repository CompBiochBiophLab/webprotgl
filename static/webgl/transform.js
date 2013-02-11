//<script>

function Transform()
{
  var that = this;
  var bbox_ = new BBox();
  var visible_ = true;
  var selectable_ = true;
  var shader_;
  var parent_;
  var world_ = new Float32Array(16);
  tdl.fast.matrix4.identity(world_);
  var local_ = new Float32Array(16);
  tdl.fast.matrix4.identity(local_);
  var shapes_ = [];
  var children_ = [];
  var params_ = {};

  this.addChild = function() {
    var child = new Transform();
    child.setParent(that);
    child.updateWorldMatrix(world_, false);
    children_.push(child);
    return child;
  }

  this.addShape = function(shape) {
    shapes_.push(shape);
    //if (parent_ && bbox_.include(shape.getBoundingBox().multiply(world_))) {
    if (bbox_.includeBBox(shape.getBoundingBox().multiply(world_)) && parent_) {
      parent_.updateBoundingBox(true);
    }
  }

  this.clear = function() {
    bbox_ = new BBox();
    visible_ = true;
    selectable_ = true;
    parent_ = null;
    tdl.fast.matrix4.identity(world_);
    tdl.fast.matrix4.identity(local_);
    shapes_ = [];
    children_ = [];
    params_ = {};
  }

  this.findParameter = function(name) {
    var p = params_[name];
    if (p)
      return p;

    if (parent_)
      return parent_.findParameter(name);

    return null;
  }

  this.getBoundingBox = function() {
    return bbox_;
  }

  this.getShader = function() {
    if (shader_)
      return shader_;

    if (parent_)
      return parent_.getShader();

    throw new Error("No shader in tree!");
  }

  this.getWorldMatrix = function() {
    return world_;
  }

  this.display = function(camera, eye, gl) {
    if (!visible_)
      return;

    if (shapes_.length > 0) {
      var shader = this.getShader();
      if (!shader.bind())
        return;
      shader.setM4Uniform(gl, "cameraMatrix",  camera);
      shader.setM4Uniform(gl, "worldMatrix",   world_);
      shader.setUniformVector("eye",           eye);

      // TODO Bind more parameters if necessary...
      var parameters = shader.getParameters();
      for (p in parameters) {
        var x = that.findParameter(p);
        if (!x)
          x = parameters[p];
        x.bind(shader, p);
      }

      for (i in shapes_) {
        shapes_[i].bind(gl);
//        gl.bindBuffer(gl.ARRAY_BUFFER, shapes_[i].getVertices());

        shader.bindPositions(3, shapes_[i].getBufferStride(), 0);
        shader.bindNormals(3, shapes_[i].getBufferStride(), 0);
        shader.bindColours(2, shapes_[i].getBufferStride(), 24);
//        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, shapes_[i].getIndices());

        gl.drawElements(shapes_[i].getType(), shapes_[i].getIndicesCount(), gl.UNSIGNED_SHORT, 0);
      }
    }

    for (i in children_) {
      children_[i].display(camera, eye, gl);
    }
  }

  this.setParameter = function(name, param) {
    params_[name] = param;
  }

  this.setParent = function(mum) {
    parent_ = mum;
  }

  this.setShader = function(shader) {
    shader_ = shader;
  }

  this.setVisibility = function(isVisible) {
    visible_ = isVisible;
  }

  this.translate = function(position) {
    local_ = tdl.fast.matrix4.translate(local_, position);
    that.updateWorldMatrix0();
  }

  this.updateBoundingBox = function(updateParent) {
    var clearBox = new BBox();
    for (i in children_) {
      clearBox.includeBBox(children_[i].getBoundingBox());
    }

    for (i in shapes_) {
      clearBox.includeBBox(shapes_[i].getBoundingBox().multiply(world_));
    }

    if (!clearBox.equals(bbox_)) {
      bbox_ = clearBox;
      if (parent_)
        parent_.updateBoundingBox(true);
    }
  }

  this.updateWorldMatrix0 = function() {
    if (!parent_) {
      world_.set(local_);
    } else {
      tdl.fast.mulMatrixMatrix4(world_, parent_.getWorldMatrix(), local_);
    }

    for (i in children_)
      children_[i].updateWorldMatrix(world_, false);

    that.updateBoundingBox(true);
  }

  this.updateWorldMatrix = function(matrix, updateParentBBox) {
    tdl.fast.matrix4.mul(world_, matrix, local_);
    for (child in children_) {
      children_[child].updateWorldMatrix(world_, false);
    }

    that.updateBoundingBox(updateParentBBox);
  }
}
