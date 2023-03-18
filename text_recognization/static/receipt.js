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

var calcCosts = function(itemLen, pLen, json) {
    let costs = new Array(pLen).fill(0);
    // holds the total cost per person for product
    const items = JSON.parse(json);
    //converts python dictionary to js dictionary

    for (let key in items) {
        let ret = Array(pLen).fill(0); //reset
        let count = 0;
        for (let j = 0; j < pLen; j++) {
            if (document.getElementById(String(j) + document.getElementById(key)).checked) {
                ret[j] = 1;
                count++;
            }
        }

        let cost = items[key];
        cost /= count;
        for (let j = 0; j < pLen; j++) {
            if (ret[j] === 1) {
                cost[j] += cost; //accumulate costs
            }
        }
    }
}