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
    xhr.send("data=" + window.encodeURIComponent(editor.innerText));
    if (xhr.responseText == "You are not logged in, or your session expired!") {
        window.open("/", "_blank");
    } else {
        window.alert(xhr.responseText);
    }
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

function uploadImage() {
    var namefield = document.getElementById("filenamefield");
    var filename = namefield.value;
    var form = document.getElementById("uploadform");
    form.submit();
    editor.innerText = editor.innerText + "![Alt text](/uploads/" + filename + ")";
}

function updateFilename() {
    var namefield = document.getElementById("filenamefield");
    var uploader = document.getElementById("uploadfield");
    namefield.value = uploader.value.split("\\").pop();
}

function printFile() {
    window.open(document.URL + "/html", "_blank");
}

document.addEventListener("keydown", function(e) {
  if (e.keyCode == 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)) {
    e.preventDefault();
    saveFile();
  }
}, false);

document.addEventListener("keydown", function(e) {
  if (e.keyCode == 80 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)) {
    e.preventDefault();
    printFile();
  }
}, false);