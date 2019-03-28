/* hides and shows the post topic field using the checkbox in the create post form */
function toggleCheckBox() {
    var checkBox = document.getElementById("checkboxAuto");
    var postTopicBox = document.getElementById("postTopicID");
    if (checkBox.checked){
        postTopicBox.style.display = 'none'; // hide the topic field 
    } else {
        postTopicBox.removeAttribute("style") // show the topic field 
    }
}

/* this script is to show the loader while the classification algorithm runs */
function showLoaderIfFormValid() {
    var postTitle = document.getElementsByName('postTitle')[0].value;
    var postContent = document.getElementsByName('postContent')[0].value;
    var checkBox = document.getElementById("checkboxAuto");
    if (postTitle.length > 0 && postContent.length > 0 && checkBox.checked){

        // creating and adding the loader div to the page 
        var loadingLayer = document.createElement('div');
        loadingLayer.className = "loadingLayer";
        loadingLayer.innerHTML = 
            "<div class='loadingDiv'>\
                <div class='loader'></div>\
                <h3>Classifying your post... This may take up to 1 minute.</h3>\
            </div>"
        document.body.appendChild(loadingLayer)

    }
}
