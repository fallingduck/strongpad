var editor = document.getElementById('editor');
var viewer = document.getElementById('viewer');
editor.onkeyup = function() {
    viewer.innerHTML = marked(editor.innerText);
};