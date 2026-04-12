function clearEl(trail=false) {
    //如果最后停留的元素被选中，则调整此元素的style为原始style，否则不进行调整
    for (let node of global.nodeList) {
        node["node"].style.backgroundColor = node["bgColor"];
        node["node"].style.boxShadow = node["boxShadow"];
        if (global.NowNode == node["node"] && !trail) ;
    }
    for (let node of global.markElements) {
        let element = node.element;
        element.style.boxShadow = "none";
    }
    global.markElements = [];
    global.step = 0;
    clearReady();
    clearParameters();
    global.nodeList.splice(0, global.nodeList.length); //清空数组
    global.app._data.option = 0; //选项重置
    global.app._data.page = 0; //恢复原始页面
    // global.app._data.nextPage = 0; //不出现翻页操作提示
}