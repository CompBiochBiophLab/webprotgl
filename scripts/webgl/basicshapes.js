//<script>

function createGLOpenCylinder(gl, nDivCircle, nDivHeight)
{
  var iV = 8;
  var nV = (nDivCircle * (nDivHeight + 1));
  var iI = 3;
  var nI = 2 * nDivCircle * nDivHeight;
  var vertices = new Float32Array(iV * nV);
  var indices = new Uint16Array(iI * nI);

  for (var h = 0; h < nDivHeight; ++h) {
    for (var a = 0; a < nDivCircle; ++a) {
      var angle = Math.PI * 2. * (a) / (nDivCircle);
      vertices[iV * (h * nDivCircle + a) + 0] = Math.cos(angle);
      vertices[iV * (h * nDivCircle + a) + 1] = Math.sin(angle);
      vertices[iV * (h * nDivCircle + a) + 2] = (h) / (nDivHeight - 1);
      vertices[iV * (h * nDivCircle + a) + 3] = Math.cos(angle);
      vertices[iV * (h * nDivCircle + a) + 4] = Math.sin(angle);
      vertices[iV * (h * nDivCircle + a) + 5] = (h) / (nDivHeight - 1);
      vertices[iV * (h * nDivCircle + a) + 6] = (a) / (nDivCircle);
      vertices[iV * (h * nDivCircle + a) + 7] = (h) / (nDivHeight - 1);

      if (h > 0) {
        var i1 = nDivCircle * (h - 1) + a;
        var i3 = nDivCircle * (h - 0) + a;
        if (a == 0) {
          var i2 = nDivCircle * (h + 0) - 1;
          var i4 = nDivCircle * (h + 1) - 1;
        } else {
          var i2 = nDivCircle * (h - 1) + a - 1;
          var i4 = nDivCircle * (h - 0) + a - 1;
        }
        indices[3 * (2 * nDivCircle * (h - 1) + 2 * a) + 0] = i1;
        indices[3 * (2 * nDivCircle * (h - 1) + 2 * a) + 1] = i2;
        indices[3 * (2 * nDivCircle * (h - 1) + 2 * a) + 2] = i3;
        indices[3 * (2 * nDivCircle * (h - 1) + 2 * a) + 3] = i2;
        indices[3 * (2 * nDivCircle * (h - 1) + 2 * a) + 4] = i4;
        indices[3 * (2 * nDivCircle * (h - 1) + 2 * a) + 5] = i3;
      }
    }
  }
  
  return new Shape(gl, gl.TRIANGLES, vertices, indices, iV, nV, iI, nI);
}

////////////////////////////////////////////////////////////////

function createGLSphere(gl, nIterations)
{
  var iV = 8;
  var p2    = Math.pow(2, nIterations);
  var p22   = p2 * 2;
  var p21   = p2 + 1;
  var p221  = p22 + 1;
  var nV = p21 * p221 + p2 * p22;
  var vertices = new Float32Array(nV * iV);
  var currentLength = 8 * iV;
  var i = 0;
  vertices[i+0] = 0.; vertices[i+1] = 0.; vertices[i+2] = 1.; vertices[i+6] = 0.25;
  vertices[i+3] = 0.; vertices[i+4] = 0.; vertices[i+5] = 1.; vertices[i+7] = 0.5;
  i = 8;
  vertices[i+0] = 1.; vertices[i+1] = 0.; vertices[i+2] = 0.; vertices[i+6] = 0.;
  vertices[i+3] = 1.; vertices[i+4] = 0.; vertices[i+5] = 0.; vertices[i+7] = 1.;
  i = 16;
  vertices[i+0] = 0.; vertices[i+1] = 1.; vertices[i+2] = 0.; vertices[i+6] = 0.;
  vertices[i+3] = 0.; vertices[i+4] = 1.; vertices[i+5] = 0.; vertices[i+7] = 0.;
  i = 24;
  vertices[i+0] = -1.; vertices[i+1] = 0.; vertices[i+2] = 0.; vertices[i+6] = 0.5;
  vertices[i+3] = -1.; vertices[i+4] = 0.; vertices[i+5] = 0.; vertices[i+7] = 0.;
  i = 32;
  vertices[i+0] = 0.; vertices[i+1] = -1.; vertices[i+2] = 0.; vertices[i+6] = 0.5;
  vertices[i+3] = 0.; vertices[i+4] = -1.; vertices[i+5] = 0.; vertices[i+7] = 1.;
  i = 40;
  vertices[i+0] = 1.; vertices[i+1] = 0.; vertices[i+2] = 0.; vertices[i+6] = 1.; // Repeat for texturing
  vertices[i+3] = 1.; vertices[i+4] = 0.; vertices[i+5] = 0.; vertices[i+7] = 1.;
  i = 48;
  vertices[i+0] = 0.; vertices[i+1] = 1.; vertices[i+2] = 0.; vertices[i+6] = 1.; // Repeat for texturing
  vertices[i+3] = 0.; vertices[i+4] = 1.; vertices[i+5] = 0.; vertices[i+7] = 0.;
  i = 56;
  vertices[i+0] = 0.; vertices[i+1] = 0.; vertices[i+2] = -1.; vertices[i+6] = 0.75;
  vertices[i+3] = 0.; vertices[i+4] = 0.; vertices[i+5] = -1.; vertices[i+7] = 0.5;
 
  var nI = 8;
  var iI = 3;
  var indices = new Uint16Array(nI * iI);
  indices[ 0] = 0; indices[ 1] = 1; indices[ 2] = 2;
  indices[ 3] = 7; indices[ 4] = 6; indices[ 5] = 5;
  indices[ 6] = 0; indices[ 7] = 2; indices[ 8] = 3;
  indices[ 9] = 7; indices[10] = 3; indices[11] = 6;
  indices[12] = 0; indices[13] = 3; indices[14] = 4;
  indices[15] = 7; indices[16] = 4; indices[17] = 3;
  indices[18] = 0; indices[19] = 4; indices[20] = 1;
  indices[21] = 7; indices[22] = 5; indices[23] = 4;

  for (var ref = 0; ref < nIterations; ++ref) {
    var vertexSize = currentLength;
    var indexSize = indices.length;
    var mapMiddle = {};

    nI *= 4;
    var oldIndices = indices;
    indices = new Uint16Array(nI * iI);
    var currentIndex = 0;

    // Add vertices
    for (var index = 0; index < indexSize; index += iI) {
      var iold = [];
      iold[0] = oldIndices[index+0];
      iold[1] = oldIndices[index+1];
      iold[2] = oldIndices[index+2];
      var totalSwap = 0;
      if (iold[0] > iold[1]) { iold[3] = iold[0]; iold[0] = iold[1]; iold[1] = iold[3]; }
      if (iold[0] > iold[2]) { iold[3] = iold[0]; iold[0] = iold[2]; iold[2] = iold[3]; }
      if (iold[1] > iold[2]) { iold[3] = iold[1]; iold[1] = iold[2]; iold[2] = iold[3]; }

      var inew = [];
      for (var i = 0; i < 3; ++i) {
        var a = iold[i];
        var b = a;
        if (i == 2) {
          a = iold[0];
        } else {
          b = iold[i+1];
        }

        var it = mapMiddle[[a, b]];
        if (it) {
          inew[i] = it;
        } else {
          // Add index
          inew[i] = currentLength / 8;
          mapMiddle[[a, b]] = inew[i];

          // Add a vertex
          var off1 = a * iV;
          var x1 = [vertices[off1 + 0], vertices[off1 + 1], vertices[off1 + 2], vertices[off1 + 6], vertices[off1 + 7]];
          var off2 = b * iV;
          var x2 = [vertices[off2 + 0], vertices[off2 + 1], vertices[off2 + 2], vertices[off2 + 6], vertices[off2 + 7]];
          var vNew = [x1[0] + x2[0], x1[1] + x2[1], x1[2] + x2[2]];
          var tNew = [(x1[3] + x2[3]) * 0.5, (x1[4] + x2[4]) * 0.5];
          var norm = vNew[0] * vNew[0] + vNew[1] * vNew[1] + vNew[2] * vNew[2];
          norm = Math.sqrt(norm);
          vertices[currentLength+0] = vNew[0] / norm;
          vertices[currentLength+1] = vNew[1] / norm;
          vertices[currentLength+2] = vNew[2] / norm;
          vertices[currentLength+3] = vNew[0] / norm;
          vertices[currentLength+4] = vNew[1] / norm;
          vertices[currentLength+5] = vNew[2] / norm;
          vertices[currentLength+6] = tNew[0];
          vertices[currentLength+7] = tNew[1];
          currentLength += 8;
        }
      }

        // Add all 4 new triangles
      if (totalSwap % 2) { // Change direction!
        indices[currentIndex++] = inew[2];
        indices[currentIndex++] = inew[0];
        indices[currentIndex++] = iold[0];

        indices[currentIndex++] = inew[0];
        indices[currentIndex++] = inew[1];
        indices[currentIndex++] = iold[1];

        indices[currentIndex++] = inew[1];
        indices[currentIndex++] = inew[2];
        indices[currentIndex++] = iold[2];

        indices[currentIndex++] = inew[0];
        indices[currentIndex++] = inew[2];
        indices[currentIndex++] = inew[1];
      } else {
        indices[currentIndex++] = inew[2];
        indices[currentIndex++] = iold[0];
        indices[currentIndex++] = inew[0];

        indices[currentIndex++] = inew[0];
        indices[currentIndex++] = iold[1];
        indices[currentIndex++] = inew[1];

        indices[currentIndex++] = inew[1];
        indices[currentIndex++] = iold[2];
        indices[currentIndex++] = inew[2];

        indices[currentIndex++] = inew[0];
        indices[currentIndex++] = inew[1];
        indices[currentIndex++] = inew[2];
      }
    }
  }
  
  return new Shape(gl, gl.TRIANGLES, vertices, indices, iV, nV, iI, nI);
}
