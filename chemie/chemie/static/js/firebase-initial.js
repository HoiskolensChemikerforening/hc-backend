//TODO populate this script with the one in base.html

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue
}
function postAjax(url, data) {
    var params = typeof data == 'string' ? data : Object.keys(data).map(
            function(k){ return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
        ).join('&');

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    xhr.open('POST', url);
    xhr.onreadystatechange = function() {
        if (xhr.readyState>3 && xhr.status==200) { console.log(xhr.status); }
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    var csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader("X-CSRFToken",csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(params);
    return xhr
}

function getBrowser(){
    var browser = null
     if((navigator.userAgent.indexOf("Opera") || navigator.userAgent.indexOf('OPR')) != -1 )
    {
        browser = 'Opera'
    }
    else if(navigator.userAgent.indexOf("Chrome") != -1 )
    {
        browser = 'Chrome'
    }
    else if(navigator.userAgent.indexOf("Safari") != -1)
    {
        browser = 'Safari'
    }
    else if(navigator.userAgent.indexOf("Firefox") != -1 )
    {
         browser = 'Firefox'
    }
    else if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) //IF IE > 10
    {
      browser = 'IE'
    }
    return browser
}