function toggleCheckBox() {
    var checkBox = document.getElementById("checkboxAuto");
    var postTopicBox = document.getElementById("postTopicID");
    if (checkBox.checked){
        postTopicBox.style.display = 'none'; // hide the topic field 
    } else {
        postTopicBox.removeAttribute("style") // show the topic field 
    }
}
