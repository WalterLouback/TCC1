function generateValTable(multiline = true) {
    let paraValues = [];
    for (let i = 0; i < global.outputParameters.length; i++) {
        let tValues = [];
        let tindex = 0;
        let l = multiline ? global.nodeList.length : 1;
        for (let j = 0; j < l; j++) {
            //注意第一个循环条件，index超出界限了就不需要再寻找了，其他的全是空
            if (tindex < global.outputParameters[i]["exampleValues"].length && global.outputParameters[i]["exampleValues"][tindex]["num"] == j) {
                tValues.push(global.outputParameters[i]["exampleValues"][tindex]["value"]);
                tindex++;
            } else {
                tValues.push(" ");
            }
        }
        paraValues.push(tValues);
    }
    global.app._data.valTable = paraValues;
    // console.log("生成参数表格", paraValues);
}