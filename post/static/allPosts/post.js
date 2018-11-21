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