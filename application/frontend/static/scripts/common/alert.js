const show_notification = (message, status) =>{
    const NOTIFICATION_PANEL = document.getElementById('notificationPanel');

    if (NOTIFICATION_PANEL){
        const DIV_ALERT = document.createElement('div');
        const BTM_CLOSE = document.createElement('button');
        const MESSAGE = document.createElement('p');

        DIV_ALERT.setAttribute('class', 'alert');
        DIV_ALERT.classList.add('alert-dismissible');
        DIV_ALERT.classList.add('fade');
        DIV_ALERT.classList.add('show');
        DIV_ALERT.classList.add(`alert-${status}`);

        MESSAGE.innerText = message;

        BTM_CLOSE.setAttribute('class', 'btn-close');
        BTM_CLOSE.setAttribute('type', 'button');
        BTM_CLOSE.setAttribute('data-bs-dismiss', 'alert');
        BTM_CLOSE.setAttribute('aria-label', 'Close');


        DIV_ALERT.appendChild(MESSAGE);
        DIV_ALERT.appendChild(BTM_CLOSE);
        NOTIFICATION_PANEL.appendChild(DIV_ALERT);

        setTimeout(() => {
            $(DIV_ALERT).alert('close');
        }, 5000);
    }
}

export { show_notification };
