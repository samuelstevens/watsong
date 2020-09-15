function getCenter(elem) {
  const { top, left, width } = elem.getBoundingClientRect();
  // return { y: top, x: left };
  return { y: top + width / 2, x: left + width / 2 };
}

function getCoord(event) {
  if (event.clientX && event.clientY) {
    return { x: event.clientX, y: event.clientY };
  }

  // return coordinates of first touch
  if (event.touches && event.touches.length > 0) {
    const firstTouch = event.touches[0];

    return { x: firstTouch.clientX, y: firstTouch.clientY };
  }
}


function makeElemTwistable(elem) {
  var currentAngle = 0, prevAngle = 0, initialAngle = 0;

  elem.onmousedown = twistStart;
  elem.ontouchstart = twistStart;

  const center = getCenter(elem);



  function twistStart(event) {
    event = event || window.event;
    event.preventDefault();

    const { x, y } = getCoord(event);

    initialAngle = Math.atan2(x - center.x, y - center.y);

    document.onmouseup = stopTwisting;
    document.onmousemove = twistElement;

    document.ontouchend = stopTwisting;
    document.ontouchmove = twistElement;
  }

  function twistElement(event) {
    event = event || window.event;
    event.preventDefault();

    const { x, y } = getCoord(event);

    const newAngle = Math.atan2(x - center.x, y - center.y);

    currentAngle = -(prevAngle + newAngle - initialAngle);

    $(elem).css("transform", `rotate(${currentAngle}rad)`);
  }

  function stopTwisting() {
    // stop twisting when mouse button is released
    document.onmouseup = null;
    document.onmousemove = null;

    document.ontouchend = null;
    document.ontouchmove = null;

    prevAngle = -currentAngle;
  }
}

$.each($('.dial > div'), function (_, elem) {
  makeElemTwistable(elem);
});
