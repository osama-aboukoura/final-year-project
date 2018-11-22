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


function disable(type, id, disabled) {
    var verb = disabled == 'True' ? 'enable' : 'disable'; 
    if (confirm("Are you sure you want to " + verb + " this " + type + "?")) {
        if (type=='post') {
            window.open("/" + id + "/disable-post","_self")
        }
        else if (type=='comment') {
            window.open("/" + id + "/disable-comment","_self")
        }
        else if (type=='reply') {
            window.open("/" + id + "/disable-reply","_self")
        }
    }
}