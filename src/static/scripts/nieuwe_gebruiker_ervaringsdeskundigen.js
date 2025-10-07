// $(document).ready(function () {
//     console.log("jQuery werkt!");
//     console.log(typeof jQuery);
//
//     // Heeft toezichthouder
//     $("#toezichthouder_ja").change(function () {
//         $("#heeft_toezichthouder").fadeIn();
//     });
//
//     $("#toezichthouder_nee").change(function () {
//         $("#heeft_toezichthouder").fadeOut();
//     });
//
//     $('form').on('submit', function (event) {
//         event.preventDefault();
//
//         let isValid = true;
//
//         // tekst input
//         $('.input[required]').each(function () {
//             let inputVal = $(this).val().trim();
//             let inputId = $(this).attr('id');
//             let errorSpan = $('#error-' + inputId);
//
//             if (inputVal === '') {
//                 errorSpan.show();
//                 isValid = false;
//
//             } else {
//                 errorSpan.hide();
//             }
//         });
//
//         // Checkbox
//         let checkbox = $('#akkoord_voorwaarden');
//         let errorCheckbox = $('#error-akkoord_voorwaarden');
//
//         if (!checkbox.prop('checked')) {
//             errorCheckbox.fadeIn();
//             isValid = false;
//         } else {
//             errorCheckbox.fadeOut();
//         }
//
//         if (!isValid) {
//             return;
//         }
//
//         if (!isValid) {
//             return;
//         }
//
//         // Cirkels
//         let radioName = 'toezichthouder';
//         let errorRadio = $('#error-toezichthouder');
//
//         if (!$('input[name="' + radioName + '"]:checked').length) {
//             errorRadio.fadeIn();
//             isValid = false;
//         } else {
//             errorRadio.fadeOut();
//         }
//
//         if (!isValid) {
//             return;
//         }
//
//         // // Datum
//         // let dateName = '#geboortedatum';
//         // let errorDate = $('#error-geboortedatum');
//
//         if (!$('input[name="' + dateName + '"]:checked').length) {
//             errorDate.fadeIn();
//             isValid = false;
//         } else {
//             errorDate.fadeOut();
//         }
//
//         if (!isValid) {
//             return;
//         }
//
//         // email (nodig, maar aanpassen zodat bepaalde tekens (niet) toegestaan zijn)
//         let emailName = '#email';
//         let errorEmail = $('#error-email');
//
//         if (!emailInput.val().includes('@')) {
//             errorEmail.fadeIn();
//             isValid = false;
//         } else {
//             errorEmail.fadeOut();
//         }
//
//         if (!isValid) {
//             return;
//         }
//
//         $.ajax({
//             type: 'POST',
//             url: '/process',
//             data: {
//                 voornaam: $('#voornaam').val(),
//                 achternaam: $('#achternaam').val(),
//                 postcode: $('#postcode').val(),
//                 geslacht: $('#geslacht').val(),
//                 email: $('#email').val(),
//                 telefoonnummer: $('#telefoonnummer').val(),
//                 geboortedatum: $('#geboortedatum').val(),
//                 type_beperking: $('#type_beperking').val(),
//                 gebruikte_hulpmiddelen: $('#gebruikte_hulpmiddelen ').val(),
//                 kort_voorstellen: $('#kort_voorstellen ').val(),
//                 bijzonderheden: $('#bijzonderheden').val(),
//                 akkoord_voorwaarden: $('#akkoord_voorwaarden').prop('checked') ? 'Ja' : 'Nee',
//
//                 // Toezichthouder
//                 toezichthouder: $('#toezichthouder').val(),
//                 naam_voogd_toezichthouder: $('#naam_voogd_toezichthouder').val(),
//                 e_mailadres_voogd_toezichthouder: $('#e_mailadres_voogd_toezichthouder').val(),
//                 telefoonnummer_voogd_toezichthouder: $('#telefoonnummer_voogd_toezichthouder').val(),
//
//                 // Overige vragen
//                 voorkeur_benadering: $('#voorkeur_benadering').val(),
//                 type_onderzoek: $('#type_onderzoek').val(),
//                 bijzonderheden_beschikbaarheid: $('#bijzonderheden_beschikbaarheid ').val(),
//             },
//
//         })
//
//             .done(function (data) {
//
//                 if (data.error) {
//                     $('#erroralert').text(data.error).show();
//                     $('#succesalert').hide();
//                 } else {
//                     $('#succesalert').text(data.message).show();
//                     $('#erroralert').hide();
//                     $('form')[0].reset();
//                     $("#heeft_toezichthouder").hide();
//                 }
//
//                 // Checkt voor input, tonen van rode tekst
//                 $('input[required]').on('input', function () {
//                     let inputId = $(this).attr('id');
//                     $('#error-' + inputId).fadeOut();
//
//             });
//         });
//
//     });
// });

$(document).ready(function () {
    console.log("jQuery werkt!");
    console.log(typeof jQuery);

    // Checkt voor input, tonen van rode tekst
    $('input[required]').on('input', function() {
        let inputId = $(this).attr('id');
        $('#error-' + inputId).fadeOut();
    });

    // Heeft toezichthouder
    $("#toezichthouder_ja").change(function () {
        $("#heeft_toezichthouder").fadeIn();
    });

    $("#toezichthouder_nee").change(function () {
        $("#heeft_toezichthouder").fadeOut();
    });

});

// Javascript validation
const formulier_gebruikers = document.getElementById('formulier_gebruikers')
const voornaam = document.getElementById('voornaam')
const achternaam = document.getElementById('achternaam')
const postcode = document.getElementById('postcode')
const geslacht = document.getElementById('geslacht')
const email = document.getElementById('email')
const telefoonnummer = document.getElementById('telefoonnummer')
const geboortedatum = document.getElementById('geboortedatum')
const type_beperking = document.getElementById('type_beperking')
const gebruikte_hulpmiddelen = document.getElementById('gebruikte_hulpmiddelen')
const kort_voorstellen = document.getElementById('kort_voorstellen')
const bijzonderheden = document.getElementById('bijzonderheden')
const akkoord_voorwaarden = document.getElementById('akkoord_voorwaarden')
const toezichthouder = document.getElementById('toezichthouder')
const naam_voogd_toezichthouder = document.getElementById('naam_voogd_toezichthouder')
const e_mailadres_voogd_toezichthouder = document.getElementById('e_mailadres_voogd_toezichthouder')
const telefoonnummer_voogd_toezichthouder = document.getElementById('telefoonnummer_voogd_toezichthouder')
const voorkeur_benadering = document.getElementById('voorkeur_benadering')
const type_onderzoek = document.getElementById('type_onderzoek')
const bijzonderheden_beschikbaarheid = document.getElementById('bijzonderheden_beschikbaarheid')

formulier_gebruikers.addEventListener('submit', e => {
     e.preventDefault();

     validateInputs();
});

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('succes')

}

const setSucces = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('succes');
    inputControl.classList.remove('error')
};

const isValidEmail = email => {
    const re = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    return re.test(email.toLowerCase());
}

const validateInputs = () => {
    const voornaamValue = voornaam.value.trim()
    const achternaamValue = achternaam.value.trim()
    const postcodeValue = postcode.value.trim()
    const geslachtValue = geslacht.value.trim()
    const emailValue = email.value.trim()
    const telefoonnummerValue = telefoonnummer.value.trim()
    const geboortedatumValue = geboortedatum.value.trim()
    const type_beperkingValue = type_beperking.value.trim()
    const gebruikte_hulpmiddelenValue = gebruikte_hulpmiddelen.value.trim()
    const kort_voorstellenValue = kort_voorstellen.value.trim()
    const bijzonderhedenValue = bijzonderheden.value.trim()
    const akkoord_voorwaardenValue = akkoord_voorwaarden.value.trim()
    const toezichthouderValue = toezichthouder.value.trim()
    const naam_voogd_toezichthouderValue = naam_voogd_toezichthouder.value.trim()
    const e_mailadres_voogd_toezichthouderValue = e_mailadres_voogd_toezichthouder.value.trim()
    const telefoon_voogd_toezichthouderValue = telefoonnummer_voogd_toezichthouder.value.trim()
    const voorkeur_benaderingValue = voorkeur_benadering.value.trim()
    const type_onderzoekValue = type_onderzoek.value.trim()
    const bijzonderheden_beschikbaarheidValue = bijzonderheden_beschikbaarheid.value.trim()

    if (voornaamValue === '') {
        setError(voornaam, 'Hier je voornaam invullen is verplicht!')
    } else {
        setSucces(voornaam);
    }

    if (achternaamValue === '') {
    setError(achternaam, 'Hier je achternaam invullen is verplicht!')
    } else {
        setSucces(achternaam);
    }

    if (postcodeValue === '') {
        setError(postcode, 'Hier je postcode invullen is verplicht!')
    } else {
        setSucces(postcode);
    }

    if (geslachtValue === '') {
        setError(geslacht, 'Hier je geslacht invullen is verplicht!')
    } else {
        setSucces(geslacht);
    }

    if (emailValue === '') {
        setError(email, 'Hier je e-mailadres invullen is verplicht!')
    } else if (!isValidEmail(emailValue)) {
        setError(email, 'Vul de juiste email in!')
    } else {
        setSucces(email);
    }

    if (telefoonnummerValue === '') {
        setError(telefoonnummer, 'Hier je telefoonnummer invullen is verplicht!')
    } else {
        setSucces(telefoonnummer);
    }

    if (geboortedatumValue === '') {
        setError(geboortedatum, 'Hier je geboortedatum invullen is verplicht!')
    } else {
        setSucces(geboortedatum);
    }

    if (type_beperkingValue === '') {
        setError(type_beperking, 'Hier je type beperking aanklikken is verplicht (minimaal 1)!')
    } else {
        setSucces(type_beperking);
    }

    if (gebruikte_hulpmiddelenValue === '') {
        setError(gebruikte_hulpmiddelen, '')
    } else {
        setSucces(gebruikte_hulpmiddelen);
    }

    if (kort_voorstellenValue === '') {
        setError(kort_voorstellen, '')
    } else {
        setSucces(kort_voorstellen);
    }

    if (bijzonderhedenValue === '') {
        setError(bijzonderheden, '')
    } else {
        setSucces(bijzonderheden);
    }

    if (akkoord_voorwaardenValue === '') {
        setError(akkoord_voorwaarden, 'U moet akkoord gaan met de voorwaarden!')
    } else {
        setSucces(akkoord_voorwaarden);
    }

    if (toezichthouderValue === '') {
        setError(toezichthouder, 'Vul hier ja of nee in: Heeft u een toezichthouder? Invullen is verplicht!')
    } else {
        setSucces(toezichthouder);
    }

    if (naam_voogd_toezichthouderValue === '') {
        setError(naam_voogd_toezichthouder, 'Vul hier de naam van uw voogd of toezichthouder in, invullen is verplicht!')
    } else {
        setSucces(naam_voogd_toezichthouder);
    }

    if (e_mailadres_voogd_toezichthouderValue === '') {
        setError(e_mailadres_voogd_toezichthouder, 'Vul hier het e-mailadres van uw voogd of toezichthouder invullen is verplicht!')
    } else {
        setSucces(e_mailadres_voogd_toezichthouder);
    }

    if (telefoon_voogd_toezichthouderValue === '') {
        setError(telefoonnummer_voogd_toezichthouder, 'Vul hier het telefoonnummer in van uw voogd of toezichthouder, invullen is verplicht!')
    } else {
        setSucces(telefoonnummer_voogd_toezichthouder);
    }

    if (voorkeur_benaderingValue === '') {
        setError(voorkeur_benadering, 'Klik hier uw voorkeur voor benadering, invullen is verplicht!')
    } else {
        setSucces(voorkeur_benadering);
    }

    if (type_onderzoekValue === '') {
        setError(type_onderzoek, 'Klik hier uw type_onderzoek aan, invullen is verplicht!')
    } else {
        setSucces(type_onderzoek);
    }

    if (bijzonderheden_beschikbaarheidValue === '') {
        setError(bijzonderheden_beschikbaarheid, '')
    } else {
        setSucces(bijzonderheden_beschikbaarheid);
    }

    console.log("het werkt niet....")

};