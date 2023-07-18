var url = "";
var loadFile = function(event) { //initialized beforehand, hoisting
    var image = document.getElementById('output');
    url = URL.createObjectURL(event.target.files[0]);
    image.src = url;
};

var getNames = function() {
    var num = document.getElementById('number');
    num = num.value;
    const location = document.getElementById('namesSection');
    let htmlString = "";
    
    location.innerHTML = "";

    for (let i = 0; i < num; i++) {
        htmlString += `<div class="names"> <label for="p${i + 1}name">Person ${i + 1} name:</label> <input type="text" id="p${i + 1}name" name="p${i + 1}name"> </div>`
    }
    location.innerHTML = htmlString;

}

var lockNames = function(event) {
    // event.preventDefault();
    const names = document.querySelectorAll(".names")
    const test = document.getElementById('test');

    for (let i = 0; i < names.length; i++) {
        var location = document.getElementById(`p${i + 1}name`);
        // console.log(location.value);
        test.innerHTML += location.value;
    }

    // const test = document.getElementById('test');
    // test.innerHTML = document.getElementById('p1name').value
}
