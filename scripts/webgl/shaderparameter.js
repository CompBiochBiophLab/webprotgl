//<script>

function ShaderParameter(type, value)
{
  var type_ = type;
  var value_ = value;

  this.bind = function(shader, name) {
    switch (type_) {
      case 0:
        shader.setUniform(name, value_);
        break;
      case 1:
        shader.setUniformVector(name, value_);
        break;
      default:
        break;
    }
  }

  this.getValue = function() {
    return value_;
  }
}

function createFloatParameter(value) {
  return new ShaderParameter(0, value);
}

function createVectorParameter(array) {
  var v = new Float32Array(array.length);
  for (var i = 0; i < array.length; ++i) {
    v[i] = array[i];
  }
  return new ShaderParameter(1, v);
}


function createVec3Parameter(x, y, z) {
  var v = new Float32Array(3);
  v[0] = x; v[1] = y; v[2] = z;
  return new ShaderParameter(1, v);
}

function createVec4Parameter(a, b, c, d) {
  var v = new Float32Array(4);
  v[0] = a; v[1] = b; v[2] = c; v[3] = d;
  return new ShaderParameter(1, v);
}
