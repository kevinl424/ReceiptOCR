var calcCosts = function() {
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
    // write to html
    const names = JSON.parse(jsonNames);
    const target = document.getElementById("breakdown")
    let s = ""
    let counter = 0
    for (let key in names) {
        s += names[key] + ":" + costs[counter] + "  ";
    }
    target.innerHTML = '<h2>' + s + '</h2>';
    return false;
}