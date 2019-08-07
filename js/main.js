window.onload = () => {
    'use strict';
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js');
    }

    fetch()



    const myHeaders = new Headers();

    const myInit = { method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default' };

    const myRequest = new Request('www.pccomponentes.com/ajax_nc/get?idArticle=53216', myInit);

    fetch(myRequest).then(function(response) {
        console.log(response);
    });


}

