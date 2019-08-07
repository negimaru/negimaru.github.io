window.onload = () => {
    'use strict';
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js');
    }

    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
        deferredPrompt = e;
    });


    document.getElementsByClassName('js-install-button')[0].addEventListener('click', (e) => {
        // Show the prompt
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice
            .then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the A2HS prompt');
                } else {
                    console.log('User dismissed the A2HS prompt');
                }
                deferredPrompt = null;
            });
    });


    const myHeaders = new Headers();

    const myInit = {
        method: 'GET',
        headers: myHeaders,
        mode: 'cors',
        cache: 'default'
    };

    const myRequest = new Request('/articles.json', myInit);



    fetch(myRequest)
        .then(function (response){ return  response.json()})
        .then(function (data) {
            console.log(data);
            const articlesContainer =  document.getElementsByClassName('articles-container')[0];
            data.map(function (article) {
                let container = document.createElement('span');
                container.className = "article"
                let image = document.createElement("img");
                image.src = "image/article.gif"

                let name = document.createElement("div");
                name.innerText = article.buyBox.nameProductBuyBox;

                let price = document.createElement('div');
                price.innerText = article.price.price + '€';

                container.append(image);
                container.append(name);
                container.append(price);

                articlesContainer.append(container);
            })
        });




}

