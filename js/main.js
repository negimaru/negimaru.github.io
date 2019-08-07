window.onload = () => {
    'use strict';




    /* Only register a service worker if it's supported */
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js');

    }


    const divInstall = document.getElementById('installContainer');
    const butInstall = document.getElementById('butInstall');



    window.addEventListener('beforeinstallprompt', (event) => {
        console.log('👍', 'beforeinstallprompt', event);
        // Stash the event so it can be triggered later.
        window.deferredPrompt = event;
        // Remove the 'hidden' class from the install button container
        divInstall.classList.toggle('hidden', false);
    });

    butInstall.addEventListener('click', () => {
        console.log('👍', 'butInstall-clicked');
        const promptEvent = window.deferredPrompt
        if (!promptEvent) {
            return;
        }
        promptEvent.prompt();
        promptEvent.userChoice.then((result) => {
            console.log('👍', 'userChoice', result);
            window.deferredPrompt = null;
            divInstall.classList.toggle('hidden', true);
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








    const Installer = function(root) {
        let promptEvent;

        const install = function(e) {
            if(promptEvent) {
                promptEvent.prompt();
                promptEvent.userChoice
                    .then(function(choiceResult) {
                        // The user actioned the prompt (good or bad).
                        // good is handled in
                        promptEvent = null;
                        ga('send', 'event', 'install', choiceResult);
                        root.classList.remove('available');
                    })
                    .catch(function(installError) {
                        // Boo. update the UI.
                        promptEvent = null;
                        ga('send', 'event', 'install', 'errored');
                        root.classList.remove('available');
                    });
            }
        };

        const installEl = document.getElementById('installer');
        const installer = new Installer(installEl);


}

