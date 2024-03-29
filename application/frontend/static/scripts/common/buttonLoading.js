const make_button_load = (buttonElement, text) => {

    buttonElement.disabled = true;
    buttonElement.innerText = '';

    const SPAN_SPINNER = document.createElement('span');
    const SPAN_TEXT = document.createElement('span');

    SPAN_SPINNER.classList.add('loader');
    SPAN_TEXT.classList.add('loader');

    SPAN_SPINNER.classList.add('spinner-border');
    SPAN_SPINNER.classList.add('spinner-border-lg');
    SPAN_SPINNER.setAttribute('role', 'status');
    SPAN_SPINNER.setAttribute('aria-hidden', 'true');

    if (!text || text.trim() === '') {
        SPAN_TEXT.classList.add('visually-hidden');
        SPAN_TEXT.innerText = 'Loading...';
    } else {
        SPAN_TEXT.innerText = text;
    }



    buttonElement.appendChild(SPAN_SPINNER);
    buttonElement.appendChild(SPAN_TEXT);
}

const remove_button_load = (buttonElement, text) => {

    buttonElement.disabled = false;
    buttonElement.innerText = text;

    buttonElement.querySelectorAll('.loader').forEach(loaderElement=>{
        buttonElement.removeChild(loaderElement);
    });
}

export { make_button_load, remove_button_load };
