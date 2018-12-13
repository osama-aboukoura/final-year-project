function report(type, id) {
    if (confirm("Are you sure you want to report this " + type + "?")) {
        if (type=='post') {
            window.open("report-post","_self")
        }
        else if (type=='comment') {
            window.open(id + "/report-comment","_self")
        }
        else if (type=='reply') {
            window.open(id + "/report-reply","_self")
        }
    } 
}

// function showLikes(listOfLikes) {
//     array = listOfLikes.replace(/, /g, '\n'); // replacing commas with line breaks 
//     alert("Users who liked this: \n\n" + array)
// }