//<script>

function Mouse(canvas)
{
  var that = this;

  var canvas_ = canvas;
  document.addEventListener('mousedown',   function(event) { onDocumentMouseDown(event);  }, false);
  document.addEventListener('mouseup',     function(event) { onDocumentMouseUp(event);    }, false);
  document.addEventListener('mousemove',   function(event) { onDocumentMouseMove(event);  }, false);
  document.addEventListener('mousewheel',  function(event) { onDocumentMouseWheel(event); }, false);
  // Firefox
  document.addEventListener('DOMMouseScroll',  function(event) { onDocumentMouseWheel(event); }, false);

  function MouseHandler()
  {
    this.execute = function(x, y, last) {}
  }

  function LeftHandler(x, y)
  {
    MouseHandler.apply(this);

    startX = x;
    startY = y;

    this.execute = function(x, y, last)
    {
      gCamera.turn((x - startX) / 100., !last);
      gCamera.lift((y - startY) / 100., !last);
    }
  }

  LeftHandler.prototype = new MouseHandler();

  var mouseHandler = null;

////////////////////////////////////////////////////////////////

  // TODO: anything better than this ? Does it always work ?
  var event2X = function(event) { return event.clientX - canvas.offsetLeft; }
  var event2Y = function(event) { return event.clientY - canvas.offsetTop; }

////////////////////////////////////////////////////////////////

  onDocumentMouseDown = function(event)
  {
    if (event.button == 0)
    {
      mouseHandler = new LeftHandler(event2X(event), event2Y(event));
    }
  }

////////////////////////////////////////////////////////////////

  onDocumentMouseMove = function(event)
  {
    if (mouseHandler != null)
    {
      mouseHandler.execute(event2X(event), event2Y(event), false);
    }
  }

////////////////////////////////////////////////////////////////

  onDocumentMouseUp = function(event)
  {
    if (mouseHandler != null)
    {
      mouseHandler.execute(event2X(event), event2Y(event), true);

      // Unregister handler
      mouseHandler = null;
    }
  }

////////////////////////////////////////////////////////////////

  onDocumentMouseWheel = function(event)
  {
    var fwd = true;
    if ('wheelDelta' in event)
      fwd = event.wheelDelta >= 0;
    else
      fwd = event.detail <= 0;

    if (fwd)
      gCamera.stepForward();
    else
      gCamera.stepBackward();
  }

////////////////////////////////////////////////////////////////

}
