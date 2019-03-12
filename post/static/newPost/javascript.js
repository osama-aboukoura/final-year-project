function toggleCheckBox() {
    var checkBox = document.getElementById("checkboxAuto");
    var postTopicBox = document.getElementById("postTopicID");
    if (checkBox.checked){
        postTopicBox.style.display = 'none';
    } else {
        postTopicBox.removeAttribute("style")
    }
}
