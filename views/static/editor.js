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
    alert(xhr.responseText);
}