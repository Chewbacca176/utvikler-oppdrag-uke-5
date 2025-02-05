function epilepi(){
    console.log("called epi");
    
    // const wrapper = document.querySelector(".bestillinger_box")
    let boxes = document.querySelectorAll(".bestillinger_boxbox")
    setInterval(function test() {
        for (let i = 0; i < boxes.length; i++) {
            console.log("in for loop");
            boxes[i].style.backgroundColor = getRandomColor()
            document.body.style.backgroundColor = getRandomColor()
        }
        // boxes[i].animation
        // console.log(boxes[i])
        // boxes[i].style.animationDelay = `${i * 0.2}s`;
        // boxes[i].style.animationDuration = '1s';
    }, 5);
    // open('/sebestillinger', "new", "height=10, width=10")
    // open('/sebestillinger');
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

document.addEventListener('DOMContentLoaded', function() {epilepi();});

function tilbakemelding_knapp() {
    console.log("called tilbakemelding_knapp")
    document.querySelector('.tilbakemelding').style.visibility = 'visible'; 
} 

function admin_passord() {
   document.querySelector('.admin_passord').classList.toggle("hide")
} 

function nullstill() {
    document.querySelector('.tilbakemelding').style.visibility = 'hidden'; 
}

function test1() {
    console.log("called test1");
}

document.querySelector('#admin').addEventListener("click", function() {admin_passord();})