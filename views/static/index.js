function newFile() {
    var pad = window.prompt("Name of new pad:", "");
    if (pad == null || pad.length == 0) {
        return false;
    }
    window.location = "/p/" + pad;
}