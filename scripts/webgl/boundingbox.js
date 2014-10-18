//<script>

function BBox()
{
  this.equals = function(bbox) {
    for (var i = 0; i < 3; ++i) {
      if (min_[i] != bbox.getMin()[i])
        return false;
      if (max_[i] != bbox.getMax()[i])
        return false;
    }

    return true;
  }

////////////////////////////////////////////////////////////////

  this.getCenter = function() {
    var b = [(min_[0] + max_[0]) * 0.5, (min_[1] + max_[1]) * 0.5, (min_[2] + max_[2]) * 0.5];
    return b;
  }

////////////////////////////////////////////////////////////////

  this.getMax = function() {
    return max_;
  }

////////////////////////////////////////////////////////////////

  this.getMin = function() {
    return min_;
  }

////////////////////////////////////////////////////////////////

  this.include = function(v) {
    var changed = false;

    for (var i = 0; i < 3; ++i) {
      if (v[i] < min_[i]) {
        min_[i] = v[i];
        changed = true;
      }
      if (v[i] > max_[i]) {
        max_[i] = v[i];
        changed = true;
      }
    }

    return changed;
  }

////////////////////////////////////////////////////////////////

  this.includeBBox = function(bbox) {
    if (bbox.isEmpty())
      return false;

    var changed = that.include(bbox.getMin());
    changed |= that.include(bbox.getMax());
    return changed;
  }

////////////////////////////////////////////////////////////////

  this.intersects = function(ray) {
    if (that.isEmpty())
      return -1.;

    var tIn = -Number.MAX_VALUE;
    var tOut = Number.MAX_VALUE;

    for (var axis = 0; axis < 3; ++axis) {
      if (ray[1][axis] == 0.) {
        if (ray[0][axis] < min_[axis] || ray[0][axis] > max_[axis])
          return -1;
      } else {
        var locIn = (min_[axis] - ray[0][axis]) / ray[1][axis];
        var locOut = (max_[axis] - ray[0][axis]) / ray[1][axis];

        if (locIn <= 0. && locOut <= 0.)
          return -1;

        if (locIn > locOut) {
          var tmp = locIn;
          locIn = locOut;
          locOut = tmp;
        }

        if (locIn > tIn)
          tIn = locIn;
        if (locOut < tOut)
          tOut = locOut;
      }
    }

    if (tIn < tOut)
      return tIn;

    return -1;
  }

////////////////////////////////////////////////////////////////

  this.isEmpty = function() {
    return min_[0] > max_[0];
  }

////////////////////////////////////////////////////////////////

  this.multiply = function(matrix) {
    if (that.isEmpty())
      return that;

    var xMin = matrix[3] * min_[0] + matrix[7] * min_[1] + matrix[11] * min_[2] + matrix[15];
    var xMax = matrix[3] * max_[0] + matrix[7] * max_[1] + matrix[11] * max_[2] + matrix[15];

    var min = [ (matrix[0] * min_[0] + matrix[ 4] * min_[1] + matrix[ 8] * min_[2] + matrix[12]) / xMin
              , (matrix[1] * min_[0] + matrix[ 5] * min_[1] + matrix[ 9] * min_[2] + matrix[13]) / xMin
              , (matrix[2] * min_[0] + matrix[ 6] * min_[1] + matrix[10] * min_[2] + matrix[14]) / xMin];
    var max = [ (matrix[0] * max_[0] + matrix[ 4] * max_[1] + matrix[ 8] * max_[2] + matrix[12]) / xMax
              , (matrix[1] * max_[0] + matrix[ 5] * max_[1] + matrix[ 9] * max_[2] + matrix[13]) / xMax
              , (matrix[2] * max_[0] + matrix[ 6] * max_[1] + matrix[10] * max_[2] + matrix[14]) / xMax];

    var bbox = new BBox();
    bbox.include(min);
    bbox.include(max);

    return bbox;
  }

////////////////////////////////////////////////////////////////

  var min_ = [ Number.MAX_VALUE,  Number.MAX_VALUE,  Number.MAX_VALUE];
  var max_ = [-Number.MAX_VALUE, -Number.MAX_VALUE, -Number.MAX_VALUE];
  var that = this;
}
