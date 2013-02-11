//<script>

function Shape(gl, type, vertices, indices, floatsPerVertex, numVertices, pointsPerShape, numShapes)
{
  var type_ = type;
  var vertices_ = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vertices_);
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
  vertices_.itemSize = floatsPerVertex;
  vertices_.numItems = numVertices;

  var indices_ = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indices_);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW);
  indices_.itemSize = pointsPerShape;
  indices_.numItems = numShapes;

  var bbox_ = new BBox();
  for (var i = 0; i < numVertices; ++i) {
    var offset = i * floatsPerVertex;
    bbox_.include([vertices[offset+0], vertices[offset+1], vertices[offset+2]]);
  }

  this.bind = function(gl) {
    gl.bindBuffer(gl.ARRAY_BUFFER, vertices_);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indices_);
  }

  this.getBoundingBox = function() {
    return bbox_;
  }

  this.getBufferStride = function()
  {
    return vertices_.itemSize * 4;
  }

  this.getIndicesCount = function()
  {
    return indices_.numItems * indices_.itemSize;
  }

  this.getIndices  = function() { return indices_ ; }
  this.getVertices = function() { return vertices_; }
  this.getType     = function() { return type_; }
}
