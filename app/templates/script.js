// This script contains a lot of console logs, as we're using it to debug
// client installations.
// For actual production script, see script.min.js.

window.onload = function () {

    function getParameterByName(name) {
        var url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results)
            return null;
        if (!results[2])
            return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }
    function checkForSlash(url) {
        // make sure we don't miss a match because customer didn't append slash
        url = url.trim();
        if (url.slice(-1) !== '/') {
            url += '/';
        }
        return url;
    }
    function checkForSignupUrl(url, signupUrl) {
        signupUrl = checkForSlash(signupUrl);
        cleanUrl = url.split('?')[0]
        if (cleanUrl === signupUrl) {
            var buzzlyRef = getParameterByName('buzzlyref');
            if (buzzlyRef !== null) {
                window.localStorage.buzzlyRef = buzzlyRef;
            }
            var buzzlyEmail = getParameterByName('buzzlyemail');
            if (buzzlyEmail !== null) {
                window.localStorage.buzzlyEmail = buzzlyEmail;
            }
        }
    }
    function postRequest(data) {
        console.log('Posting data....');
        console.log(data);
        var request = new XMLHttpRequest();
        request.open('POST', 'https://api.buzzlyapp.com/api/create-referral-signup/', true);
        request.setRequestHeader('content-type', 'application/json');
        request.send(JSON.stringify(data));
        console.log('Done!');
    }
    function checkForSignupSuccessUrl(url, signupSuccessUrl) {
        console.log('checking for signup success...');
        signupSuccessUrl = checkForSlash(signupSuccessUrl);
        console.log(signupSuccessUrl);
        cleanUrl = url.split('?')[0]
        console.log(cleanUrl);
        if (cleanUrl === signupSuccessUrl && window.localStorage.buzzlyRef !== undefined) {
            console.log('Match!');
            data = {};
            data.referral = parseInt(window.localStorage.buzzlyRef);
            if (window.localStorage.buzzlyEmail !== undefined) {
                data.email = window.localStorage.buzzlyEmail;
            }
            postRequest(data);
            window
                .localStorage
                .removeItem('buzzlyEmail');
            window
                .localStorage
                .removeItem('buzzlyRef');

        }
    }
    console.log('Runnin.....');
    // get the url
    var url = window.location.href;
    // check for signup & signup success url
    checkForSignupUrl(url, '{{ object.signup_url }}');
    checkForSignupSuccessUrl(url, '{{ object.signup_success_url}}');
}
