
/* shows a pop-up message asking the user to confirm reporting a post/comment/reply */
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

/* fades out the div below the image in a post when hoverting over the image */
function fadeOutDateAndButtons() {
    document.getElementsByClassName('buttons-and-date-fixed-bottom')[0].style.opacity = '0.1'
}

/* fades back in the div below the image in a post when hoverting away from the image */
function fadeInDateAndButtons() {
    document.getElementsByClassName('buttons-and-date-fixed-bottom')[0].style.opacity = '1'
}
