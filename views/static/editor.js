var editor = document.getElementById('editor');
var viewer = document.getElementById('viewer');

function updateViewer() {
    viewer.innerHTML = marked(editor.innerText);
    viewer.scrollTop = viewer.scrollHeight;
}
editor.onkeyup = updateViewer;
updateViewer();

function saveFile() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL + '/save', false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("data=" + editor.innerText);
    window.alert(xhr.responseText);
}

function renameFile() {
    if (!window.confirm('Be sure you have saved your work!')) {
        return false;
    }
    var newpad = window.prompt('Enter the name of the new pad:', '');
    if (newpad == null || newpad.length == 0) {
        return false;
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", document.URL + '/rename/' + newpad, false)
    xhr.send();
    if (xhr.responseText == "The operation succeeded!") {
        window.location = "/p/" + newpad;
    } else {
        window.alert(xhr.responseText);
    }
}

function publishFile() {
    var xhr = new XMLHttpRequest();
    if (published) {
        xhr.open("POST", document.URL + '/unpublish', false);
        xhr.send();
        if (xhr.responseText == "This pad is no longer available for viewing!") {
            document.getElementById("publishbutton").value = "Publish";
            published = false;
        }
        window.alert(xhr.responseText);
    } else {
        xhr.open("POST", document.URL + '/publish', false);
        xhr.send();
        if (xhr.responseText == "This pad is now available for viewing!") {
            document.getElementById("publishbutton").value = "Unpublish";
            published = true;
        }
        window.alert(xhr.responseText);
    }
}

function deleteFile() {
    window.location = document.URL + "/delete";
}