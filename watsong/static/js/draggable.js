/**
 * getCenter returns the center of an HTML element in x-y coordinates.
 *
 * @param {HTMLElement} elem element to find the center of
 * @return {{x: number, y: number}} center of elem in as object with .x and .y
 */
function getCenter(elem) {
  const { top, left, width } = elem.getBoundingClientRect();
  return { y: top + width / 2, x: left + width / 2 };
}

/**
 *  getCoord returns the position of a touch or click event
 *
 * @param event touch/mouse event
 * @return {{x: number, y: number}} position of touch or click with .x and .y
 */
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

/**
 * initializeDial makes the DOM element twistable and sends HTTP request when the twisting stops.
 *
 * @param {HTMLElement} elem is the `div` element that contains the image.
 * @param {string} dialName is the dial name to be sent to the backend
 */
function initializeDial(elem, dialName) {
  var currentAngle = 0, prevAngle = 0, initialAngle = 0;

  elem.onmousedown = onTwistStart;
  elem.ontouchstart = onTwistStart;

  const center = getCenter(elem);

  /**
   * onTwistStart is called when a user touches or clicks down on `elem`
   *
   * @param {Event} event touch/mouse event
   */
  function onTwistStart(event) {
    event = event || window.event;
    event.preventDefault();

    const { x, y } = getCoord(event);

    initialAngle = Math.atan2(x - center.x, y - center.y);

    document.onmouseup = onStopTwisting;
    document.onmousemove = onTwist;

    document.ontouchend = onStopTwisting;
    document.ontouchmove = onTwist;
  }

  /**
   * onTwist is called when a mouse moves while clicked, or dragged via touch.
   *
   * @param {Event} event touch/mouse event
   */
  function onTwist(event) {
    event = event || window.event;
    event.preventDefault();

    const { x, y } = getCoord(event);

    const newAngle = Math.atan2(x - center.x, y - center.y);

    currentAngle = -(prevAngle + newAngle - initialAngle);

    $(elem).css("transform", `rotate(${currentAngle}rad)`);
  }


  /**
   * onStopTwisting is called when a user lets go of the dial (`elem`)
   */
  function onStopTwisting() {
    // stop twisting when mouse button is released
    document.onmouseup = null;
    document.onmousemove = null;

    document.ontouchend = null;
    document.ontouchmove = null;

    prevAngle = -currentAngle;

    const level = (1.5 + (currentAngle % (2 * Math.PI)) / (2 * Math.PI)) % 1.0;

    $.getJSON($SCRIPT_ROOT + '/jukebox/filter', {
      [dialName]: level
    }, function (data) {
      console.log(data);
    });
  }
}

$.each($('.dial'), function (_, elem) {
  const dial = $(elem).children('div')[0];
  initializeDial(dial, elem.id);
});
