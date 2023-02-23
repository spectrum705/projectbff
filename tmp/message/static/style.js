let processScroll = () => {
  let docElem = document.documentElement, 
    docBody = document.body,
    scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
      scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - window.innerHeight,
    scrollPercent = scrollTop / scrollBottom * 100 + '%';
  
  // console.log(scrollTop + ' / ' + scrollBottom + ' / ' + scrollPercent);
  
    document.getElementById("progress-bar").style.setProperty("--scrollAmount", scrollPercent); 
}

document.addEventListener('scroll', processScroll);
// trying to remember the scroll position 
// document.location.reload(true)
// get scrop position
// let scrollPosition = document.documentElement.scrollTop;
// console.log(scrollPosition);


// set scroll position

// window.onscroll = function() {
//   window.scrollTo(0,0);
// };
