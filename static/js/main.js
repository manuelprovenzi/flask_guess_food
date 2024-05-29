function start_button(){
    location.href = "/game";
}

function getClassifica(){
    location.href = "/classifica";
}

function logout(){
    location.href = "/logout";
}

window.addEventListener('beforeunload', function (e) {
    // Invio una richiesta al server quando la scheda sta per essere chiusa
    //navigator.sendBeacon('/window_closed', JSON.stringify({ message: 'La scheda è stata chiusa.' }));

    // Se vuoi mostrare un messaggio di conferma di uscita
    // e.returnValue = '';
});

function timerTerminato(){
    location.href = "/game?timer=terminato";
}